"""Deterministic local analysis, with no execution or cloud client."""
from . import capacity, economics, finops, intake, scenarios
from .contracts import envelope, validate, timestamp
from .io import digest, fail, json_bytes

TITLES=['Decision brief','Company and goals','Current infrastructure','Alternatives and constraints','Recommended architecture','Capacity and service objectives','Costs and accounting','Savings and recovery','Connections and trust boundaries','Implementation procedure','Migration and rollback','Operations and security','Evidence, limitations and approvals']

def _sensitivity(comparisons, baseline_id):
    """Exact one-variable cost perturbation that erases each modeled net result."""
    rows=[]
    for comparison in comparisons:
        if comparison['scenario_id']==baseline_id:
            continue
        for months in (12,36):
            variable=f"{comparison['scenario_id']} / {comparison['view']} / {months} months"
            net_text=comparison[f'net_{months}_months']
            if not comparison['comparable'] or net_text is None:
                condition='Costs are incomplete or incomparable under the declared accounting basis.'
                effect='No numeric cost-perturbation threshold can be derived.'
            else:
                net=economics.decimal(net_text)
                if net>0:
                    condition=(f"If proposal cost increases by {comparison['currency']} "
                               f"{format(net,'f')} over {months} months with other assumptions fixed.")
                    effect='Modeled net saving reaches zero; this is a threshold, not a probability.'
                elif net<0:
                    condition=(f"If proposal cost decreases by {comparison['currency']} "
                               f"{format(-net,'f')} over {months} months with other assumptions fixed.")
                    effect='Modeled net loss reaches zero; this is a threshold, not a probability.'
                else:
                    condition='At the declared costs, the modeled net result is zero.'
                    effect='Any additional proposal cost creates a net loss.'
            rows.append(dict(variable=variable,condition=condition,effect=effect))
    rows.append(dict(variable='Arrival rate or service time',
                     condition='Demand exceeds min(slots, memory slots) / service time',
                     effect='Queue can grow without bound; capacity validation fails.'))
    return rows


