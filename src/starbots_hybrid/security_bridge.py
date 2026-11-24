"""Independent data-only security attachment verifier. No Security package import."""
from pathlib import Path
import re
from .contracts import validate, verify_assessment
from .io import digest, fail, load_json, read_bytes, verify_subject

def verify_security(review_dir,proposal,assessment_sha256,*,client_id,project_id,as_of):
    # This expected hash must come from the operator's trusted review receipt,
    # never be calculated from the incoming assessment at the trust boundary.
    if not isinstance(assessment_sha256,str) or not re.fullmatch('[a-f0-9]{64}',assessment_sha256):fail('HASH_MISMATCH','A separately trusted SHA-256 is required')
    source=Path(proposal);original=read_bytes(source.parent,source.name);subject=load_json(source.parent,source.name)
    validate(subject,expected_kind='SubjectRef',client_id=client_id,project_id=project_id)
    verify_subject(source.parent,subject,client_id=client_id,project_id=project_id)
    root=Path(review_dir);review_subject=load_json(root,'subject.json')
    validate(review_subject,expected_kind='SubjectRef',client_id=client_id,project_id=project_id)
    linked=[a for a in review_subject['payload']['artifacts'] if a['role']=='proposal-subject']
    if len(linked)!=1 or linked[0]['path']!='proposal/subject.json' or linked[0]['sha256']!=digest(original):fail('HASH_MISMATCH','Review does not reference the exact original proposal')
    if read_bytes(root,linked[0]['path'])!=original:fail('HASH_MISMATCH','Reviewed proposal bytes changed')
    verify_subject(root/'proposal',subject,client_id=client_id,project_id=project_id)
    assessment=verify_assessment(root,dict(path='security-assessment.json',sha256=assessment_sha256),review_subject,as_of=as_of,expected_policy_id='starbots-local-review')
    return dict(valid=True,proposal_manifest_sha256=subject['payload']['manifest_sha256'],assessment_sha256=assessment_sha256,readiness=assessment['payload']['readiness']['state'],execution_eligible=False,scope=assessment['payload']['scope'],trust='Integrity against an operator-supplied digest; no publisher authentication or deployment approval')
