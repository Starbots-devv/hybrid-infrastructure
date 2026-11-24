"""Conservative queue-service model. A model is never a measured benchmark."""
from decimal import Decimal, localcontext
from .economics import CONTEXT, decimal, text

def assess(profile, scenario, scenario_sha256, policy):
    p=scenario['payload'];c=p['capacity_inputs'];w=profile['payload']['workloads'][0]
    target=w['arrival_rate_per_second'];capacity=None;headroom=None;limits=[];checks=[]
    def check(id,actual,threshold,ok):
        state='UNKNOWN' if ok is None else ('PASS' if ok else 'FAIL')
        checks.append(dict(id=id,dimension='capacity',mandatory=True,state=state,actual=actual,threshold=threshold,rationale='Analytical synthetic model only; benchmark and load test required',evidence_level=c['evidence_level']))
    with localcontext(CONTEXT):
        keys=('parallel_slots','available_memory_gib','required_memory_per_job_gib','service_time_seconds')
        if all(c[k] is not None for k in keys) and decimal(c['service_time_seconds'])>0 and decimal(c['required_memory_per_job_gib'])>0:
            slots=min(decimal(c['parallel_slots']),decimal(c['available_memory_gib'])//decimal(c['required_memory_per_job_gib']))
            capacity=slots/decimal(c['service_time_seconds'])
            if target is not None and capacity>0:headroom=(capacity-decimal(target))/capacity*100
        strict=policy=='strict-analysis-1.0.0'
        # This release deliberately has no measured-benchmark verifier. A caller label or hash alone cannot promote it.
        check('model-throughput',text(capacity) if capacity is not None else None,target,None if strict or capacity is None or target is None else capacity>=decimal(target))
        for id,available,required in [('model-db-connections',c['max_db_connections'],c['required_connections']),('model-network',c['network_capacity_mbps'],c['target_network_mbps'])]:
            check(id,available,required,None if strict or available is None or required is None else decimal(available)>=decimal(required))
    limits.extend(['No measured throughput, latency percentile, queue-drain or restore test is supplied.','Correlated power/network failures and cloud fallback capacity need independent tests.','Single workload, steady arrival rate and equal service times; no users-to-RPS conversion.'])
    return dict(scenario_id=scenario['id'],scenario_sha256=scenario_sha256,demand_case=p['demand_case'],configuration='Declared parallel slots, memory, database connections and network ceilings',target_load_rps=target,estimated_capacity_rps=text(capacity) if capacity is not None else None,measured_or_estimated='estimated' if capacity is not None else 'unknown',method='min(parallel slots, floor(memory / memory per job)) / service time',evidence_refs=[],assumptions=c['assumptions'],headroom_percent=text(headroom) if headroom is not None else None,bottlenecks=[x['id'] for x in checks if x['state']!='PASS'],limits=limits,critical_paths=['worker -> durable queue -> managed database'],failure_domains=p['failure_domains'],recovery_objectives=profile['payload']['service_objectives'],restoration_test_refs=[],constraint_results=checks)
