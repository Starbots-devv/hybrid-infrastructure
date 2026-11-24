# Starbots Hybrid Infrastructure

Maple Service — fictional organization

**SYNTHETIC / ESTIMATED — execution blocked**

[Full dossier](dossier.html) · [Canonical JSON](evaluation.json) · [Cost lines](costs.csv)

## 1. Executive decision

Maple Service — fictional organization — CONDITIONAL recommendation: current. Savings are ESTIMATED.

Lowest allocated TCO over the requested horizon among model-compatible, budget-compatible alternatives.

Mandatory security remains UNKNOWN; no scenario is demonstrated feasible.

incremental&#95;cash: monthly saving 0 USD; net12 0; net36 0; investment 0; recovery month 1.

allocated&#95;tco: monthly saving 0 USD; net12 0; net36 0; investment 0; recovery month 1.

## 3. Alternatives and rejects

current: UNDEMONSTRATED. verified-security: UNKNOWN

vm: UNDEMONSTRATED. verified-security: UNKNOWN

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

### vm — UNDEMONSTRATED

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

## 8. Economics and recovery

All views are derived from the canonical cost rows and series. Cash excludes allocated depreciation; TCO includes it.

Migration/training is one-time investment; already owned hardware has no upfront purchase in this example. Hash-bound monthly FinOps assumptions produce the 36-month series.

### current / incremental&#95;cash totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 260 |
| monthly&#95;total | 260 |
| one&#95;time&#95;total | 0 |
| rounding&#95;delta | 0 |
| scenario&#95;id | current |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 260 |
| view | incremental&#95;cash |

### current / allocated&#95;tco totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 260 |
| monthly&#95;total | 260 |
| one&#95;time&#95;total | 0 |
| rounding&#95;delta | 0 |
| scenario&#95;id | current |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 260 |
| view | allocated&#95;tco |

### vm / incremental&#95;cash totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 305 |
| monthly&#95;total | 305 |
| one&#95;time&#95;total | 600 |
| rounding&#95;delta | 0 |
| scenario&#95;id | vm |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 305 |
| view | incremental&#95;cash |

### vm / allocated&#95;tco totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 305 |
| monthly&#95;total | 305 |
| one&#95;time&#95;total | 600 |
| rounding&#95;delta | 0 |
| scenario&#95;id | vm |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 305 |
| view | allocated&#95;tco |

### Comparable monthly economics

| Scenario / view | Month 1 saving | Net12 / net36 | Investment / recovery | Comparability |
| --- | --- | --- | --- | --- |
| current / incremental&#95;cash | 0 USD | 0 / 0 | 0 / 1 | True / None declared |
| current / allocated&#95;tco | 0 USD | 0 / 0 | 0 / 1 | True / None declared |
| vm / incremental&#95;cash | -45 USD | -1140 / -2220 | 600 / UNKNOWN — required input or evidence | True / Decimal inexact flag set by division/presentation; declared context preserved |
| vm / allocated&#95;tco | -45 USD | -1140 / -2220 | 600 / UNKNOWN — required input or evidence | True / Decimal inexact flag set by division/presentation; declared context preserved |

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
| input-bundle | bundle.json | 3714fbdc5cfcf28de60a5b92f2e1a1c929d9af2860b5e1e0f99d64786afeeed8 |
| profile | profile.json | 80e3e7b1500ac7948e5f7c4e67dabd79e8d7901a80eea9a20ae4016e9f7e8d59 |
| scenario | scenario-current.json | 8cec2b1f6a43adcb77bc0978a36fa759fd8871d924275ad0f8c8f54acb15cd70 |
| prices | prices-current.json | 62f2fb8489ae63918bf02aa6d3f369770c4825d780e3d6e42f65291e7125c480 |
| finops-plan | finops-current.json | 033d0f76e28a7c527b1760e8387f257ce53024ce463df7a2d26947cd1604c6c3 |
| scenario | scenario-vm.json | d5c94f6c237a3b11ff7130f0f9397c571d7243bb787347dfe17e49a899b96b46 |
| prices | prices-vm.json | 435da4332af2b3a28b4a65218ff05e72f39b767e9992b5c244f9110c2f68d295 |
| finops-plan | finops-vm.json | f0212efbaec157b5b3362d8a7f61d6d7b8e6762b7aa52f7d9a9d41af10ca8f90 |

### Run provenance

| Field | Value |
| --- | --- |
| Evaluation ID | evaluation-ec4a3b34833dc8df |
| Producer | name: starbots&#95;hybrid; source&#95;commit: UNRELEASED; version: 0.1.0a0 |
| As of | 2026-10-17T00:00:00Z |
| Policy | offline-demo-1.0.0 |
| Client / project | synthetic-stay-managed / synthetic-evaluation |
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
<!-- row-id: vm|incremental_cash|compute|monthly -->
<!-- row-id: vm|incremental_cash|network|monthly -->
<!-- row-id: vm|incremental_cash|operations|monthly -->
<!-- row-id: vm|incremental_cash|migration|one_time -->
<!-- row-id: vm|allocated_tco|compute|monthly -->
<!-- row-id: vm|allocated_tco|network|monthly -->
<!-- row-id: vm|allocated_tco|operations|monthly -->
<!-- row-id: vm|allocated_tco|migration|one_time -->
