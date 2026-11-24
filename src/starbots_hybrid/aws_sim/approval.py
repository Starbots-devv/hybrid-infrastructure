"""Ed25519 verification of exact detached approval bytes."""
import base64
from decimal import Decimal

from ..contracts import timestamp, validate
from ..io import digest, fail, parse_json, read_bytes

SIGNED_FIELDS = frozenset(('approval_id','plan_sha256','proposal_sha256','assessment_sha256',
    'policy_sha256','runner_sha256','account_id','region','environment','resource_scope',
    'action_allowlist','max_incremental_cost','query_budget','issued_at','expires_at','approver_id'))


def _decode(value):
    if not isinstance(value, str) or not value or '=' in value:
        fail('INVALID_SIGNATURE', 'Invalid base64url encoding')
    try:
        raw = base64.urlsafe_b64decode(value + '=' * (-len(value) % 4))
    except (ValueError, base64.binascii.Error):
        fail('INVALID_SIGNATURE', 'Invalid base64url encoding')
    if base64.urlsafe_b64encode(raw).rstrip(b'=').decode('ascii') != value:
        fail('INVALID_SIGNATURE', 'Noncanonical base64url encoding')
    return raw


def verify_approval(root, approval_path, plan, plan_digest, *, trust_keys, revoked_key_ids, as_of):
    raw = read_bytes(root, approval_path)
    approval = validate(parse_json(raw), expected_kind='ApprovalEnvelope',
                        client_id=plan['client_id'], project_id=plan['project_id'], as_of=as_of)
    p = approval['payload']
    sig = p['signature']
    if sig['key_id'] in revoked_key_ids or sig['key_id'] not in trust_keys:
        fail('UNTRUSTED_SIGNER', 'Approval signer is untrusted or revoked')
    signed_raw = _decode(p['signed_payload_base64url'])
    signed = parse_json(signed_raw)
    if set(signed) != SIGNED_FIELDS or signed != {k:v for k,v in p.items() if k in SIGNED_FIELDS}:
        fail('INVALID_SIGNATURE', 'Signed bytes differ from approval fields')
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        Ed25519PublicKey.from_public_bytes(trust_keys[sig['key_id']]).verify(_decode(sig['value']), signed_raw)
    except ImportError:
        fail('CRYPTO_UNAVAILABLE', 'Reviewed Ed25519 dependency is unavailable')
    except (InvalidSignature, ValueError, TypeError):
        fail('INVALID_SIGNATURE', 'Approval signature is invalid')
    q = plan['payload']
    expected = {'plan_sha256':plan_digest,'proposal_sha256':q['subject_ref']['manifest_sha256'],
                'assessment_sha256':q['security_assessment_digest'],'policy_sha256':q['action_policy_digest'],
                'runner_sha256':q['runner_digest'],'account_id':q['account_id'],'region':q['region'],
                'environment':q['environment'],'resource_scope':q['resources'],
                'action_allowlist':['sqs:CreateQueue']}
    if any(signed[k] != v for k,v in expected.items()):
        fail('APPROVAL_SCOPE', 'Approval does not bind this exact plan and scope')
    now = timestamp(as_of)
    issued, expires = timestamp(signed['issued_at']), timestamp(signed['expires_at'])
    if issued < timestamp(plan['created_at']) or timestamp(approval['created_at']) < timestamp(plan['created_at']):
        fail('EVIDENCE_STALE', 'Approval predates the change plan it signs')
    if issued > now or expires <= now or (expires - issued).total_seconds() > 900 or expires > timestamp(q['expires_at']):
        fail('APPROVAL_EXPIRED', 'Approval clock or lifetime is invalid')
    if Decimal(q['incremental_cost']) > Decimal(signed['max_incremental_cost']) or q['query_budget'] > signed['query_budget']:
        fail('APPROVAL_SCOPE', 'Cost or read budget exceeds signed approval')
    return approval, digest(raw)
