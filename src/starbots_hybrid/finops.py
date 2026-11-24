"""Bounded, explicit monthly overrides for local FinOps comparisons."""
from decimal import Decimal, localcontext
from copy import deepcopy

from .contracts import timestamp, validate
from .economics import CONTEXT, MINOR_DIGITS, calculate_cost, decimal, month_hours, text
from .io import fail, inspect_data


PLAN_KEYS = {'format', 'scenario_id', 'client_id', 'project_id', 'observed_at',
             'valid_until', 'currency', 'start_month', 'tax_status', 'source_uri',
             'line_rules', 'promotions'}


def _plan(plan, snapshot, scenario_id, as_of):
    inspect_data(plan)
    if not isinstance(plan, dict) or not PLAN_KEYS.issubset(plan) or set(plan)-PLAN_KEYS-{'fx','asset_rules'} or plan['format'] != 'starbots-finops-1':
        fail('INVALID_SCHEMA', 'Unsupported FinOps plan structure')
    if (plan['scenario_id'], plan['client_id'], plan['project_id']) != (
            scenario_id, snapshot['client_id'], snapshot['project_id']):
        fail('IDENTITY_MISMATCH', 'FinOps plan belongs to another subject')
    if plan['start_month'] != snapshot['payload']['period_definition']['start_month']:
        fail('INCOMPARABLE_COSTS', 'FinOps month boundary differs from price snapshot')
    if not isinstance(plan['currency'], str) or plan['currency'] not in MINOR_DIGITS or plan['tax_status'] != 'pre_tax_unknown':
        fail('UNSUPPORTED_FEATURE', 'Unknown currency or tax treatment')
    if not isinstance(plan['source_uri'], str) or not plan['source_uri'] or len(plan['source_uri']) > 1000:
        fail('INVALID_SCHEMA', 'A bounded input source is required')
    now = timestamp(as_of)
    if timestamp(plan['observed_at']) > now or now >= timestamp(plan['valid_until']):
        fail('EVIDENCE_STALE', 'FinOps assumptions are future-dated or expired')
    fx=plan.get('fx')
    if fx is not None:
        keys={'version','from_currency','to_currency','direction','rate','spread_percent','observed_at','valid_until','source_uri'}
        if not isinstance(fx,dict) or set(fx)!=keys or fx['version']!='1.0.0' or fx['direction']!='multiply' or not isinstance(fx['from_currency'],str) or fx['from_currency'] not in MINOR_DIGITS or fx['to_currency']!=plan['currency'] or fx['from_currency']==fx['to_currency']:
            fail('INVALID_SCHEMA','Unsupported versioned FX direction or currency pair')
        if timestamp(fx['observed_at'])>now or now>=timestamp(fx['valid_until']):fail('EVIDENCE_STALE','FX quote is future-dated or expired')
        if decimal(fx['rate'])<=0 or not 0<=decimal(fx['spread_percent'])<=100:fail('INVALID_SCHEMA','Invalid FX rate or spread')
        if not isinstance(fx['source_uri'],str) or not fx['source_uri'] or len(fx['source_uri'])>1000:fail('INVALID_SCHEMA','FX needs a bounded source')
    if not isinstance(plan['line_rules'], list) or len(plan['line_rules']) > 1000:
        fail('RESOURCE_LIMIT', 'Invalid FinOps line count')
    if not isinstance(plan['promotions'], list) or len(plan['promotions']) > 100:
        fail('RESOURCE_LIMIT', 'Invalid promotion count')
    known = {line['id'] for line in snapshot['payload']['lines']}
    rules = {}
    by_id={line['id']:line for line in snapshot['payload']['lines']}
    asset_rules=plan.get('asset_rules',[])
    if not isinstance(asset_rules,list) or len(asset_rules)>100:fail('RESOURCE_LIMIT','Invalid asset rule count')
    assets=set()
    quantum=Decimal(1).scaleb(-MINOR_DIGITS[plan['currency']])
    for asset in asset_rules:
        if not isinstance(asset,dict) or set(asset)!={'resource_id','purchase_line_id','depreciation_line_id','purchase_cost','residual_value','life_months'}:fail('INVALID_SCHEMA','Invalid asset allocation rule')
        resource=asset['resource_id']
        if not isinstance(resource,str) or not resource or not isinstance(asset['depreciation_line_id'],str) or (asset['purchase_line_id'] is not None and not isinstance(asset['purchase_line_id'],str)):
            fail('INVALID_SCHEMA','Asset identifiers must be strings')
        dep=by_id.get(asset['depreciation_line_id'])
        if resource in assets or dep is None or dep['resource_id']!=resource or dep['period']!='monthly' or dep['view']!='allocated_tco' or dep['unit_rate'] is None:fail('DUPLICATE_ALLOCATION','Asset depreciation needs one TCO-only line')
        assets.add(resource)
        life=asset['life_months']
        if type(life) is not int or not 36<=life<=240:fail('INVALID_SCHEMA','Asset life must cover the 36-month model')
        purchase_cost=decimal(asset['purchase_cost']);residual=decimal(asset['residual_value'])
        if purchase_cost<0 or residual<0 or residual>purchase_cost:fail('INVALID_SCHEMA','Invalid asset acquisition or residual value')
        expected=((purchase_cost-residual)/life).quantize(quantum)
        observed=(decimal(dep['quantity'])*decimal(dep['unit_rate'])).quantize(quantum)
        if expected!=observed:fail('INCOMPARABLE_COSTS','Depreciation does not reconcile to declared asset life')
        purchase_id=asset['purchase_line_id']
        if purchase_id is not None:
            purchase=by_id.get(purchase_id)
            if purchase is None or purchase['resource_id']!=resource or purchase['period']!='one_time' or purchase['view']!='incremental_cash' or purchase['unit_rate'] is None:fail('DUPLICATE_ALLOCATION','Asset purchase must be cash-only')
            if (decimal(purchase['quantity'])*decimal(purchase['unit_rate'])).quantize(quantum)!=purchase_cost:fail('INCOMPARABLE_COSTS','Purchase line disagrees with asset rule')
    for rule in plan['line_rules']:
        if not isinstance(rule, dict) or set(rule) != {'line_id', 'segments'} or not isinstance(rule['line_id'],str) or rule['line_id'] not in known or rule['line_id'] in rules:
            fail('INVALID_SCHEMA', 'Duplicate or unknown line override')
        if not isinstance(rule['segments'], list) or not 1 <= len(rule['segments']) <= 36:
            fail('INVALID_SCHEMA', 'Expected bounded monthly segments')
        if by_id[rule['line_id']]['period']=='one_time':fail('INVALID_SCHEMA','One-time charges cannot be monthly overrides')
        if any(asset['depreciation_line_id']==rule['line_id'] for asset in asset_rules):fail('INVALID_SCHEMA','Depreciation cannot be overridden by demand rules')
        segments = {}
        for segment in rule['segments']:
            allowed={'first','last','unit_rate','quantity','growth_percent','tiers','minimum','block_size','block_price'}
            if not isinstance(segment, dict) or not {'first','last'}.issubset(segment) or set(segment)-allowed:
                fail('INVALID_SCHEMA', 'Unsupported monthly segment')
            first, last = segment['first'], segment['last']
            if type(first) is not int or type(last) is not int or not 1 <= first <= last <= 36:
                fail('INVALID_SCHEMA', 'Invalid month range')
            if 'unit_rate' in segment and ('tiers' in segment or 'block_size' in segment):fail('INVALID_SCHEMA','Choose one pricing rule')
            if ('block_size' in segment)!=('block_price' in segment):fail('INVALID_SCHEMA','Block size and price must be paired')
            for key in ('unit_rate','quantity','minimum','block_size','block_price'):
                if key in segment and decimal(segment[key])<0:fail('INVALID_SCHEMA','Negative price or quantity')
            if 'block_size' in segment and decimal(segment['block_size'])==0:fail('INVALID_SCHEMA','Block size must be positive')
            if 'growth_percent' in segment and not Decimal('-100')<=decimal(segment['growth_percent'])<=Decimal('1000'):fail('INVALID_SCHEMA','Unbounded growth input')
            if 'tiers' in segment:
                tiers=segment['tiers']
                if not isinstance(tiers,list) or not 1<=len(tiers)<=100:fail('INVALID_SCHEMA','Invalid marginal tiers')
                previous=Decimal(0)
                for index,tier in enumerate(tiers):
                    if not isinstance(tier,dict) or set(tier)!={'through','unit_rate'} or decimal(tier['unit_rate'])<0:fail('INVALID_SCHEMA','Invalid tier')
                    if tier['through'] is None:
                        if index!=len(tiers)-1:fail('INVALID_SCHEMA','Unbounded tier must be last')
                    else:
                        ceiling=decimal(tier['through'])
                        if ceiling<=previous:fail('INVALID_SCHEMA','Tier thresholds must increase')
                        previous=ceiling
                if tiers[-1]['through'] is not None:fail('INVALID_SCHEMA','Marginal tiers must cover all demand')
            for month in range(first, last + 1):
                if month in segments:fail('DUPLICATE_ALLOCATION', 'Overlapping monthly rate overrides')
                segments[month] = segment
        rules[rule['line_id']] = segments
    promotions=[];seen=set();pool_totals={}
    for promotion in plan['promotions']:
        expected={'id','pool_id','first','last','monthly_cap','pool_total','eligible_line_ids'}
        if not isinstance(promotion,dict) or set(promotion)!=expected or not isinstance(promotion['id'],str) or not promotion['id'].isascii() or not promotion['id'].replace('-','').replace('_','').isalnum() or len(promotion['id'])>55 or promotion['id'] in seen:fail('INVALID_SCHEMA','Invalid or duplicate promotion')
        seen.add(promotion['id'])
        first,last=promotion['first'],promotion['last']
        if type(first) is not int or type(last) is not int or not 1<=first<=last<=36:fail('INVALID_SCHEMA','Invalid promotion period')
        if not isinstance(promotion['pool_id'],str) or not promotion['pool_id'] or len(promotion['pool_id'])>64:fail('INVALID_SCHEMA','Invalid shared promotion pool')
        cap,total=decimal(promotion['monthly_cap']),decimal(promotion['pool_total'])
        if cap<0 or total<0:fail('INVALID_SCHEMA','Negative promotion credit')
        if not isinstance(promotion['eligible_line_ids'],list) or not promotion['eligible_line_ids'] or any(not isinstance(line_id,str) for line_id in promotion['eligible_line_ids']) or len(promotion['eligible_line_ids'])!=len(set(promotion['eligible_line_ids'])) or any(line_id not in by_id or by_id[line_id]['period']=='one_time' for line_id in promotion['eligible_line_ids']):fail('INVALID_SCHEMA','Promotion eligibility must name recurring lines')
        pool=promotion['pool_id']
        if pool in pool_totals and pool_totals[pool]!=total:fail('INVALID_SCHEMA','Shared pool balances disagree')
        pool_totals[pool]=total
        promotions.append(promotion)
    return rules,promotions,pool_totals


