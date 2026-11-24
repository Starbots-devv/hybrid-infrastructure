"""Standalone local simulator command; there is no real AWS mode."""
import argparse
import json
from pathlib import Path

from ..io import ValidationError, fail, parse_json
from .journal import canonical_state_dir
from .plan import policy_bytes
from .runner import _persist_rejection, run_simulation, reconcile_simulation
from .transport import InMemorySQS


def main(argv=None):
    parser = argparse.ArgumentParser(prog='sb-aws-sim', description='Synthetic, local SQS simulation only')
    parser.add_argument('--root', required=True, help='Directory containing exact reviewed artifacts')
    parser.add_argument('--plan', required=True)
    parser.add_argument('--approval', required=True)
    parser.add_argument('--evaluation', required=True)
    parser.add_argument('--assessment', required=True)
    parser.add_argument('--state-dir', default=str(canonical_state_dir()), help='Canonical installation-local state directory')
    parser.add_argument('--trust-public-key', required=True, help='Raw 32-byte Ed25519 TEST public key')
    parser.add_argument('--trust-key-id', required=True)
    parser.add_argument('--runner-digest', required=True)
    parser.add_argument('--review-receipt-sha256', required=True, help='Independently supplied security assessment digest')
    parser.add_argument('--as-of', required=True, help='Explicit UTC clock for local reproduction')
    parser.add_argument('--mode', default='PLAN', help='PLAN only; APPLY_AWS is always denied')
    parser.add_argument('--revoked-key-id', action='append', default=[])
    parser.add_argument('--recover-only', action='store_true', help='Read-only reconciliation of a consumed approval')
    args = parser.parse_args(argv)
    try:
        if args.mode != 'PLAN':
            denied = ValidationError('MODE_DENIED', 'APPLY_AWS is unavailable in this package')
            _persist_rejection(root=args.root,plan_path=args.plan,approval_path=args.approval,
                               as_of=args.as_of,error=denied)
            raise denied
        key_path = Path(args.trust_public_key)
        key = key_path.read_bytes()
        if len(key) != 32:
            fail('UNTRUSTED_SIGNER', 'Expected a raw 32-byte Ed25519 test public key')
        policy = parse_json(policy_bytes())
        transport = InMemorySQS(account_id=policy['account_id'], region=policy['region'])
        runner = reconcile_simulation if args.recover_only else run_simulation
        result = runner(root=args.root,plan_path=args.plan,approval_path=args.approval,
            evaluation_path=args.evaluation,assessment_path=args.assessment,
            trust_keys={args.trust_key_id:key},revoked_key_ids=set(args.revoked_key_id),
            runner_digest=args.runner_digest,as_of=args.as_of,transport=transport,
            state_dir=args.state_dir,mode=args.mode,
            trusted_assessment_digest=args.review_receipt_sha256)
        print(json.dumps(result,sort_keys=True))
        return 0
    except (ValidationError, OSError) as exc:
        code = exc.code if isinstance(exc,ValidationError) else 'LOCAL_IO_ERROR'
        print(json.dumps({'execution_kind':'SIMULATED','state':'rejected','error':code}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
