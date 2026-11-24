# Starbots Hybrid Infrastructure

Northstar Parts — fictional organization

**SYNTHETIC / ESTIMATED — execution blocked**

[Full dossier](dossier.html) · [Canonical JSON](evaluation.json) · [Cost lines](costs.csv)

## 1. Executive decision

Northstar Parts — fictional organization — CONDITIONAL recommendation: hybrid. Savings are ESTIMATED.

Lowest allocated TCO over the requested horizon among model-compatible, budget-compatible alternatives.

Mandatory security remains UNKNOWN; no scenario is demonstrated feasible.

incremental&#95;cash: monthly saving 220 USD; net12 1440; net36 6720; investment 1200; recovery month 6.

allocated&#95;tco: monthly saving 180 USD; net12 960; net36 5280; investment 1200; recovery month 7.

## 3. Alternatives and rejects

current: UNDEMONSTRATED. verified-security: UNKNOWN

hybrid: UNDEMONSTRATED. verified-security: UNKNOWN

local-only: INFEASIBLE. availability: FAIL, restore: FAIL, data-loss: FAIL, eu-residency: FAIL, verified-security: UNKNOWN

### current — UNDEMONSTRATED

| ID / dimension | Rule target / observation | State / mandatory | Evidence / rationale |
| --- | --- | --- | --- |
| availability / availability | 99.5 / 99.9 | PASS / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| restore / rto | 60 / 45 | PASS / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| data-loss / rpo | 15 / 10 | PASS / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| staffing / staffing | 20 / 18 | PASS / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| eu-residency / residency | EU / EU | PASS / True | synthetic / All data-bearing dependencies must satisfy the mandatory EU boundary; declared observation, not independently verified |
| model-throughput / capacity | 1 / 4 | PASS / True | synthetic / Analytical synthetic model only; benchmark and load test required |
| model-db-connections / capacity | 10 / 20 | PASS / True | synthetic / Analytical synthetic model only; benchmark and load test required |
| model-network / capacity | 10 / 100 | PASS / True | synthetic / Analytical synthetic model only; benchmark and load test required |
| verified-security / security | Exact-subject verified security coverage / UNKNOWN — required input or evidence | UNKNOWN / True | unknown / No independently verified exact-subject security review is bound to this analysis |

### hybrid — UNDEMONSTRATED

| ID / dimension | Rule target / observation | State / mandatory | Evidence / rationale |
| --- | --- | --- | --- |
| availability / availability | 99.5 / 99.9 | PASS / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| restore / rto | 60 / 45 | PASS / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| data-loss / rpo | 15 / 10 | PASS / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| staffing / staffing | 20 / 16 | PASS / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| eu-residency / residency | EU / EU | PASS / True | synthetic / All data-bearing dependencies must satisfy the mandatory EU boundary; declared observation, not independently verified |
| model-throughput / capacity | 1 / 2 | PASS / True | synthetic / Analytical synthetic model only; benchmark and load test required |
| model-db-connections / capacity | 10 / 20 | PASS / True | synthetic / Analytical synthetic model only; benchmark and load test required |
| model-network / capacity | 10 / 100 | PASS / True | synthetic / Analytical synthetic model only; benchmark and load test required |
| verified-security / security | Exact-subject verified security coverage / UNKNOWN — required input or evidence | UNKNOWN / True | unknown / No independently verified exact-subject security review is bound to this analysis |

### local-only — INFEASIBLE

| ID / dimension | Rule target / observation | State / mandatory | Evidence / rationale |
| --- | --- | --- | --- |
| availability / availability | 99.5 / 98 | FAIL / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| restore / rto | 60 / 240 | FAIL / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| data-loss / rpo | 15 / 120 | FAIL / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| staffing / staffing | 20 / 18 | PASS / True | synthetic / Unmeasured design hypothesis; prove by load test, restore drill or operations log; declared observation, not independently verified |
| eu-residency / residency | EU / Unspecified | FAIL / True | synthetic / All data-bearing dependencies must satisfy the mandatory EU boundary; declared observation, not independently verified |
| model-throughput / capacity | 1 / 2 | PASS / True | synthetic / Analytical synthetic model only; benchmark and load test required |
| model-db-connections / capacity | 10 / 20 | PASS / True | synthetic / Analytical synthetic model only; benchmark and load test required |
| model-network / capacity | 10 / 100 | PASS / True | synthetic / Analytical synthetic model only; benchmark and load test required |
| verified-security / security | Exact-subject verified security coverage / UNKNOWN — required input or evidence | UNKNOWN / True | unknown / No independently verified exact-subject security review is bound to this analysis |

## 8. Economics and recovery

All views are derived from the canonical cost rows and series. Cash excludes allocated depreciation; TCO includes it.

