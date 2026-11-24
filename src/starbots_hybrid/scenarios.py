"""Mandatory constraints cannot be traded against a cheaper price."""
from .economics import decimal
from .io import fail

def requirements(profile, scenario):
    p=profile['payload'];declared={x['id']:x for x in scenario['payload']['constraint_requirements']}
    for slo in p['service_objectives']:
        r=declared.get(slo['id'])
        if r is None or not r['mandatory'] or (r['dimension'],r['threshold'],r['rule'])!=(slo['indicator'],slo['target'],slo['acceptance_condition']):
            fail('REQUIREMENT_MISMATCH','Scenario omitted or changed a mandatory profile objective: '+slo['id'])
    for region in p['data_policy']['residency']:
        if not any(r['mandatory'] and r['dimension']=='residency' and r['rule']=='includes' and r['threshold']==region for r in declared.values()):
            fail('REQUIREMENT_MISMATCH','Scenario omitted mandatory data residency')
    return list(declared.values())

def evaluate(profile, scenario, capacity, policy):
    checks=[]
    for r in requirements(profile,scenario):
        o=r['observation'];value=o['value'];state='UNKNOWN'
        # Evidence semantics stay conservative: bundles do not import independently verified measured evidence.
        if value is not None and policy=='offline-demo-1.0.0':
            if r['rule']=='equals':ok=type(value) is type(r['threshold']) and value==r['threshold']
            elif r['rule']=='includes':ok=isinstance(value,str) and r['threshold'] in [x.strip() for x in value.split(',')]
            else:
                a,b=decimal(value),decimal(r['threshold']);ok=a<=b if r['rule']=='lte' else a>=b
            state='PASS' if ok else 'FAIL'
        checks.append(dict(id=r['id'],dimension=r['dimension'],mandatory=r['mandatory'],state=state,actual=value,threshold=r['threshold'],rationale=r['rationale']+'; declared observation, not independently verified',evidence_level=o['evidence_level']))
    checks.extend(capacity['constraint_results'])
    checks.append(dict(id='verified-security',dimension='security',mandatory=True,state='UNKNOWN',actual=None,threshold='Exact-subject verified security coverage',rationale='No independently verified exact-subject security review is bound to this analysis',evidence_level='unknown'))
    mandatory=[x for x in checks if x['mandatory']]
    state='INFEASIBLE' if any(x['state']=='FAIL' for x in mandatory) else ('UNDEMONSTRATED' if any(x['state']=='UNKNOWN' for x in mandatory) else 'FEASIBLE')
    return dict(scenario_id=scenario['id'],state=state,constraints=checks,reasons=[x['id']+': '+x['state'] for x in mandatory if x['state']!='PASS'])