def _converted_snapshot(snapshot,plan):
    fx=plan.get('fx')
    if fx is None:return snapshot
    if snapshot['payload']['fx_snapshot_refs']:fail('UNSUPPORTED_FEATURE','External FX references require separate verification')
    converted=deepcopy(snapshot);matched=False
    with localcontext(CONTEXT):
        factor=decimal(fx['rate'])*(Decimal(1)+decimal(fx['spread_percent'])/100)
        for line in converted['payload']['lines']:
            if line['currency']==fx['from_currency']:
                matched=True
                if line['unit_rate'] is not None:line['unit_rate']=text(decimal(line['unit_rate'])*factor)
                line['currency']=fx['to_currency']
                line['assumptions'].append('FX '+fx['from_currency']+' to '+fx['to_currency']+' multiply, quoted '+fx['rate']+', spread '+fx['spread_percent']+'%; source '+fx['source_uri']+'.')
            elif line['currency']!=fx['to_currency']:fail('INCOMPARABLE_COSTS','No FX quote covers a line currency')
    if not matched:fail('INVALID_SCHEMA','Unused FX snapshot')
    return converted


def _tier_cost(quantity,tiers):
    total=Decimal(0);previous=Decimal(0)
    for tier in tiers:
        through=decimal(tier['through']) if tier['through'] is not None else quantity
        units=max(Decimal(0),min(quantity,through)-previous)
        total+=units*decimal(tier['unit_rate'])
        previous=through
        if previous>=quantity:break
    return total


