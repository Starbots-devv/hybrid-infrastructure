"""One typed result feeds every dossier view. Renderers do not calculate prices."""
from copy import deepcopy
from .contracts import validate
from .io import json_bytes

TITLES=['Executive decision','Context and evidence','Alternatives and rejects','Current and proposed architecture','Resource bill','Connection matrix','Capacity and service objectives','Economics and recovery','Security and continuity','Ordered implementation','Migration and rollback','Operations','Evidence, approval and acceptance']

def populate(result):
    validate(result,expected_kind='EvaluationResult');r=deepcopy(result);p=r['payload'];rec=p['recommendation'];company=p['profile']['payload']['company_name']
    dynamic=any(item['role']=='finops-plan' for item in p['input_manifest'])
    paragraphs={1:[company+' — '+rec['status']+' recommendation: '+(rec['scenario_id'] or 'none')+'. Savings are ESTIMATED.',*rec['reasons']],2:[*p['profile']['payload']['goals'],'All demo facts and rates are synthetic assumptions; evidence and open questions remain explicit.'],3:[f['scenario_id']+': '+f['state']+'. '+', '.join(f['reasons']) for f in p['feasibility']],4:['Diagrams show declared nodes and directed edges. They do not prove availability, compatibility or live connectivity.','Failure domains sharing power or uplink have no demonstrated independence.'],5:['Each declared resource is listed with owner, quantity and region. A resource without a priced line is explicitly identified; this is an exclusion, not a zero-cost claim.'],6:['Required DNS, identities, secrets, TLS roots and routes remain inputs. No connection test has been executed; missing inputs block implementation.'],7:['Capacity is a steady-state analytical hypothesis. It predicts neither concurrent users nor latency percentiles.','Trigger: stop rollout when arrival rate exceeds modeled service capacity, a connection limit is reached, or queue age breaches the approved objective.'],8:['All views are derived from the canonical cost rows and series. Cash excludes allocated depreciation; TCO includes it.','Migration/training is one-time investment; already owned hardware has no upfront purchase in this example. '+('Hash-bound monthly FinOps assumptions produce the 36-month series.' if dynamic else 'Constant prices and demand are assumed.')],9:[*p['missing_security_reasons'],'Backup configuration is not proof of restoration. RTO/RPO, retention, encryption, scoped identities and fallback need independent evidence.'],10:['Steps are a reviewed design procedure requiring actual accounts, hostnames, versions and separate approval. No command here deploys infrastructure.','Owner, prerequisites, required inputs, expected result, validation and stop conditions apply before each step.'],11:['Preserve accepted writes and idempotent event IDs. Reconcile state before reopening traffic; reverting a process alone is insufficient.'],12:['The platform engineer reviews queue age, errors, DB connections and backup freshness daily; reconciles costs weekly and reviews patches and restore evidence monthly.','Alert thresholds and on-call coverage require customer approval. Fallback capacity and its budget are unverified.'],13:[*p['limitations'],'Acceptance requires measured load and outage tests, successful restore within RTO/RPO, dated complete prices, independent exact-subject security review, and customer/engineering/finance approvals.','This dossier grants no execution authority. Input hashes provide integrity, not authenticity or approval.']}
    for e in p['comparable_economics']:
        if e['scenario_id']==rec['scenario_id']:
            paragraphs[1].append(f"{e['view']}: monthly saving {e['monthly_saving']} {e['currency']}; net12 {e['net_12_months']}; net36 {e['net_36_months']}; investment {e['incremental_investment']}; recovery month {e['break_even_month']}.")
    p['dossier_sections']=[dict(id=i,title=t,paragraphs=paragraphs[i]) for i,t in enumerate(TITLES,1)]
    validate(r);return r

def display(value):
    if value is None:return 'UNKNOWN — required input or evidence'
    if isinstance(value,bool):return str(value).lower()
    if isinstance(value,list):return '; '.join(display(v) for v in value) or 'None declared'
    if isinstance(value,dict):return '; '.join(k+': '+display(v) for k,v in sorted(value.items()))
    return str(value)

