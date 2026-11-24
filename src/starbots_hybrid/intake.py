"""Manual local bundle import. Sealing is integrity, never approval."""
from pathlib import Path
import re
from .contracts import validate, protocol_digest
from .io import digest, fail, json_bytes, load_json, read_bytes, verify_ref, write_json

KEYS={'schema_version','client_id','project_id','profile','scenarios','baseline_id','security_assessments'}
FINOPS_KEYS=KEYS|{'finops'}

def _shape(bundle):
    if not isinstance(bundle,dict) or not ((set(bundle)==KEYS and bundle.get('schema_version')=='1.0.0') or (set(bundle)==FINOPS_KEYS and bundle.get('schema_version')=='1.1.0')):fail('INVALID_SCHEMA','Unsupported closed input-bundle structure')
    if not isinstance(bundle['scenarios'],list) or not 1<=len(bundle['scenarios'])<=30:fail('RESOURCE_LIMIT','Provide between 1 and 30 scenarios')
    if any(not isinstance(bundle[k],str) or not re.fullmatch('[A-Za-z0-9_-]{1,64}',bundle[k]) for k in ('client_id','project_id','baseline_id')):fail('INVALID_SCHEMA','Invalid bundle identity')
    if not isinstance(bundle['security_assessments'],list):fail('INVALID_SCHEMA','Assessment references must be an array')
    for ref in [bundle['profile'],*bundle['scenarios']]:
        if not isinstance(ref,dict) or set(ref)!={'path','sha256'}:fail('INVALID_SCHEMA','Expected a bounded artifact reference')
        if not isinstance(ref['path'],str) or not isinstance(ref['sha256'],str) or not re.fullmatch('[a-f0-9]{64}',ref['sha256']):fail('INVALID_SCHEMA','Invalid artifact reference types or hash')
    if bundle['security_assessments']:fail('UNSUPPORTED_FEATURE','Embedded scanner assessments are not supported in bundles; use exact-subject verification separately')
    if bundle['schema_version']=='1.1.0':
        if not isinstance(bundle['finops'],dict) or len(bundle['finops'])!=len(bundle['scenarios']):fail('INVALID_SCHEMA','Each scenario requires one FinOps plan')
        for scenario_id,ref in bundle['finops'].items():
            if not isinstance(scenario_id,str) or not re.fullmatch('[A-Za-z0-9_-]{1,64}',scenario_id):fail('INVALID_SCHEMA','Invalid FinOps scenario ID')
            if not isinstance(ref,dict) or set(ref)!={'path','sha256'} or not isinstance(ref['path'],str) or not isinstance(ref['sha256'],str) or not re.fullmatch('[a-f0-9]{64}',ref['sha256']):fail('INVALID_SCHEMA','Invalid FinOps artifact reference')

def _document(root,ref,bundle,kind,verify=True):
    raw=verify_ref(root,ref) if verify else read_bytes(root,ref['path'])
    from .io import parse_json
    d=parse_json(raw)
    validate(d,expected_kind=kind,client_id=bundle['client_id'],project_id=bundle['project_id'])
    return d,raw

def seal_bundle(path):
    path=Path(path).absolute();root=path.parent
    _root(root);b=load_json(root,path.name);_shape(b)
    _,raw=_document(root,b['profile'],b,'WorkloadProfile',False);b['profile']['sha256']=digest(raw)
    for ref in b['scenarios']:
        scenario,_=_document(root,ref,b,'Scenario',False)
        scenario['payload']['required_capacity_profile_digest']=b['profile']['sha256']
        scenario['payload']['required_security_profile_digest']=protocol_digest()
        for price_ref in scenario['payload']['input_cost_snapshot_refs']:
            _,raw=_document(root,price_ref,b,'CostSnapshot',False);price_ref['sha256']=digest(raw)
        # Explicitly regenerate only content hashes. No assessment, signature or approval is produced.
        write_json(root,ref['path'],scenario);ref['sha256']=digest(json_bytes(scenario))
    if b['schema_version']=='1.1.0':
        for ref in b['finops'].values():ref['sha256']=digest(read_bytes(root,ref['path']))
    write_json(root,path.name,b)
    return b

