# Starbots Hybrid Infrastructure

Cedar API — fictional organization

**SYNTHETIC / ESTIMATED — execution blocked**

[Full dossier](dossier.html) · [Canonical JSON](evaluation.json) · [Cost lines](costs.csv)

## 1. Executive decision

Cedar API — fictional organization — CONDITIONAL recommendation: current. Savings are ESTIMATED.

Lowest allocated TCO over the requested horizon among model-compatible, budget-compatible alternatives.

Mandatory security remains UNKNOWN; no scenario is demonstrated feasible.

incremental&#95;cash: monthly saving 0 USD; net12 0; net36 0; investment 0; recovery month 1.

allocated&#95;tco: monthly saving 0 USD; net12 0; net36 0; investment 0; recovery month 1.

## 3. Alternatives and rejects

current: UNDEMONSTRATED. verified-security: UNKNOWN

hidden-costs: UNDEMONSTRATED. verified-security: UNKNOWN

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

### hidden-costs — UNDEMONSTRATED

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
| known&#95;monthly&#95;subtotal | 520 |
| monthly&#95;total | 520 |
| one&#95;time&#95;total | 0 |
| rounding&#95;delta | 0 |
| scenario&#95;id | current |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 520 |
| view | incremental&#95;cash |

### current / allocated&#95;tco totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 520 |
| monthly&#95;total | 520 |
| one&#95;time&#95;total | 0 |
| rounding&#95;delta | 0 |
| scenario&#95;id | current |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 520 |
| view | allocated&#95;tco |

### hidden-costs / incremental&#95;cash totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 620 |
| monthly&#95;total | 620 |
| one&#95;time&#95;total | 400 |
| rounding&#95;delta | 0 |
| scenario&#95;id | hidden-costs |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 620 |
| view | incremental&#95;cash |

### hidden-costs / allocated&#95;tco totals

| Field | Value |
| --- | --- |
| accounting&#95;basis | list |
| complete | true |
| currency | USD |
| known&#95;monthly&#95;subtotal | 620 |
| monthly&#95;total | 620 |
| one&#95;time&#95;total | 400 |
| rounding&#95;delta | 0 |
| scenario&#95;id | hidden-costs |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 620 |
| view | allocated&#95;tco |

### Comparable monthly economics

| Scenario / view | Month 1 saving | Net12 / net36 | Investment / recovery | Comparability |
| --- | --- | --- | --- | --- |
| current / incremental&#95;cash | 0 USD | 0 / 0 | 0 / 1 | True / None declared |
| current / allocated&#95;tco | 0 USD | 0 / 0 | 0 / 1 | True / None declared |
| hidden-costs / incremental&#95;cash | -100 USD | -1600 / -4000 | 400 / UNKNOWN — required input or evidence | True / Decimal inexact flag set by division/presentation; declared context preserved |
| hidden-costs / allocated&#95;tco | -100 USD | -1600 / -4000 | 400 / UNKNOWN — required input or evidence | True / Decimal inexact flag set by division/presentation; declared context preserved |

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
| input-bundle | bundle.json | 34b2f3424f04f8200e20634711f469abd90f47f070d0bc2848d30dbd9aa42207 |
| profile | profile.json | 1e5496286ab0f0194ae1d054f98e22cd3efd736d519fe4d31fa4f7b6e0a71bdb |
| scenario | scenario-current.json | 02609f39e6e64426662479ee34fd9b9f25d840c847aa77a443cc43811f9c4e77 |
| prices | prices-current.json | 3566f56de0095fe452adc164caf97576c1a8a61edea52bc8bb982de22a424a96 |
| finops-plan | finops-current.json | ffdac7d3f11b4243b631bc517aef4a83949a397942d9ef9ef1c8152f21edb8fe |
| scenario | scenario-hidden-costs.json | bf39bea19f461df9a3b0326bf2baccbc70aaff9c211cc2a3bf8ca999f630a4c3 |
| prices | prices-hidden-costs.json | a6b41bece9feb3e804bb83ef6a47f65c951f063489dcd63a3cbf63cb76481c83 |
| finops-plan | finops-hidden-costs.json | da4e54af3dfeac0d078aac9be6fec5e6c5a235c671f0b9f47bfa834dfed69fba |

### Run provenance

| Field | Value |
| --- | --- |
| Evaluation ID | evaluation-b23bb55512731e40 |
| Producer | name: starbots&#95;hybrid; source&#95;commit: UNRELEASED; version: 0.1.0a0 |
| As of | 2026-10-17T00:00:00Z |
| Policy | offline-demo-1.0.0 |
| Client / project | synthetic-hidden-costs / synthetic-evaluation |
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
<!-- row-id: hidden-costs|incremental_cash|compute|monthly -->
<!-- row-id: hidden-costs|incremental_cash|db|monthly -->
<!-- row-id: hidden-costs|incremental_cash|network|monthly -->
<!-- row-id: hidden-costs|incremental_cash|observability|monthly -->
<!-- row-id: hidden-costs|incremental_cash|transfer|monthly -->
<!-- row-id: hidden-costs|incremental_cash|operations|monthly -->
<!-- row-id: hidden-costs|incremental_cash|power|monthly -->
<!-- row-id: hidden-costs|incremental_cash|fallback|monthly -->
<!-- row-id: hidden-costs|incremental_cash|migration|one_time -->
<!-- row-id: hidden-costs|allocated_tco|compute|monthly -->
<!-- row-id: hidden-costs|allocated_tco|db|monthly -->
<!-- row-id: hidden-costs|allocated_tco|network|monthly -->
<!-- row-id: hidden-costs|allocated_tco|observability|monthly -->
<!-- row-id: hidden-costs|allocated_tco|transfer|monthly -->
<!-- row-id: hidden-costs|allocated_tco|operations|monthly -->
<!-- row-id: hidden-costs|allocated_tco|power|monthly -->
<!-- row-id: hidden-costs|allocated_tco|fallback|monthly -->
<!-- row-id: hidden-costs|allocated_tco|migration|one_time -->
