# Local SQS simulation

`sb-aws-sim` is an optional local state machine for one **synthetic** SQS standard queue. It demonstrates how a reviewed change plan, a signed approval and a security review can gate an infrastructure change. It never contacts AWS, reads credentials, imports an AWS SDK or creates a real queue. `ExecutionRecord.execution_kind` is always `SIMULATED`; a `succeeded` record means only that the in-memory queue matched the expected synthetic attributes and tags.

Install the optional dependency first: `pip install --require-hashes -r requirements-simulation.lock`.

## What is simulated

The only simulated mutation is `CreateQueue` with tags supplied in the same call. The pinned policy (`src/starbots_hybrid/data/sqs-simulation-policy.json`) fixes the synthetic account `000000000000`, region `us-east-1`, name prefix `starbots-sandbox-`, SSE-SQS (`SqsManagedSseEnabled=true`), one-day retention and a 30-second visibility timeout. The queue name derives from the plan's idempotency key, and creation tags bind the exact plan, client and transaction ID. Simulated reads are `GetCallerIdentity`, `GetQueueUrl`, `GetQueueAttributes` and `ListQueueTags`, all counted against the signed query budget. There is no deletion, purge, messaging, later tagging, attribute editing, IAM, database, DNS or other provider operation. A mixed plan is rejected.

## Inputs and checks

The simulator consumes a closed `ChangePlan`, a detached `ApprovalEnvelope`, the referenced `EvaluationResult`, a `SecurityAssessment` and the subject manifest with all its artifacts. It hashes exact bytes, validates the versioned contracts, requires the `starbots-local-review` policy with all six mandatory controls and tool runs, and recomputes readiness from the bound evidence. A separately supplied assessment digest must match the exact assessment bytes; it is only an independent receipt when you obtained it through a channel other than the incoming files. The assessment, evaluation and queue baseline must exist before the change plan, and the approval must follow the plan. The plan names one `sqs:CreateQueue` action and an absent baseline observed no more than five minutes before the explicit `--as-of` clock. The security assessment may be at most 24 hours old. Unknown or expired costs or evidence, identity mismatch and drift stop the run before any simulated mutation.

The approval carries a detached Ed25519 signature over the decoded `signed_payload_base64url` bytes. The verifier rejects a changed signature, a missing or revoked public key, mismatched signed fields, scope, hash, runner digest, budget or clock. An approval lives at most 15 minutes. The public key is supplied as a raw 32-byte test key. The runner digest is a consistency marker; the simulator does not attest installed code. The package ships no signer or trust root; the test suite generates ephemeral keys. `EvaluationResult.execution_eligibility.eligible` stays false: a signed local simulation does not override the product's execution block.

```text
sb-aws-sim --root FIXTURE_ROOT --plan plan.json --approval approval.json --evaluation evaluation.json --assessment assessment.json --trust-public-key TEST_PUBLIC_KEY_FILE --trust-key-id TEST_KEY_ID --runner-digest RUNNER_SHA256 --review-receipt-sha256 ASSESSMENT_SHA256 --as-of 2026-10-18T12:00:00Z --mode PLAN
```

`--mode APPLY_AWS` always exits with `MODE_DENIED`; no flag or environment variable enables a real transport, and ambient AWS variables are ignored. The command prints a JSON `ExecutionRecord` for a completed simulation, or a redacted JSON error with exit code 2. Validation failures and `APPLY_AWS` denials also append a contract-valid `SIMULATED` / `rejected` record to a local denial journal that contains input digests and an error code, but no raw plan or client fields. A local I/O or state failure fails closed.

## Recovery and limits

State lives in `.local-evidence/aws-sim-state` under the resolved checkout or virtual-environment root: an account/region lock, a hash-chained journal and hashed audit snapshots. Lock and replay protection apply to one installation, not across machines. An approval ID is consumed once; a second attempt cannot call `CreateQueue` again. If the first call times out, the record is `unknown` before an observed effect or `partial` after one. Repeating with the same approval performs read-only reconciliation and reports `succeeded` only when the queue's exact attributes and transaction tag match. Foreign pre-existing queues, postcondition mismatches and journal corruption fail closed. Nothing is deleted or cleaned up automatically.

The queue itself lives in process memory, so a new process keeps the consumed approval from the journal but cannot reconstruct an uncertain queue effect; such a record stays `unknown` and needs a person to review it. `--recover-only` checks the original signed issue time and can reconcile an expired approval without calling `CreateQueue`; it cannot approve a new mutation. The journal and test key are demonstration controls, not production runner infrastructure. A real deployment would need an isolated runner, operator-owned trust configuration and journal, IAM limits, cost review and AWS-specific validation, none of which are included.