def load_bundle(path):
    path=Path(path).absolute();root=path.parent
    _root(root);b=load_json(root,path.name);_shape(b)
    bundle_raw=read_bytes(root,path.name)
    profile,raw=_document(root,b['profile'],b,'WorkloadProfile');artifacts=[{'role':'input-bundle','path':path.name,'sha256':digest(bundle_raw)},{'role':'profile',**b['profile']}];copies={path.name:bundle_raw,b['profile']['path']:raw}
    if (profile['payload']['current_system'] is None)!=profile['payload']['new_system']:fail('INVALID_SCHEMA','Declare either a new system or the current system')
    scenarios=[];prices={};plans={};seen_ids=set();total=len(raw)+len(bundle_raw)
    for ref in b['scenarios']:
        scenario,raw=_document(root,ref,b,'Scenario')
        if scenario['id'] in seen_ids:fail('INVALID_SCHEMA','Duplicate scenario ID')
        seen_ids.add(scenario['id']);scenarios.append(scenario);artifacts.append({'role':'scenario',**ref});copies[ref['path']]=raw;total+=len(raw)
        p=scenario['payload'];nodes={n['id'] for n in p['resource_nodes']}
        if p['required_capacity_profile_digest']!=b['profile']['sha256'] or p['required_security_profile_digest']!=protocol_digest():fail('HASH_MISMATCH','Scenario profile binding differs from the imported requirements or security protocol')
        for edge in p['connection_edges']:
            if edge['source'] not in nodes or edge['destination'] not in nodes:fail('INVALID_SCHEMA','Connection references an unknown resource')
        if len({g['resource_id'] for g in p['action_groups']})!=len(p['action_groups']):fail('INCOMPATIBLE_ACTIONS','A resource cannot appear in multiple action groups')
        for group in p['action_groups']:
            if group['resource_id'] not in nodes or len(group['actions'])!=1:fail('INCOMPATIBLE_ACTIONS','Use one non-overlapping action per resource')
        if len(p['input_cost_snapshot_refs'])!=1:fail('UNSUPPORTED_FEATURE','Exactly one explicit complete snapshot per scenario is supported')
        price_ref=p['input_cost_snapshot_refs'][0];price,raw=_document(root,price_ref,b,'CostSnapshot')
        if any(l['resource_id'] not in nodes for l in price['payload']['lines']):fail('INVALID_SCHEMA','Cost references an unknown resource')
        prices[scenario['id']]=price;copies[price_ref['path']]=raw;total+=len(raw)
        artifacts.append({'role':'prices',**price_ref})
        if b['schema_version']=='1.1.0':
            plan_ref=b['finops'].get(scenario['id'])
            if plan_ref is None:fail('INVALID_SCHEMA','Scenario FinOps plan is missing')
            plan_raw=verify_ref(root,plan_ref)
            from .io import parse_json
            plans[scenario['id']]=parse_json(plan_raw)
            copies[plan_ref['path']]=plan_raw;total+=len(plan_raw)
            artifacts.append({'role':'finops-plan',**plan_ref})
    if b['baseline_id'] not in seen_ids:fail('INVALID_SCHEMA','Baseline scenario is missing')
    if next(s for s in scenarios if s['id']==b['baseline_id'])['payload']['type']!='current':fail('INVALID_SCHEMA','The comparison baseline must be current')
    baseline_period=prices[b['baseline_id']]['payload']['period_definition']
    if any(p['payload']['period_definition']!=baseline_period for p in prices.values()):fail('INCOMPARABLE_COSTS','Cost periods and horizons must match explicitly')
    if len(copies)>1000 or total>100*1024*1024:fail('RESOURCE_LIMIT','Bundle exceeds file or byte limit')
    unique={a['path']:a for a in artifacts}
    if len(unique)!=len(artifacts):fail('INVALID_SCHEMA','Input paths may not be reused under multiple roles')
    if b['schema_version']=='1.1.0' and set(b['finops'])!=seen_ids:fail('INVALID_SCHEMA','FinOps plans do not match scenario IDs')
    return {'root':root,'bundle':b,'profile':profile,'scenarios':scenarios,'prices':prices,'finops':plans,'artifacts':list(unique.values()),'copies':copies}

def _root(root):
    for directory in (root,*root.parents):
        if directory.is_symlink() or directory.is_junction():fail('PATH_DENIED','Input root cannot traverse a link or junction')