def analyze(bundle_path,*,as_of,policy='offline-demo-1.0.0',locale='en'):
    timestamp(as_of)
    if policy not in ('offline-demo-1.0.0','strict-analysis-1.0.0') or locale not in ('en','es'):fail('INVALID_SCHEMA','Unsupported policy or locale')
    data=intake.load_bundle(bundle_path);profile=data['profile'];b=data['bundle']
    if len(profile['payload']['workloads'])!=1:fail('UNSUPPORTED_FEATURE','This release models one explicit steady-state workload')
    if policy=='offline-demo-1.0.0' and not profile['payload']['synthetic']:fail('INVALID_SCHEMA','Demo policy requires explicitly synthetic requirements')
    costs=[];capacities=[];feasibility=[];economy=[];monthly={}
    for s,ref in zip(data['scenarios'],b['scenarios']):
        validate(s,as_of=as_of)
        c=capacity.assess(profile,s,ref['sha256'],policy);capacities.append(c)
        feasibility.append(scenarios.evaluate(profile,s,c,policy))
        for view in ('incremental_cash','allocated_tco'):
            if s['id'] in data['finops']:
                cost,series=finops.calculate_series(data['prices'][s['id']],s['id'],view,as_of,data['finops'][s['id']])
                monthly[(s['id'],view)]=series
            else:cost=economics.calculate_cost(data['prices'][s['id']],s['id'],view,as_of)
            costs.append(cost)
    validate(profile,as_of=as_of)
    for c in costs:
        base=next(x for x in costs if x['scenario_id']==b['baseline_id'] and x['view']==c['view'])
        series_kwargs=({'baseline_series':monthly[(b['baseline_id'],c['view'])],
                        'proposed_series':monthly[(c['scenario_id'],c['view'])]} if monthly else {})
        economy.append(economics.compare(base,c,baseline_id=b['baseline_id'],scenario_id=c['scenario_id'],**series_kwargs))
    candidates=[];horizon=profile['payload']['commercial']['horizon_months'];budget=profile['payload']['commercial']['monthly_budget']
    for f in feasibility:
        # Missing security remains mandatory UNKNOWN: this provisional shortlist is never a feasible approval.
        if any(x['mandatory'] and x['state']!='PASS' and not (x['id']=='verified-security' and x['state']=='UNKNOWN') for x in f['constraints']):continue
        rows=[x for x in costs if x['scenario_id']==f['scenario_id']]
        comparisons=[x for x in economy if x['scenario_id']==f['scenario_id']]
        if not all(x['complete'] for x in rows) or not all(x['comparable'] for x in comparisons):continue
        cash=next(x for x in rows if x['view']=='incremental_cash')
        if cash['currency']!=profile['payload']['commercial']['currency']:continue
        if budget is not None:
            cash_compare=next(x for x in comparisons if x['view']=='incremental_cash')
            if any(economics.decimal(point['proposed'])>economics.decimal(budget) for point in cash_compare['monthly_series'][:horizon]):continue
        tco=next(x for x in rows if x['view']=='allocated_tco')
        tco_compare=next(x for x in comparisons if x['view']=='allocated_tco')
        with economics.localcontext(economics.CONTEXT):
            score=sum((economics.decimal(point['proposed']) for point in tco_compare['monthly_series'][:horizon]),economics.Decimal(0))+economics.decimal(tco['one_time_total'])
        candidates.append((score,f['scenario_id']))
    selected=min(candidates)[1] if candidates else None
    missing=['No complete, independently verified security assessment is bound to this exact bundle.']
    limitations=['Synthetic rates and service times are explicit modeling inputs, not vendor quotes or measured benchmarks.','No deployment, provider lookup, credentials or execution approval is provided.','FinOps plan overrides are explicit and hash-bound when present; absent a plan, demand and prices remain constant. Tax is pre-tax UNKNOWN.','One workload and one cost snapshot per scenario, one currency per view.','Sensitivity is a deterministic single-variable cost threshold, not a probability distribution or market forecast.','Security and recovery objectives require separate exact-subject verification.','English dossier text is implemented; locale metadata does not translate imported or generated prose.']
    recommendation=dict(status='CONDITIONAL' if selected else 'NONE',scenario_id=selected,reasons=['Lowest allocated TCO over the requested horizon among model-compatible, budget-compatible alternatives.' if selected else 'No alternative satisfies the provisional model and comparable-cost conditions.','Mandatory security remains UNKNOWN; no scenario is demonstrated feasible.'],confidence='low',confidence_rationale='Synthetic assumptions, untested restoration, and missing security evidence limit confidence.')
    payload=dict(input_manifest=data['artifacts'],as_of=as_of,policy=policy,locale=locale,synthetic=profile['payload']['synthetic'],profile=profile,scenarios=data['scenarios'],security_assessment_refs=[],missing_security_reasons=missing,capacities=capacities,costs=costs,feasibility=feasibility,comparable_economics=economy,recommendation=recommendation,savings_state='ESTIMATED',sensitivity=_sensitivity(economy,b['baseline_id']),dossier_sections=[dict(id=i,title=t,paragraphs=[]) for i,t in enumerate(TITLES,1)],evidence_manifest=data['artifacts'],execution_eligibility=dict(eligible=False,reasons=['ANALYZE only; independent evidence and future approval gates are pending.'],supported_mode='ANALYZE'),open_questions=profile['payload']['open_questions'],limitations=limitations)
    result=envelope('EvaluationResult','evaluation-'+digest(json_bytes(payload))[:16],payload,client_id=b['client_id'],project_id=b['project_id'],created_at=as_of)
    from .dossier import populate
    result=populate(result);result['id']='evaluation-'+digest(json_bytes(result['payload']))[:16]
    validate(result,expected_kind='EvaluationResult');return result
