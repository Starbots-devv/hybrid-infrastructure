"""Reproducible constant-demand economics. No provider API or live price lookup."""
from decimal import Context, Decimal, Inexact, ROUND_HALF_UP, localcontext
from datetime import datetime
from calendar import monthrange
from .contracts import timestamp, validate
from .io import fail

CONTEXT=Context(prec=50,rounding=ROUND_HALF_UP,Emin=-256,Emax=256)
MINOR_DIGITS={'USD':2,'EUR':2,'GTQ':2,'JPY':0}

def month_hours(period_definition,month):
    if period_definition['kind']=='fixed_730_hours':return 730
    if period_definition['kind']!='calendar_month':fail('INVALID_UNIT','Unsupported month-hour definition')
    year,first=map(int,period_definition['start_month'].split('-'))
    index=first-1+month-1
    return 24*monthrange(year+index//12,index%12+1)[1]

def decimal(value):
    try:
        if not isinstance(value,str):raise ValueError()
        n=Decimal(value)
        if not n.is_finite() or len(n.as_tuple().digits)>50:raise ValueError()
        return n
    except (ValueError,ArithmeticError):fail('INVALID_SCHEMA','Expected a finite decimal string')

def text(number):
    if number==0:return '0'
    value=format(number,'f')
    return value.rstrip('0').rstrip('.') if '.' in value else value

def calculate_cost(snapshot,scenario_id,view,as_of):
    validate(snapshot,expected_kind='CostSnapshot',as_of=as_of)
    if view not in ('incremental_cash','allocated_tco'):fail('INVALID_SCHEMA','Unknown accounting view')
    p=snapshot['payload'];now=timestamp(as_of)
    try:datetime.strptime(p['period_definition']['start_month'],'%Y-%m')
    except ValueError:fail('INVALID_SCHEMA','Invalid cost calendar month')
    if p['fx_snapshot_refs']:fail('UNSUPPORTED_FEATURE','FX conversion is deferred; supply one comparable currency')
    selected=[l for l in p['lines'] if l['view'] in ('both',view)]
    currencies={l['currency'] for l in selected}
    if len(currencies)!=1:fail('INCOMPARABLE_COSTS','A view must use exactly one known currency')
    currency=next(iter(currencies))
    if currency not in MINOR_DIGITS:fail('UNSUPPORTED_CURRENCY','Currency minor-unit metadata is not available')
    seen=set();lines=[];unknown=[];stale=[]
    with localcontext(CONTEXT) as ctx:
        quantum=Decimal(1).scaleb(-MINOR_DIGITS[currency]);monthly=Decimal(0);once=Decimal(0);unrounded=Decimal(0)
        source_stale=p['valid_until'] is None or now>=timestamp(p['valid_until']) or timestamp(p['observed_at'])>now or (now-timestamp(p['observed_at'])).days>30
        for line in selected:
            if line['allocation_id'] in seen:fail('DUPLICATE_ALLOCATION','A cost allocation is counted twice in this view')
            seen.add(line['allocation_id'])
            if line['price_kind']!=p['accounting_basis']:fail('INCOMPARABLE_COSTS','Price bases cannot be mixed')
            if line['period']=='one_time' and line['unit']!='one_time':fail('INVALID_UNIT','One-time lines require one_time units')
            if line['period']=='hourly' and line['unit']!='hour':fail('INVALID_UNIT','Hourly usage requires hour units')
            is_stale=source_stale or line['valid_until'] is None or now>=timestamp(line['valid_until']) or timestamp(line['observed_at'])>now or (now-timestamp(line['observed_at'])).days>30
            amount=None;ctx.clear_flags()
            if line['unit_rate'] is None:unknown.append(line['id'])
            elif is_stale:stale.append(line['id'])
            else:
                try:
                    raw=decimal(line['quantity'])*decimal(line['unit_rate'])
                    if line['period']=='hourly':raw*=month_hours(p['period_definition'],1)
                    rounded=raw.quantize(quantum)
                except ArithmeticError:fail('RESOURCE_LIMIT','Cost exceeds the declared decimal context')
                if line['period']=='one_time':once+=rounded
                else:monthly+=rounded;unrounded+=raw
                amount=text(rounded)
            assumptions=[*line['assumptions'],'Decimal precision=50; ROUND_HALF_UP; inexact='+str(ctx.flags[Inexact]).lower(),'Period: '+p['period_definition']['kind']+' starting '+p['period_definition']['start_month']+'; hourly quantity uses actual calendar days or explicit fixed 730 hours.']
            lines.append({'id':line['id'],'resource_id':line['resource_id'],'provider':line['provider'],'service':line['service'],'quantity':line['quantity'],'unit':line['unit'],'unit_rate':line['unit_rate'],'currency':currency,'period':line['period'],'amount':amount,'source_uri':line['source']['uri'],'evidence_level':line['evidence_level'],'assumptions':assumptions})
        if any(e['material'] for e in p['exclusions']):unknown.append('material-exclusion')
        complete=not unknown and not stale and p['completeness']=='complete'
        return {'scenario_id':scenario_id,'view':view,'currency':currency,'accounting_basis':p['accounting_basis'],'complete':complete,'known_monthly_subtotal':text(monthly),'monthly_total':text(monthly) if complete else None,'one_time_total':text(once) if complete else None,'unrounded_monthly_total':text(unrounded) if complete else None,'rounding_delta':text(monthly-unrounded) if complete else None,'unknown_line_ids':unknown,'stale_line_ids':stale,'lines':lines}

def compare(baseline,proposed,*,baseline_id,scenario_id,baseline_series=None,proposed_series=None):
    reasons=[]
    for key in ('currency','accounting_basis','view'):
        if baseline[key]!=proposed[key]:reasons.append('Incompatible '+key)
    if not baseline['complete'] or not proposed['complete']:reasons.append('Cost data is incomplete or stale')
    if (baseline_series is None)!=(proposed_series is None):reasons.append('Both monthly series are required')
    if baseline_series is not None and (len(baseline_series)!=36 or len(proposed_series)!=36):reasons.append('Exactly 36 months are required')
    out={'baseline_id':baseline_id,'scenario_id':scenario_id,'view':proposed['view'],'currency':proposed['currency'],'comparable':not reasons,'reasons':reasons,'monthly_saving':None,'saving_percent':None,'incremental_investment':None,'net_12_months':None,'net_36_months':None,'break_even_month':None,'monthly_series':[]}
    if reasons:return out
    with localcontext(CONTEXT) as ctx:
        b=decimal(baseline['monthly_total']);p=decimal(proposed['monthly_total'])
        investment=decimal(proposed['one_time_total'])-decimal(baseline['one_time_total']);saving=b-p
        if baseline_series is None:
            baseline_series=[baseline['monthly_total']]*36
            proposed_series=[proposed['monthly_total']]*36
        if decimal(baseline_series[0])!=b or decimal(proposed_series[0])!=p:fail('INCOMPARABLE_COSTS','Month one must reconcile with displayed cost totals')
        if any(decimal(v)<0 for v in (*baseline_series,*proposed_series)):fail('INCOMPARABLE_COSTS','Monthly costs cannot be negative')
        out.update(monthly_saving=text(saving),saving_percent=text((saving/b*100).quantize(Decimal('.01'))) if b>0 else None,incremental_investment=text(investment))
        cumulative=-investment
        for month,(base_amount,proposed_amount) in enumerate(zip(baseline_series,proposed_series),1):
            base_month=decimal(base_amount);proposed_month=decimal(proposed_amount)
            month_saving=base_month-proposed_month;cumulative+=month_saving
            out['monthly_series'].append({'month':month,'baseline':text(base_month),'proposed':text(proposed_month),'saving':text(month_saving),'cumulative_net':text(cumulative)})
            if out['break_even_month'] is None and cumulative>=0:out['break_even_month']=month
            if month==12:out['net_12_months']=text(cumulative)
            if month==36:out['net_36_months']=text(cumulative)
        if ctx.flags[Inexact]:out['reasons'].append('Decimal inexact flag set by division/presentation; declared context preserved')
    return out