def tables(result):
    """Semantic table rows shared by Markdown and HTML; no financial arithmetic."""
    p=result['payload'];groups={i:[] for i in range(1,14)}
    def add(section,title,headers,rows):groups[section].append((title,headers,[[display(c) for c in row] for row in rows]))
    profile=p['profile']['payload']
    add(2,'Business profile',['Field','Value'],[(k,v) for k,v in sorted(profile.items()) if k not in ('inventory','workloads','service_objectives','open_questions')])
    add(2,'Workload inputs',['Field','Value'],[(w['id']+' / '+k,v) for w in profile['workloads'] for k,v in sorted(w.items())])
    for f in p['feasibility']:add(3,f['scenario_id']+' — '+f['state'],['ID / dimension','Rule target / observation','State / mandatory','Evidence / rationale'],[(c['id']+' / '+c['dimension'],display(c['threshold'])+' / '+display(c['actual']),c['state']+' / '+str(c['mandatory']),c['evidence_level']+' / '+c['rationale']) for c in f['constraints']])
    for s in p['scenarios']:
        sid=s['id'];sp=s['payload'];priced={l['resource_id'] for c in p['costs'] if c['scenario_id']==sid for l in c['lines']}
        add(4,sid+' trust and failure domains',['Field','Value'],[('Trust boundaries',sp['trust_boundaries']),('Failure domains',sp['failure_domains']),('Actions',sp['action_groups'])])
        add(5,sid+' resource bill',['ID / service','Provider / region','Size / quantity','Owner / allocation'],[(n['id']+' / '+n['service'],n['provider']+' / '+n['region'],n['size']+' / '+n['quantity'],n['owner']+' / '+('priced' if n['id'] in priced else 'No separate line: cost assumed included in compute; verify completeness')) for n in sp['resource_nodes']])
        for e in sp['connection_edges']:add(6,sid+' / '+e['id'],['Connection field','Required design / validation'],[(k,v) for k,v in sorted(e.items())])
        if sid==p['recommendation']['scenario_id']:
            for step in sp['implementation_steps']:add(10,sid+' / '+step['id'],['Step field','Procedure'],[(k.replace('_',' ').capitalize(),v) for k,v in sorted(step.items())])
            add(11,sid+' migration and rollback',['Field','Procedure'],[(k.replace('_',' ').capitalize(),v) for k,v in sorted(sp['migration_rollback'].items())])
        add(12,sid+' operating model',['Field','Value'],[(k.replace('_',' ').capitalize(),v) for k,v in sorted(sp['operational_model'].items())])
    for c in p['capacities']:add(7,c['scenario_id']+' capacity',['Field','Value'],[(k,v) for k,v in sorted(c.items())])
    for c in p['costs']:
        add(8,c['scenario_id']+' / '+c['view']+' totals',['Field','Value'],[(k,v) for k,v in sorted(c.items()) if k!='lines'])
        add(8,c['scenario_id']+' / '+c['view']+' cost lines',['Row ID','Resource / service','Quantity / rate / unit','Amount / currency','Source / evidence'],[('|'.join([c['scenario_id'],c['view'],l['id'],l['period']]),l['resource_id']+' / '+l['service'],l['quantity']+' / '+display(l['unit_rate'])+' / '+l['unit'],display(l['amount'])+' / '+c['currency'],l['source_uri']+' / '+l['evidence_level']+' / '+display(l['assumptions'])) for l in c['lines']])
    add(8,'Comparable monthly economics',['Scenario / view','Month 1 saving','Net12 / net36','Investment / recovery','Comparability'],[(e['scenario_id']+' / '+e['view'],display(e['monthly_saving'])+' '+e['currency'],display(e['net_12_months'])+' / '+display(e['net_36_months']),display(e['incremental_investment'])+' / '+display(e['break_even_month']),str(e['comparable'])+' / '+display(e['reasons'])) for e in p['comparable_economics']])
    for comparison in p['comparable_economics']:
        add(8,comparison['scenario_id']+' / '+comparison['view']+' monthly series',['Month','Baseline','Proposed','Saving','Cumulative net'],[(f"Month {point['month']}",point['baseline'],point['proposed'],point['saving'],point['cumulative_net']) for point in comparison['monthly_series']])
    add(8,'Sensitivity',['Variable','Condition','Effect'],[(x['variable'],x['condition'],x['effect']) for x in p['sensitivity']])
    add(9,'Security coverage',['Area','State'],[('Exact-subject assessment','MISSING; no real scanner has run'),('Capacity benchmark / restore test','MISSING'),('Execution eligibility',p['execution_eligibility'])])
    add(13,'Open questions',['ID','Question','Owner / required by'],[(q['id'],q['question'],q['owner']+' / '+q['required_by']) for q in p['open_questions']])
    add(13,'Input evidence manifest',['Role','Path','SHA-256'],[(a['role'],a['path'],a['sha256']) for a in p['input_manifest']])
    add(13,'Run provenance',['Field','Value'],[('Evaluation ID',result['id']),('Producer',result['producer']),('As of',p['as_of']),('Policy',p['policy']),('Client / project',result['client_id']+' / '+result['project_id']),('Confidence',p['recommendation']['confidence']+' / '+p['recommendation']['confidence_rationale'])])
    return groups

def render(result):
    from .renderers import markdown, html, csv, svg
    validate(result,expected_kind='EvaluationResult');p=result['payload'];groups=tables(result)
    baseline_id=p['comparable_economics'][0]['baseline_id']
    baseline=next(s for s in p['scenarios'] if s['id']==baseline_id)
    selected=next((s for s in p['scenarios'] if s['id']==p['recommendation']['scenario_id']),None)
    diagrams={'architecture-current.svg':svg.render(baseline),'architecture-proposed.svg':svg.render(selected)}
    out={**diagrams,'dossier.md':markdown.render(result,groups),'dossier.html':html.render(result,groups,diagrams),'costs.csv':csv.render(result),'cashflow.csv':csv.cashflow(result),'executive-summary.md':markdown.render(result,groups,sections=[1,3,8,9,13],executive=True),'implementation-guide.md':markdown.render(result,groups,sections=[4,5,6,7,8,9,10,11,12,13])}
    # Shareable output has a small fixed allowlist: no names, IDs, paths, free text or imported labels.
    out['shareable-summary.html']=html.shareable(result)
    out['redaction-manifest.json']=json_bytes(dict(version='1.0.0',policy='summary-allowlist-1',retained_fields=['synthetic','recommendation.status','economics numeric values and supported currency'],omitted_categories=['client and project identifiers','company and scenario names','resource names and locations','input paths and hashes','free text','connection and secret references','implementation details'],limitations=['Commercial totals remain potentially sensitive; review before sharing.','No anonymity guarantee; no automatic publication.']))
    return out
