---
name: hybrid-infrastructure
description: Compare a current infrastructure design with user-supplied alternatives (cloud, hybrid, on-premise worker, managed service) offline with the Starbots sb-hybrid CLI and produce a cost and decision dossier with 12/36-month cash and TCO, break-even, capacity and constraint checks. Use when someone asks whether to move, keep or split a workload between cloud and their own hardware, wants hidden costs made explicit, or needs a decision document for a business owner and an engineer. Not for live pricing, provisioning or deployment.
---

# Starbots Hybrid Infrastructure

Use the installed `sb-hybrid` CLI. It reads a local input bundle, never contacts a provider, needs no credentials and never changes infrastructure. Every recommendation it produces is conditional on the inputs, and `execution_eligible` is always false.

## Workflow

1. **Start from an example.** From a checkout of the `hybrid-infrastructure` repository, copy a whole example directory to a new working directory: `examples/hybrid-saving` for one workload with three alternatives, or one of `examples/flows/flow-01`, `flow-02`, `flow-03`. Never edit the examples in place. `docs/usage.md` and `docs/cost-methodology.md` in that repository describe every input field.
2. **Collect facts from the user.** Edit `profile.json` (goals, mandatory service objectives, residency, the single steady-state workload, budget, team, open questions), each `scenario-*.json` (resources, directed connections, constraint observations, capacity inputs, implementation steps, rollback) and each `prices-*.json` cost snapshot (dated rates, currency, period, quantity). Optional `finops-*.json` plans add 36-month growth, tiers, promotions, FX and asset depreciation. Ask for missing numbers instead of inventing them. Decimal values are strings, never JSON floats. A missing rate stays `null`; it is never zero. Keep `synthetic: true` for fictional data and never put real secrets or account identifiers in a bundle.
3. **Seal the bundle** after every edit, so input hashes match the files: `sb-hybrid seal-bundle --bundle <dir>/bundle.json`. Sealing refreshes hashes only; it is not an approval.
4. **Validate:** `sb-hybrid validate --bundle <dir>/bundle.json`.
5. **Analyze** into a new, empty directory with an explicit UTC time (`YYYY-MM-DDTHH:MM:SSZ`) inside the validity window of the cost snapshots: `sb-hybrid analyze --bundle <dir>/bundle.json --as-of <UTC> --output-dir <new-dir>`. Add `--policy strict-analysis-1.0.0` when unmeasured capacity must stay UNKNOWN and no recommendation should be made from assumptions.
6. **Report from the outputs,** not from memory. Read `evaluation.json` (canonical figures), then `dossier.html` or `dossier.md` (13 sections), `executive-summary.md`, `implementation-guide.md`, `costs.csv` and `cashflow.csv`. State: the recommendation status (`CONDITIONAL` or `NONE`) and scenario, which alternatives are infeasible and which constraint failed, monthly cash and allocated TCO per scenario, net at 12 and 36 months, break-even month, the sensitivity thresholds, open questions and why security is UNKNOWN.
7. **Re-render without recalculating** when only a new copy of the documents is needed: `sb-hybrid dossier --evaluation <new-dir>/evaluation.json --output-dir <another-new-dir>`. It verifies every manifest hash first.
8. **Optional security attachment.** If a Starbots Security Skills review was produced for the report's `subject.json`, verify it with `sb-hybrid verify-security --review-dir <review> --proposal <new-dir>/subject.json --assessment-sha256 <receipt-kept-separately> --client-id <client> --project-id <project> --as-of <UTC>`. A valid but BLOCKED review is still reported as BLOCKED.

## Errors

On failure the CLI prints JSON with an `error` code and exits 2. Common codes: `HASH_MISMATCH` (run `seal-bundle` after editing), `EVIDENCE_STALE` (the `--as-of` is outside a snapshot or plan validity window; do not move the date just to make it pass), `INCOMPARABLE_COSTS` (currencies, periods or horizons differ), `UNSUPPORTED_FEATURE` (for example more than one workload or more than one cost snapshot per scenario), `PATH_DENIED` (the output directory already exists or traverses a link) and `INVALID_SCHEMA`. Fix the input and rerun; never hand-edit generated reports.

## Rules

- Present every figure as a modeled estimate from the supplied inputs, never as an observed saving or a vendor quote.
- Treat UNKNOWN, stale or missing values as blockers, not as zero.
- Cash and allocated TCO are separate views; never add them together.
- A `CONDITIONAL` recommendation is not approval. Real changes need current quotes, measured capacity, a tested restore, an independent security review and a separate human decision.
- Keep each output directory new; the CLI refuses to overwrite.

## Limits

No provider credentials, no live or scraped pricing, no billing or inventory import, no provisioning and no execution authority. One steady-state workload per bundle, a finite set of user-supplied alternatives and one cost snapshot per scenario. Capacity is an analytical model, not a load test. Taxes are not computed (`pre_tax_unknown`); FX applies only through an explicit dated quote. The optional `sb-aws-sim` command is an in-memory SQS simulation; it has no AWS SDK or real transport.