def calculate_series(snapshot, scenario_id, view, as_of, plan):
    """Return the existing cost row at month one and 36 reconciled month totals."""
    validate(snapshot,expected_kind='CostSnapshot',as_of=as_of)
    rules,promotions,pools = _plan(plan, snapshot, scenario_id, as_of)
    snapshot=_converted_snapshot(snapshot,plan)
    row = calculate_cost(snapshot, scenario_id, view, as_of)
    if row['currency'] != plan['currency']:fail('INCOMPARABLE_COSTS', 'FinOps currency differs from prices')
    if not row['complete']:
        return row, [None] * 36
    selected = [line for line in snapshot['payload']['lines'] if line['view'] in ('both', view)]
    quantum = Decimal(1).scaleb(-MINOR_DIGITS[row['currency']])
    months = [];first_unrounded=Decimal(0);first_rounded=Decimal(0)
    with localcontext(CONTEXT):
        for month in range(1, 37):
            total = Decimal(0);line_amounts={}
            for line in selected:
                if line['period'] == 'one_time':continue
                rule=rules.get(line['id'],{}).get(month,{})
                quantity=decimal(rule.get('quantity',line['quantity']))
                if 'growth_percent' in rule:
                    quantity*=((Decimal(1)+decimal(rule['growth_percent'])/100)**(month-rule['first']))
                if 'tiers' in rule:raw=_tier_cost(quantity,rule['tiers'])
                elif 'block_size' in rule:
                    blocks=(quantity/decimal(rule['block_size'])).to_integral_value(rounding='ROUND_CEILING')
                    raw=blocks*decimal(rule['block_price'])
                else:raw=quantity*decimal(rule.get('unit_rate',line['unit_rate']))
                if line['period'] == 'hourly':raw *= month_hours(snapshot['payload']['period_definition'],month)
                if 'minimum' in rule:raw=max(raw,decimal(rule['minimum']))
                amount = raw.quantize(quantum)
                total += amount
                line_amounts[line['id']]=amount
                if month == 1:
                    first_unrounded+=raw;first_rounded+=amount
                    shown = next(item for item in row['lines'] if item['id'] == line['id'])
                    shown['amount'] = text(amount)
                    shown['assumptions'].append('Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series.')
            for promotion in promotions:
                if not promotion['first']<=month<=promotion['last']:continue
                eligible=sum((line_amounts.get(item,Decimal(0)) for item in promotion['eligible_line_ids']),Decimal(0))
                credit=min(eligible,decimal(promotion['monthly_cap']),pools[promotion['pool_id']]).quantize(quantum)
                pools[promotion['pool_id']]-=credit;total-=credit
                remaining=credit
                for line_id in promotion['eligible_line_ids']:
                    consumed=min(remaining,line_amounts.get(line_id,Decimal(0)))
                    line_amounts[line_id]-=consumed;remaining-=consumed
                    if remaining==0:break
                if month==1 and credit:
                    row['lines'].append({'id':'promo-'+promotion['id'],'resource_id':promotion['eligible_line_ids'][0],
                        'provider':'Declared promotion pool','service':'Eligible credit from '+promotion['pool_id'],
                        'quantity':'1','unit':'month','unit_rate':text(-credit),'currency':row['currency'],
                        'period':'monthly','amount':text(-credit),'source_uri':plan['source_uri'],
                        'evidence_level':'synthetic' if plan['source_uri'].startswith('synthetic://') else 'assumption',
                        'assumptions':['Shared pool '+promotion['pool_id']+' applies once per alternative and is depleted over time.']})
                    first_unrounded-=credit;first_rounded-=credit
            months.append(text(total))
        row['known_monthly_subtotal'] = row['monthly_total'] = months[0]
        row['unrounded_monthly_total'] = text(first_unrounded)
        row['rounding_delta'] = text(first_rounded-first_unrounded)
    return row, months