Migration/training is one-time investment; already owned hardware has no upfront purchase in this example. Hash-bound monthly FinOps assumptions produce the 36-month series.

### current / incremental&#95;cash totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 720 |
| monthly&#95;total | 720 |
| one&#95;time&#95;total | 0 |
| rounding&#95;delta | 0 |
| scenario&#95;id | current |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 720 |
| view | incremental&#95;cash |

### current / allocated&#95;tco totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 720 |
| monthly&#95;total | 720 |
| one&#95;time&#95;total | 0 |
| rounding&#95;delta | 0 |
| scenario&#95;id | current |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 720 |
| view | allocated&#95;tco |

### hybrid / incremental&#95;cash totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 500 |
| monthly&#95;total | 500 |
| one&#95;time&#95;total | 1200 |
| rounding&#95;delta | 0 |
| scenario&#95;id | hybrid |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 500 |
| view | incremental&#95;cash |

### hybrid / allocated&#95;tco totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 540 |
| monthly&#95;total | 540 |
| one&#95;time&#95;total | 1200 |
| rounding&#95;delta | 0 |
| scenario&#95;id | hybrid |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 540 |
| view | allocated&#95;tco |

### local-only / incremental&#95;cash totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 150 |
| monthly&#95;total | 150 |
| one&#95;time&#95;total | 0 |
| rounding&#95;delta | 0 |
| scenario&#95;id | local-only |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 150 |
| view | incremental&#95;cash |

### local-only / allocated&#95;tco totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 150 |
| monthly&#95;total | 150 |
| one&#95;time&#95;total | 0 |
| rounding&#95;delta | 0 |
| scenario&#95;id | local-only |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 150 |
| view | allocated&#95;tco |

### Comparable monthly economics

| Scenario / view | Month 1 saving | Net12 / net36 | Investment / recovery | Comparability |
| --- | --- | --- | --- | --- |
| current / incremental&#95;cash | 0 USD | 0 / 0 | 0 / 1 | True / None declared |
| current / allocated&#95;tco | 0 USD | 0 / 0 | 0 / 1 | True / None declared |
| hybrid / incremental&#95;cash | 220 USD | 1440 / 6720 | 1200 / 6 | True / Decimal inexact flag set by division/presentation; declared context preserved |
| hybrid / allocated&#95;tco | 180 USD | 960 / 5280 | 1200 / 7 | True / None declared |
| local-only / incremental&#95;cash | 570 USD | 6840 / 20520 | 0 / 1 | True / Decimal inexact flag set by division/presentation; declared context preserved |
| local-only / allocated&#95;tco | 570 USD | 6840 / 20520 | 0 / 1 | True / Decimal inexact flag set by division/presentation; declared context preserved |

## 9. Security and continuity

No complete, independently verified security assessment is bound to this exact bundle.

Backup configuration is not proof of restoration. RTO/RPO, retention, encryption, scoped identities and fallback need independent evidence.

### Security coverage

| Area | State |
| --- | --- |
| Exact-subject assessment | MISSING; no real scanner has run |
| Capacity benchmark / restore test | MISSING |
| Execution eligibility | eligible: false; reasons: ANALYZE only; independent evidence and future approval gates are pending.; supported&#95;mode: ANALYZE |

## 13. Evidence, approval and acceptance

Synthetic rates and service times are explicit modeling inputs, not vendor quotes or measured benchmarks.

No deployment, provider lookup, credentials or execution approval is provided.

FinOps plan overrides are explicit and hash-bound when present; absent a plan, demand and prices remain constant. Tax is pre-tax UNKNOWN.

One workload and one cost snapshot per scenario, one currency per view.

Sensitivity is a deterministic single-variable cost threshold, not a probability distribution or market forecast.

Security and recovery objectives require separate exact-subject verification.

English dossier text is implemented; locale metadata does not translate imported or generated prose.

Acceptance requires measured load and outage tests, successful restore within RTO/RPO, dated complete prices, independent exact-subject security review, and customer/engineering/finance approvals.

This dossier grants no execution authority. Input hashes provide integrity, not authenticity or approval.

### Open questions

| ID | Question | Owner / required by |
| --- | --- | --- |
| prove-capacity | Can the declared worker, database and network sustain demand during a site outage? | Platform engineer / Before any production change |
| verify-prices | What are the dated provider quotes, labor costs, taxes and actual egress? | Finance owner / Before commercial approval |
| security-review | Do exact-subject security controls, credentials, retention and recovery pass independent validation? | Security reviewer / Before implementation approval |

### Input evidence manifest

