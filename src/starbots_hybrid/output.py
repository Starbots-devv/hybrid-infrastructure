"""Fresh-directory exports with exact-byte subject manifests."""
from pathlib import Path
import re
from .contracts import DATA, envelope, validate
from .io import digest, fail, json_bytes, load_json, verify_ref, verify_subject, write_bytes, write_json

def checked_root(path):
    root=Path(path).absolute()
    for p in (root,*root.parents):
        if p.is_symlink() or p.is_junction():fail('PATH_DENIED','Output roots cannot traverse a link or junction')
    if root.exists() and (not root.is_dir() or any(root.iterdir())):fail('PATH_DENIED','Choose a fresh output directory; existing artifacts are never overwritten')
    return root

def export_analysis(data,result,output_dir,render=None):
    if result['payload']['input_manifest']!=data['artifacts']:fail('HASH_MISMATCH','Inputs changed after analysis; rerun against one reviewed bundle')
    root=checked_root(output_dir)
    rendered=render(result) if render else {}
    if root.resolve()==data['root'].resolve() or data['root'].resolve().is_relative_to(root.resolve()):fail('PATH_DENIED','Output must not contain the input root')
    artifacts=[]
    def add(name,raw,role):
        write_bytes(root,name,raw);artifacts.append(dict(role=role,path=name,sha256=digest(raw)))
    for name,raw in data['copies'].items():add('inputs/'+name,raw,'input')
    for c in result['payload']['capacities']:
        capacity=envelope('CapacityAssessment','capacity-'+digest(c['scenario_id'].encode())[:16],c,client_id=result['client_id'],project_id=result['project_id'],created_at=result['created_at'])
        validate(capacity);add('capacity-'+c['scenario_id']+'.json',json_bytes(capacity),'capacity')
    add('security-control-profile.json',DATA.joinpath('protocol','1.0.0','control-profile.json').read_bytes(),'security-control-profile')
    identity=dict(revision='1',client_id=result['client_id'],project_id=result['project_id'],artifacts=list(artifacts))
    subject_id='proposal-'+digest(json_bytes(identity))[:32]
    manifest=dict(subject_id=subject_id,**identity)
    write_json(root,'subject-manifest.json',manifest)
    subject=envelope('SubjectRef','subject-'+subject_id,dict(subject_id=subject_id,revision='1',manifest_path='subject-manifest.json',manifest_sha256=digest(json_bytes(manifest)),artifacts=list(artifacts)),client_id=result['client_id'],project_id=result['project_id'],created_at=result['created_at'])
    validate(subject);write_json(root,'subject.json',subject)
    verify_subject(root,subject,client_id=result['client_id'],project_id=result['project_id'])
    add('subject-manifest.json',json_bytes(manifest),'subject-manifest')
    add('subject.json',json_bytes(subject),'subject-reference')
    add('evaluation.json',json_bytes(result),'evaluation')
    for name,raw in rendered.items():add(name,raw,'dossier')
    write_json(root,'artifact-manifest.json',dict(report_id=result['id'],artifacts=artifacts))
    return root

def verify_report(root):
    manifest=load_json(root,'artifact-manifest.json')
    if not isinstance(manifest,dict) or set(manifest)!={'report_id','artifacts'} or not isinstance(manifest['artifacts'],list) or len(manifest['artifacts'])>1000:fail('INVALID_SCHEMA','Invalid report manifest')
    seen=set();total=0
    for ref in manifest['artifacts']:
        if not isinstance(ref,dict) or set(ref)!={'role','path','sha256'} or any(not isinstance(ref[k],str) for k in ('role','path','sha256')):fail('INVALID_SCHEMA','Invalid report artifact types')
        if ref['path'] in seen or not re.fullmatch('[a-f0-9]{64}',ref['sha256']):fail('INVALID_SCHEMA','Invalid or duplicate report artifact')
        seen.add(ref['path']);total+=len(verify_ref(root,ref))
        if total>100*1024*1024:fail('RESOURCE_LIMIT','Report exceeds byte limit')
    if 'evaluation.json' not in seen:fail('INVALID_SCHEMA','Evaluation is missing from report manifest')
    evaluation=load_json(root,'evaluation.json');validate(evaluation,expected_kind='EvaluationResult')
    if manifest['report_id']!=evaluation['id']:fail('IDENTITY_MISMATCH','Report identity differs from evaluation')
    return evaluation