| Role | Path | SHA-256 |
| --- | --- | --- |
| input-bundle | bundle.json | 86a3152c2b5df68ebd179c88a47ea0cbac1262041507bb5c765a35d2c9bc349e |
| profile | profile.json | 683b7a55276f3d565e6e57780ed975cd7cd3b1f48cd107eece6f2f355a3746e1 |
| scenario | scenario-current.json | d5115e3f1e1a67d41ba4484f59f1f02418f7fbf820034bbae323217ca23ca4ee |
| prices | prices-current.json | 823b20d09d751060ac6d8d6fc72fbeae9e9a7184b8f1c0f0d9b05d850fd63216 |
| finops-plan | finops-current.json | 3071b30a0ccac3bfc1c6a68df0df73e4338f4dae0fc02cc5f1d43f2e0a2546d0 |
| scenario | scenario-hybrid.json | ef3fb9f1fd3984f82d81eb24cfd07c03f25175dc162033bb5cc420c22129e5af |
| prices | prices-hybrid.json | 738ace94c25738840884e6ebdca1ae44e0d7c6657af8879bb329e5728cddfdfa |
| finops-plan | finops-hybrid.json | 999d7f83e809ea23319cd655285955355f9c05a062848b1751b77aa5b30be5c4 |
| scenario | scenario-local-only.json | 44434ad823ecd65a04baaf3d1c2627a5dae10743e4a48206dba676fbada53617 |
| prices | prices-local-only.json | 38eddb63969c56825ea09d8be6f9629b5882902ee6d2ffce24fb0b9f35ed9358 |
| finops-plan | finops-local-only.json | e2281c97007efcca23d07932bfd20a3c18141ebed0734c0beea54ad0a398f487 |

### Run provenance

| Field | Value |
| --- | --- |
| Evaluation ID | evaluation-3292d33349617ff4 |
| Producer | name: starbots&#95;hybrid; source&#95;commit: UNRELEASED; version: 0.1.0a0 |
| As of | 2026-10-17T00:00:00Z |
| Policy | offline-demo-1.0.0 |
| Client / project | synthetic-northstar-parts / synthetic-evaluation |
| Confidence | low / Synthetic assumptions, untested restoration, and missing security evidence limit confidence. |

<!-- row-id: current|incremental_cash|compute|monthly -->
<!-- row-id: current|incremental_cash|db|monthly -->
<!-- row-id: current|incremental_cash|network|monthly -->
<!-- row-id: current|incremental_cash|observability|monthly -->
<!-- row-id: current|incremental_cash|operations|monthly -->
<!-- row-id: current|allocated_tco|compute|monthly -->
<!-- row-id: current|allocated_tco|db|monthly -->
<!-- row-id: current|allocated_tco|network|monthly -->
<!-- row-id: current|allocated_tco|observability|monthly -->
<!-- row-id: current|allocated_tco|operations|monthly -->
<!-- row-id: hybrid|incremental_cash|compute|monthly -->
<!-- row-id: hybrid|incremental_cash|db|monthly -->
<!-- row-id: hybrid|incremental_cash|network|monthly -->
<!-- row-id: hybrid|incremental_cash|observability|monthly -->
<!-- row-id: hybrid|incremental_cash|power|monthly -->
<!-- row-id: hybrid|incremental_cash|operations|monthly -->
<!-- row-id: hybrid|incremental_cash|migration|one_time -->
<!-- row-id: hybrid|allocated_tco|compute|monthly -->
<!-- row-id: hybrid|allocated_tco|db|monthly -->
<!-- row-id: hybrid|allocated_tco|network|monthly -->
<!-- row-id: hybrid|allocated_tco|observability|monthly -->
<!-- row-id: hybrid|allocated_tco|power|monthly -->
<!-- row-id: hybrid|allocated_tco|operations|monthly -->
<!-- row-id: hybrid|allocated_tco|hardware|monthly -->
<!-- row-id: hybrid|allocated_tco|migration|one_time -->
<!-- row-id: local-only|incremental_cash|compute|monthly -->
<!-- row-id: local-only|incremental_cash|db|monthly -->
<!-- row-id: local-only|incremental_cash|network|monthly -->
<!-- row-id: local-only|incremental_cash|observability|monthly -->
<!-- row-id: local-only|incremental_cash|power|monthly -->
<!-- row-id: local-only|incremental_cash|operations|monthly -->
<!-- row-id: local-only|allocated_tco|compute|monthly -->
<!-- row-id: local-only|allocated_tco|db|monthly -->
<!-- row-id: local-only|allocated_tco|network|monthly -->
<!-- row-id: local-only|allocated_tco|observability|monthly -->
<!-- row-id: local-only|allocated_tco|power|monthly -->
<!-- row-id: local-only|allocated_tco|operations|monthly -->
