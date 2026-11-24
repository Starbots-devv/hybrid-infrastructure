# Starbots Hybrid Infrastructure

Cedar API — fictional organization

**SYNTHETIC / ESTIMATED — execution blocked**

[Full dossier](dossier.html) · [Canonical JSON](evaluation.json) · [Cost lines](costs.csv)

## 4. Current and proposed architecture

Diagrams show declared nodes and directed edges. They do not prove availability, compatibility or live connectivity.

Failure domains sharing power or uplink have no demonstrated independence.

### current trust and failure domains

| Field | Value |
| --- | --- |
| Trust boundaries | Worker host; Cloud control plane; Managed database |
| Failure domains | correlated&#95;with: site-power-and-network; id: worker-site; independence&#95;evidence: UNKNOWN — required input or evidence; network: Single site uplink; outage test required; power: Single synthetic site; no independence proven; resource&#95;ids: compute |
| Actions | actions: keep; resource&#95;id: compute; actions: keep; resource&#95;id: db; actions: keep; resource&#95;id: network; actions: keep; resource&#95;id: observability; actions: keep; resource&#95;id: operations |

### hidden-costs trust and failure domains

| Field | Value |
| --- | --- |
| Trust boundaries | Optional local worker; Managed SaaS/API; Managed database |
| Failure domains | correlated&#95;with: site-power-and-network; id: worker-site; independence&#95;evidence: UNKNOWN — required input or evidence; network: Single site uplink; outage test required; power: Single synthetic site; no independence proven; resource&#95;ids: local-worker |
| Actions | actions: keep; resource&#95;id: compute; actions: keep; resource&#95;id: db; actions: keep; resource&#95;id: network; actions: keep; resource&#95;id: observability; actions: keep; resource&#95;id: transfer; actions: keep; resource&#95;id: operations; actions: keep; resource&#95;id: power; actions: keep; resource&#95;id: fallback; actions: keep; resource&#95;id: local-worker; actions: keep; resource&#95;id: migration |

![Current architecture](architecture-current.svg)
![Proposed architecture](architecture-proposed.svg)

## 5. Resource bill

Each declared resource is listed with owner, quantity and region. A resource without a priced line is explicitly identified; this is an exclusion, not a zero-cost claim.

### current resource bill

| ID / service | Provider / region | Size / quantity | Owner / allocation |
| --- | --- | --- | --- |
| compute / Managed SaaS/API compute | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| db / Managed database | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| network / Network | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| observability / Monitoring and security | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| operations / Operations labor | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |

### hidden-costs resource bill

| ID / service | Provider / region | Size / quantity | Owner / allocation |
| --- | --- | --- | --- |
| compute / Optional local worker and API compute | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| db / Managed database | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| network / Base network | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| observability / Monitoring and security | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| transfer / Data transfer and egress | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| operations / Additional operations labor | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| power / Power and replacement reserve | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| fallback / Cloud fallback | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| local-worker / Optional local worker host | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / No separate line: cost assumed included in compute; verify completeness |
| migration / Transition and training | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |

## 6. Connection matrix

Required DNS, identities, secrets, TLS roots and routes remain inputs. No connection test has been executed; missing inputs block implementation.

### current / worker-db

| Connection field | Required design / validation |
| --- | --- |
| connectivity&#95;test | Resolve approved hostname, validate TLS and perform a scoped dry-run transaction; not executed |
| cost&#95;line&#95;ids | network |
| destination | db |
| direction | outbound |
| dns | UNKNOWN — required input or evidence |
| firewall&#95;route | Outbound only; allow destination service and port after review |
| id | worker-db |
| identity | Dedicated least-privilege workload identity; no shared admin key |
| permissions | Write only application schema |
| port | 5432 |
| protocol | PostgreSQL over TLS |
| required&#95;inputs | Approved hostname; Certificate trust root; Scoped identity; Reviewed firewall rule |
| secret&#95;refs | secret://required/workload-identity |
| source | compute |
| tls | TLS with verified server certificate; actual hostname and trust chain required |
| traffic&#95;gb&#95;month | 10 |
| trust&#95;boundary | Cloud service boundary |

### hidden-costs / worker-db

| Connection field | Required design / validation |
| --- | --- |
| connectivity&#95;test | Resolve approved hostname, validate TLS and perform a scoped dry-run transaction; not executed |
| cost&#95;line&#95;ids | network |
| destination | db |
| direction | outbound |
| dns | UNKNOWN — required input or evidence |
| firewall&#95;route | Outbound only; allow destination service and port after review |
| id | worker-db |
| identity | Dedicated least-privilege workload identity; no shared admin key |
| permissions | Write only application schema |
| port | 5432 |
| protocol | PostgreSQL over TLS |
| required&#95;inputs | Approved hostname; Certificate trust root; Scoped identity; Reviewed firewall rule |
| secret&#95;refs | secret://required/workload-identity |
| source | compute |
| tls | TLS with verified server certificate; actual hostname and trust chain required |
| traffic&#95;gb&#95;month | 10 |
| trust&#95;boundary | Cloud service boundary |

### hidden-costs / local-worker-queue

| Connection field | Required design / validation |
| --- | --- |
| connectivity&#95;test | Resolve approved hostname, validate TLS and perform a scoped dry-run transaction; not executed |
| cost&#95;line&#95;ids | network |
| destination | compute |
| direction | outbound |
| dns | UNKNOWN — required input or evidence |
| firewall&#95;route | Outbound only; allow destination service and port after review |
| id | local-worker-queue |
| identity | Dedicated least-privilege workload identity; no shared admin key |
| permissions | Write only application schema |
| port | 443 |
| protocol | HTTPS |
| required&#95;inputs | Approved hostname; Certificate trust root; Scoped identity; Reviewed firewall rule |
| secret&#95;refs | secret://required/workload-identity |
| source | local-worker |
| tls | TLS with verified server certificate; actual hostname and trust chain required |
| traffic&#95;gb&#95;month | 10 |
| trust&#95;boundary | Local-to-cloud |

### hidden-costs / local-worker-db

| Connection field | Required design / validation |
| --- | --- |
| connectivity&#95;test | Resolve approved hostname, validate TLS and perform a scoped dry-run transaction; not executed |
| cost&#95;line&#95;ids | network |
| destination | db |
| direction | outbound |
| dns | UNKNOWN — required input or evidence |
| firewall&#95;route | Outbound only; allow destination service and port after review |
| id | local-worker-db |
| identity | Dedicated least-privilege workload identity; no shared admin key |
| permissions | Write only application schema |
| port | 5432 |
| protocol | PostgreSQL over TLS |
| required&#95;inputs | Approved hostname; Certificate trust root; Scoped identity; Reviewed firewall rule |
| secret&#95;refs | secret://required/workload-identity |
| source | local-worker |
| tls | TLS with verified server certificate; actual hostname and trust chain required |
| traffic&#95;gb&#95;month | 10 |
| trust&#95;boundary | Local-to-cloud |

## 7. Capacity and service objectives

Capacity is a steady-state analytical hypothesis. It predicts neither concurrent users nor latency percentiles.

Trigger: stop rollout when arrival rate exceeds modeled service capacity, a connection limit is reached, or queue age breaches the approved objective.

### current capacity

| Field | Value |
| --- | --- |
| assumptions | Synthetic steady-state slots and two-second service time; no measured benchmark.; Retry bursts, I/O ceilings and tail latency require separate tests. |
| bottlenecks | None declared |
| configuration | Declared parallel slots, memory, database connections and network ceilings |
| constraint&#95;results | actual: 4; dimension: capacity; evidence&#95;level: synthetic; id: model-throughput; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 1; actual: 20; dimension: capacity; evidence&#95;level: synthetic; id: model-db-connections; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 10; actual: 100; dimension: capacity; evidence&#95;level: synthetic; id: model-network; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 10 |
| critical&#95;paths | worker -&gt; durable queue -&gt; managed database |
| demand&#95;case | Managed SaaS/API with database and optional worker; full transfer, operations, power, and fallback cost |
| estimated&#95;capacity&#95;rps | 4 |
| evidence&#95;refs | None declared |
| failure&#95;domains | correlated&#95;with: site-power-and-network; id: worker-site; independence&#95;evidence: UNKNOWN — required input or evidence; network: Single site uplink; outage test required; power: Single synthetic site; no independence proven; resource&#95;ids: compute |
| headroom&#95;percent | 75 |
| limits | No measured throughput, latency percentile, queue-drain or restore test is supplied.; Correlated power/network failures and cloud fallback capacity need independent tests.; Single workload, steady arrival rate and equal service times; no users-to-RPS conversion. |
| measured&#95;or&#95;estimated | estimated |
| method | min&#40;parallel slots, floor&#40;memory / memory per job&#41;&#41; / service time |
| recovery&#95;objectives | acceptance&#95;condition: gte; id: availability; indicator: availability; measurement: Availability percentage; test is pending; target: 99.5; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: restore; indicator: rto; measurement: Minutes to restore service; drill is pending; target: 60; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: data-loss; indicator: rpo; measurement: Minutes of potentially lost writes; drill is pending; target: 15; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: staffing; indicator: staffing; measurement: Maintenance hours per month; target: 20; window: Monthly steady demand; recovery per incident |
| restoration&#95;test&#95;refs | None declared |
| scenario&#95;id | current |
| scenario&#95;sha256 | 02609f39e6e64426662479ee34fd9b9f25d840c847aa77a443cc43811f9c4e77 |
| target&#95;load&#95;rps | 1 |

### hidden-costs capacity

| Field | Value |
| --- | --- |
| assumptions | Synthetic steady-state slots and two-second service time; no measured benchmark.; Retry bursts, I/O ceilings and tail latency require separate tests. |
| bottlenecks | None declared |
| configuration | Declared parallel slots, memory, database connections and network ceilings |
| constraint&#95;results | actual: 2; dimension: capacity; evidence&#95;level: synthetic; id: model-throughput; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 1; actual: 20; dimension: capacity; evidence&#95;level: synthetic; id: model-db-connections; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 10; actual: 100; dimension: capacity; evidence&#95;level: synthetic; id: model-network; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 10 |
| critical&#95;paths | worker -&gt; durable queue -&gt; managed database |
| demand&#95;case | Managed SaaS/API with database and optional worker; full transfer, operations, power, and fallback cost |
| estimated&#95;capacity&#95;rps | 2 |
| evidence&#95;refs | None declared |
| failure&#95;domains | correlated&#95;with: site-power-and-network; id: worker-site; independence&#95;evidence: UNKNOWN — required input or evidence; network: Single site uplink; outage test required; power: Single synthetic site; no independence proven; resource&#95;ids: local-worker |
| headroom&#95;percent | 50 |
| limits | No measured throughput, latency percentile, queue-drain or restore test is supplied.; Correlated power/network failures and cloud fallback capacity need independent tests.; Single workload, steady arrival rate and equal service times; no users-to-RPS conversion. |
| measured&#95;or&#95;estimated | estimated |
| method | min&#40;parallel slots, floor&#40;memory / memory per job&#41;&#41; / service time |
| recovery&#95;objectives | acceptance&#95;condition: gte; id: availability; indicator: availability; measurement: Availability percentage; test is pending; target: 99.5; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: restore; indicator: rto; measurement: Minutes to restore service; drill is pending; target: 60; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: data-loss; indicator: rpo; measurement: Minutes of potentially lost writes; drill is pending; target: 15; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: staffing; indicator: staffing; measurement: Maintenance hours per month; target: 20; window: Monthly steady demand; recovery per incident |
| restoration&#95;test&#95;refs | None declared |
| scenario&#95;id | hidden-costs |
| scenario&#95;sha256 | bf39bea19f461df9a3b0326bf2baccbc70aaff9c211cc2a3bf8ca999f630a4c3 |
| target&#95;load&#95;rps | 1 |

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

### current / incremental&#95;cash cost lines

| Row ID | Resource / service | Quantity / rate / unit | Amount / currency | Source / evidence |
| --- | --- | --- | --- | --- |
| current&#124;incremental&#95;cash&#124;compute&#124;monthly | compute / Managed SaaS/API compute | 1 / 220 / month | 220 / USD | synthetic://flows/current/compute / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;incremental&#95;cash&#124;db&#124;monthly | db / Managed database | 1 / 100 / month | 100 / USD | synthetic://flows/current/db / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;incremental&#95;cash&#124;network&#124;monthly | network / Network | 1 / 60 / month | 60 / USD | synthetic://flows/current/network / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;incremental&#95;cash&#124;observability&#124;monthly | observability / Monitoring and security | 1 / 40 / month | 40 / USD | synthetic://flows/current/observability / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;incremental&#95;cash&#124;operations&#124;monthly | operations / Operations labor | 1 / 100 / month | 100 / USD | synthetic://flows/current/operations / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |

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

### current / allocated&#95;tco cost lines

| Row ID | Resource / service | Quantity / rate / unit | Amount / currency | Source / evidence |
| --- | --- | --- | --- | --- |
| current&#124;allocated&#95;tco&#124;compute&#124;monthly | compute / Managed SaaS/API compute | 1 / 220 / month | 220 / USD | synthetic://flows/current/compute / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;allocated&#95;tco&#124;db&#124;monthly | db / Managed database | 1 / 100 / month | 100 / USD | synthetic://flows/current/db / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;allocated&#95;tco&#124;network&#124;monthly | network / Network | 1 / 60 / month | 60 / USD | synthetic://flows/current/network / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;allocated&#95;tco&#124;observability&#124;monthly | observability / Monitoring and security | 1 / 40 / month | 40 / USD | synthetic://flows/current/observability / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;allocated&#95;tco&#124;operations&#124;monthly | operations / Operations labor | 1 / 100 / month | 100 / USD | synthetic://flows/current/operations / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |

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

### hidden-costs / incremental&#95;cash cost lines

| Row ID | Resource / service | Quantity / rate / unit | Amount / currency | Source / evidence |
| --- | --- | --- | --- | --- |
| hidden-costs&#124;incremental&#95;cash&#124;compute&#124;monthly | compute / Optional local worker and API compute | 1 / 120 / month | 120 / USD | synthetic://flows/hidden-costs/compute / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;incremental&#95;cash&#124;db&#124;monthly | db / Managed database | 1 / 100 / month | 100 / USD | synthetic://flows/hidden-costs/db / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;incremental&#95;cash&#124;network&#124;monthly | network / Base network | 1 / 30 / month | 30 / USD | synthetic://flows/hidden-costs/network / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;incremental&#95;cash&#124;observability&#124;monthly | observability / Monitoring and security | 1 / 40 / month | 40 / USD | synthetic://flows/hidden-costs/observability / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;incremental&#95;cash&#124;transfer&#124;monthly | transfer / Data transfer and egress | 1 / 110 / month | 110 / USD | synthetic://flows/hidden-costs/transfer / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;incremental&#95;cash&#124;operations&#124;monthly | operations / Additional operations labor | 1 / 80 / month | 80 / USD | synthetic://flows/hidden-costs/operations / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;incremental&#95;cash&#124;power&#124;monthly | power / Power and replacement reserve | 1 / 65 / month | 65 / USD | synthetic://flows/hidden-costs/power / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;incremental&#95;cash&#124;fallback&#124;monthly | fallback / Cloud fallback | 1 / 75 / month | 75 / USD | synthetic://flows/hidden-costs/fallback / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;incremental&#95;cash&#124;migration&#124;one&#95;time | migration / Transition and training | 1 / 400 / one&#95;time | 400 / USD | synthetic://flows/hidden-costs/migration / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours. |

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

### hidden-costs / allocated&#95;tco cost lines

| Row ID | Resource / service | Quantity / rate / unit | Amount / currency | Source / evidence |
| --- | --- | --- | --- | --- |
| hidden-costs&#124;allocated&#95;tco&#124;compute&#124;monthly | compute / Optional local worker and API compute | 1 / 120 / month | 120 / USD | synthetic://flows/hidden-costs/compute / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;allocated&#95;tco&#124;db&#124;monthly | db / Managed database | 1 / 100 / month | 100 / USD | synthetic://flows/hidden-costs/db / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;allocated&#95;tco&#124;network&#124;monthly | network / Base network | 1 / 30 / month | 30 / USD | synthetic://flows/hidden-costs/network / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;allocated&#95;tco&#124;observability&#124;monthly | observability / Monitoring and security | 1 / 40 / month | 40 / USD | synthetic://flows/hidden-costs/observability / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;allocated&#95;tco&#124;transfer&#124;monthly | transfer / Data transfer and egress | 1 / 110 / month | 110 / USD | synthetic://flows/hidden-costs/transfer / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;allocated&#95;tco&#124;operations&#124;monthly | operations / Additional operations labor | 1 / 80 / month | 80 / USD | synthetic://flows/hidden-costs/operations / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;allocated&#95;tco&#124;power&#124;monthly | power / Power and replacement reserve | 1 / 65 / month | 65 / USD | synthetic://flows/hidden-costs/power / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;allocated&#95;tco&#124;fallback&#124;monthly | fallback / Cloud fallback | 1 / 75 / month | 75 / USD | synthetic://flows/hidden-costs/fallback / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hidden-costs&#124;allocated&#95;tco&#124;migration&#124;one&#95;time | migration / Transition and training | 1 / 400 / one&#95;time | 400 / USD | synthetic://flows/hidden-costs/migration / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours. |

### Comparable monthly economics

| Scenario / view | Month 1 saving | Net12 / net36 | Investment / recovery | Comparability |
| --- | --- | --- | --- | --- |
| current / incremental&#95;cash | 0 USD | 0 / 0 | 0 / 1 | True / None declared |
| current / allocated&#95;tco | 0 USD | 0 / 0 | 0 / 1 | True / None declared |
| hidden-costs / incremental&#95;cash | -100 USD | -1600 / -4000 | 400 / UNKNOWN — required input or evidence | True / Decimal inexact flag set by division/presentation; declared context preserved |
| hidden-costs / allocated&#95;tco | -100 USD | -1600 / -4000 | 400 / UNKNOWN — required input or evidence | True / Decimal inexact flag set by division/presentation; declared context preserved |

### current / incremental&#95;cash monthly series

| Month | Baseline | Proposed | Saving | Cumulative net |
| --- | --- | --- | --- | --- |
| Month 1 | 520 | 520 | 0 | 0 |
| Month 2 | 520 | 520 | 0 | 0 |
| Month 3 | 520 | 520 | 0 | 0 |
| Month 4 | 520 | 520 | 0 | 0 |
| Month 5 | 520 | 520 | 0 | 0 |
| Month 6 | 520 | 520 | 0 | 0 |
| Month 7 | 520 | 520 | 0 | 0 |
| Month 8 | 520 | 520 | 0 | 0 |
| Month 9 | 520 | 520 | 0 | 0 |
| Month 10 | 520 | 520 | 0 | 0 |
| Month 11 | 520 | 520 | 0 | 0 |
| Month 12 | 520 | 520 | 0 | 0 |
| Month 13 | 520 | 520 | 0 | 0 |
| Month 14 | 520 | 520 | 0 | 0 |
| Month 15 | 520 | 520 | 0 | 0 |
| Month 16 | 520 | 520 | 0 | 0 |
| Month 17 | 520 | 520 | 0 | 0 |
| Month 18 | 520 | 520 | 0 | 0 |
| Month 19 | 520 | 520 | 0 | 0 |
| Month 20 | 520 | 520 | 0 | 0 |
| Month 21 | 520 | 520 | 0 | 0 |
| Month 22 | 520 | 520 | 0 | 0 |
| Month 23 | 520 | 520 | 0 | 0 |
| Month 24 | 520 | 520 | 0 | 0 |
| Month 25 | 520 | 520 | 0 | 0 |
| Month 26 | 520 | 520 | 0 | 0 |
| Month 27 | 520 | 520 | 0 | 0 |
| Month 28 | 520 | 520 | 0 | 0 |
| Month 29 | 520 | 520 | 0 | 0 |
| Month 30 | 520 | 520 | 0 | 0 |
| Month 31 | 520 | 520 | 0 | 0 |
| Month 32 | 520 | 520 | 0 | 0 |
| Month 33 | 520 | 520 | 0 | 0 |
| Month 34 | 520 | 520 | 0 | 0 |
| Month 35 | 520 | 520 | 0 | 0 |
| Month 36 | 520 | 520 | 0 | 0 |

### current / allocated&#95;tco monthly series

| Month | Baseline | Proposed | Saving | Cumulative net |
| --- | --- | --- | --- | --- |
| Month 1 | 520 | 520 | 0 | 0 |
| Month 2 | 520 | 520 | 0 | 0 |
| Month 3 | 520 | 520 | 0 | 0 |
| Month 4 | 520 | 520 | 0 | 0 |
| Month 5 | 520 | 520 | 0 | 0 |
| Month 6 | 520 | 520 | 0 | 0 |
| Month 7 | 520 | 520 | 0 | 0 |
| Month 8 | 520 | 520 | 0 | 0 |
| Month 9 | 520 | 520 | 0 | 0 |
| Month 10 | 520 | 520 | 0 | 0 |
| Month 11 | 520 | 520 | 0 | 0 |
| Month 12 | 520 | 520 | 0 | 0 |
| Month 13 | 520 | 520 | 0 | 0 |
| Month 14 | 520 | 520 | 0 | 0 |
| Month 15 | 520 | 520 | 0 | 0 |
| Month 16 | 520 | 520 | 0 | 0 |
| Month 17 | 520 | 520 | 0 | 0 |
| Month 18 | 520 | 520 | 0 | 0 |
| Month 19 | 520 | 520 | 0 | 0 |
| Month 20 | 520 | 520 | 0 | 0 |
| Month 21 | 520 | 520 | 0 | 0 |
| Month 22 | 520 | 520 | 0 | 0 |
| Month 23 | 520 | 520 | 0 | 0 |
| Month 24 | 520 | 520 | 0 | 0 |
| Month 25 | 520 | 520 | 0 | 0 |
| Month 26 | 520 | 520 | 0 | 0 |
| Month 27 | 520 | 520 | 0 | 0 |
| Month 28 | 520 | 520 | 0 | 0 |
| Month 29 | 520 | 520 | 0 | 0 |
| Month 30 | 520 | 520 | 0 | 0 |
| Month 31 | 520 | 520 | 0 | 0 |
| Month 32 | 520 | 520 | 0 | 0 |
| Month 33 | 520 | 520 | 0 | 0 |
| Month 34 | 520 | 520 | 0 | 0 |
| Month 35 | 520 | 520 | 0 | 0 |
| Month 36 | 520 | 520 | 0 | 0 |

### hidden-costs / incremental&#95;cash monthly series

| Month | Baseline | Proposed | Saving | Cumulative net |
| --- | --- | --- | --- | --- |
| Month 1 | 520 | 620 | -100 | -500 |
| Month 2 | 520 | 620 | -100 | -600 |
| Month 3 | 520 | 620 | -100 | -700 |
| Month 4 | 520 | 620 | -100 | -800 |
| Month 5 | 520 | 620 | -100 | -900 |
| Month 6 | 520 | 620 | -100 | -1000 |
| Month 7 | 520 | 620 | -100 | -1100 |
| Month 8 | 520 | 620 | -100 | -1200 |
| Month 9 | 520 | 620 | -100 | -1300 |
| Month 10 | 520 | 620 | -100 | -1400 |
| Month 11 | 520 | 620 | -100 | -1500 |
| Month 12 | 520 | 620 | -100 | -1600 |
| Month 13 | 520 | 620 | -100 | -1700 |
| Month 14 | 520 | 620 | -100 | -1800 |
| Month 15 | 520 | 620 | -100 | -1900 |
| Month 16 | 520 | 620 | -100 | -2000 |
| Month 17 | 520 | 620 | -100 | -2100 |
| Month 18 | 520 | 620 | -100 | -2200 |
| Month 19 | 520 | 620 | -100 | -2300 |
| Month 20 | 520 | 620 | -100 | -2400 |
| Month 21 | 520 | 620 | -100 | -2500 |
| Month 22 | 520 | 620 | -100 | -2600 |
| Month 23 | 520 | 620 | -100 | -2700 |
| Month 24 | 520 | 620 | -100 | -2800 |
| Month 25 | 520 | 620 | -100 | -2900 |
| Month 26 | 520 | 620 | -100 | -3000 |
| Month 27 | 520 | 620 | -100 | -3100 |
| Month 28 | 520 | 620 | -100 | -3200 |
| Month 29 | 520 | 620 | -100 | -3300 |
| Month 30 | 520 | 620 | -100 | -3400 |
| Month 31 | 520 | 620 | -100 | -3500 |
| Month 32 | 520 | 620 | -100 | -3600 |
| Month 33 | 520 | 620 | -100 | -3700 |
| Month 34 | 520 | 620 | -100 | -3800 |
| Month 35 | 520 | 620 | -100 | -3900 |
| Month 36 | 520 | 620 | -100 | -4000 |

### hidden-costs / allocated&#95;tco monthly series

| Month | Baseline | Proposed | Saving | Cumulative net |
| --- | --- | --- | --- | --- |
| Month 1 | 520 | 620 | -100 | -500 |
| Month 2 | 520 | 620 | -100 | -600 |
| Month 3 | 520 | 620 | -100 | -700 |
| Month 4 | 520 | 620 | -100 | -800 |
| Month 5 | 520 | 620 | -100 | -900 |
| Month 6 | 520 | 620 | -100 | -1000 |
| Month 7 | 520 | 620 | -100 | -1100 |
| Month 8 | 520 | 620 | -100 | -1200 |
| Month 9 | 520 | 620 | -100 | -1300 |
| Month 10 | 520 | 620 | -100 | -1400 |
| Month 11 | 520 | 620 | -100 | -1500 |
| Month 12 | 520 | 620 | -100 | -1600 |
| Month 13 | 520 | 620 | -100 | -1700 |
| Month 14 | 520 | 620 | -100 | -1800 |
| Month 15 | 520 | 620 | -100 | -1900 |
| Month 16 | 520 | 620 | -100 | -2000 |
| Month 17 | 520 | 620 | -100 | -2100 |
| Month 18 | 520 | 620 | -100 | -2200 |
| Month 19 | 520 | 620 | -100 | -2300 |
| Month 20 | 520 | 620 | -100 | -2400 |
| Month 21 | 520 | 620 | -100 | -2500 |
| Month 22 | 520 | 620 | -100 | -2600 |
| Month 23 | 520 | 620 | -100 | -2700 |
| Month 24 | 520 | 620 | -100 | -2800 |
| Month 25 | 520 | 620 | -100 | -2900 |
| Month 26 | 520 | 620 | -100 | -3000 |
| Month 27 | 520 | 620 | -100 | -3100 |
| Month 28 | 520 | 620 | -100 | -3200 |
| Month 29 | 520 | 620 | -100 | -3300 |
| Month 30 | 520 | 620 | -100 | -3400 |
| Month 31 | 520 | 620 | -100 | -3500 |
| Month 32 | 520 | 620 | -100 | -3600 |
| Month 33 | 520 | 620 | -100 | -3700 |
| Month 34 | 520 | 620 | -100 | -3800 |
| Month 35 | 520 | 620 | -100 | -3900 |
| Month 36 | 520 | 620 | -100 | -4000 |

### Sensitivity

| Variable | Condition | Effect |
| --- | --- | --- |
| hidden-costs / incremental&#95;cash / 12 months | If proposal cost decreases by USD 1600 over 12 months with other assumptions fixed. | Modeled net loss reaches zero; this is a threshold, not a probability. |
| hidden-costs / incremental&#95;cash / 36 months | If proposal cost decreases by USD 4000 over 36 months with other assumptions fixed. | Modeled net loss reaches zero; this is a threshold, not a probability. |
| hidden-costs / allocated&#95;tco / 12 months | If proposal cost decreases by USD 1600 over 12 months with other assumptions fixed. | Modeled net loss reaches zero; this is a threshold, not a probability. |
| hidden-costs / allocated&#95;tco / 36 months | If proposal cost decreases by USD 4000 over 36 months with other assumptions fixed. | Modeled net loss reaches zero; this is a threshold, not a probability. |
| Arrival rate or service time | Demand exceeds min&#40;slots, memory slots&#41; / service time | Queue can grow without bound; capacity validation fails. |

## 9. Security and continuity

No complete, independently verified security assessment is bound to this exact bundle.

Backup configuration is not proof of restoration. RTO/RPO, retention, encryption, scoped identities and fallback need independent evidence.

### Security coverage

| Area | State |
| --- | --- |
| Exact-subject assessment | MISSING; no real scanner has run |
| Capacity benchmark / restore test | MISSING |
| Execution eligibility | eligible: false; reasons: ANALYZE only; independent evidence and future approval gates are pending.; supported&#95;mode: ANALYZE |

## 10. Ordered implementation

Steps are a reviewed design procedure requiring actual accounts, hostnames, versions and separate approval. No command here deploys infrastructure.

Owner, prerequisites, required inputs, expected result, validation and stop conditions apply before each step.

### current / inventory

| Step field | Procedure |
| --- | --- |
| Action | Confirm residency, ownership, current bill and steady-state workload |
| Artifact | UNKNOWN — required input or evidence |
| Expected result | Reviewed inventory and dated price sheet |
| Id | inventory |
| Owner | Platform engineer |
| Parameters | name: Environment; required: true; value: Nonproduction only; actual account, region and names remain required inputs |
| Prerequisites | None declared |
| Required inputs | Approved account and region; Actual resource names and versions; Independent reviewer; Separate execution approval |
| Stop condition | Stop if ownership or data boundary is unknown |
| Validation | Reconcile every resource and rate against independently obtained evidence |

### current / identity

| Step field | Procedure |
| --- | --- |
| Action | Design scoped identities, secret delivery and outbound-only routes; do not put secrets in files |
| Artifact | UNKNOWN — required input or evidence |
| Expected result | Reviewed identity and network matrix |
| Id | identity |
| Owner | Platform engineer |
| Parameters | name: Environment; required: true; value: Nonproduction only; actual account, region and names remain required inputs |
| Prerequisites | inventory |
| Required inputs | Approved account and region; Actual resource names and versions; Independent reviewer; Separate execution approval |
| Stop condition | Stop on broad permissions, public DB route or missing TLS verification |
| Validation | Security reviewer verifies least privilege and TLS endpoints |

### current / sandbox

| Step field | Procedure |
| --- | --- |
| Action | In a separately approved nonproduction sandbox, configure durable jobs, idempotent consumers and managed DB backups |
| Artifact | UNKNOWN — required input or evidence |
| Expected result | Repeatable job processing with duplicate suppression |
| Id | sandbox |
| Owner | Platform engineer |
| Parameters | name: Environment; required: true; value: Nonproduction only; actual account, region and names remain required inputs; name: Database hostname; required: true; value: UNKNOWN — required input or evidence; name: Database port; required: true; value: 5432; name: Database TLS mode; required: true; value: verify-full; name: Queue endpoint; required: true; value: UNKNOWN — required input or evidence; name: Queue transport; required: true; value: HTTPS on port 443; AWS remains simulated; name: Queue visibility timeout seconds; required: true; value: UNKNOWN — required input or evidence; name: Worker parallel slots; required: true; value: 8; name: Database maximum pool connections; required: true; value: 10; name: Idempotency key; required: true; value: job&#95;id; persist before acknowledgment; name: Acknowledgment order; required: true; value: Commit database transaction, then acknowledge queue message; name: Retry policy; required: true; value: Bounded retries and dead-letter handling; counts require workload review; name: Application and provider versions; required: true; value: UNKNOWN — required input or evidence |
| Prerequisites | identity |
| Required inputs | Approved account and region; Actual resource names and versions; Independent reviewer; Separate execution approval; Measured worst-case job duration for visibility timeout; Validated backup and retention settings; Compatible application, database and queue versions |
| Stop condition | Stop on lost jobs, duplicate side effects or untested backup |
| Validation | Replay synthetic jobs, interrupt consumer before acknowledgment, verify deduplication and retained queue |

### current / capacity

| Step field | Procedure |
| --- | --- |
| Action | Run steady and burst load tests and simulate loss of local power/network |
| Artifact | UNKNOWN — required input or evidence |
| Expected result | Measured service rate, queue drain, DB connection ceiling and fallback budget |
| Id | capacity |
| Owner | Platform engineer |
| Parameters | name: Environment; required: true; value: Nonproduction only; actual account, region and names remain required inputs |
| Prerequisites | sandbox |
| Required inputs | Approved account and region; Actual resource names and versions; Independent reviewer; Separate execution approval |
| Stop condition | Stop if any mandatory objective fails or remains unmeasured |
| Validation | Record throughput, tail latency, queue age, costs and correlation during outage |

### current / restore

| Step field | Procedure |
| --- | --- |
| Action | Rehearse cutover and restore with a consistent backup and old consumers available |
| Artifact | UNKNOWN — required input or evidence |
| Expected result | Proven RTO/RPO and reversible cutover |
| Id | restore |
| Owner | Platform engineer |
| Parameters | name: Environment; required: true; value: Nonproduction only; actual account, region and names remain required inputs |
| Prerequisites | capacity |
| Required inputs | Approved account and region; Actual resource names and versions; Independent reviewer; Separate execution approval |
| Stop condition | Stop if data cannot reconcile or writes are not replayable |
| Validation | Time restore, compare checksums and replay post-cutover events |

### current / approval

| Step field | Procedure |
| --- | --- |
| Action | Obtain independent security, engineering, finance and customer approval before production |
| Artifact | UNKNOWN — required input or evidence |
| Expected result | Explicit approval bound to final artifact hashes |
| Id | approval |
| Owner | Customer and independent reviewers |
| Parameters | name: Environment; required: true; value: Nonproduction only; actual account, region and names remain required inputs |
| Prerequisites | restore |
| Required inputs | Approved account and region; Actual resource names and versions; Independent reviewer; Separate execution approval |
| Stop condition | Stop if any evidence or approval is missing |
| Validation | Verify subject identity, freshness and every mandatory control |

## 11. Migration and rollback

Preserve accepted writes and idempotent event IDs. Reconcile state before reopening traffic; reverting a process alone is insufficient.

### current migration and rollback

| Field | Procedure |
| --- | --- |
| Cutover | Pause consumers, drain in-flight jobs, record watermark, enable one consumer cohort |
| Data state | Managed database remains source of truth; snapshot and event journal before cutover |
| Irreversible actions | None declared |
| Post cutover writes | Replay idempotent event IDs; never discard newly accepted writes |
| Rollback actions | Pause new consumers; Retain queue and audit journal; Resume old cloud consumers at recorded watermark; Reconcile writes before reopening |
| Rollback triggers | Objective violation; Lost or duplicated side effect; Unreconciled write; Unexpected operating cost |
| Schema compatibility | Use an additive backward-compatible schema; verify both consumer versions before cutover |
| Window | Approved maintenance window after successful rehearsal; duration not measured |

## 12. Operations

The platform engineer reviews queue age, errors, DB connections and backup freshness daily; reconciles costs weekly and reviews patches and restore evidence monthly.

Alert thresholds and on-call coverage require customer approval. Fallback capacity and its budget are unverified.

### current operating model

| Field | Value |
| --- | --- |
| Alerts | Queue age and depth; Consumer errors and retries; Database connection pool; Backup age; Local uplink health |
| Fallback | Retain the current managed service until a separately tested recovery path exists. |
| Maintenance hours month | 18 |
| On call | Business-hours response; verify incident coverage |
| Owner | Platform engineer |

### hidden-costs operating model

| Field | Value |
| --- | --- |
| Alerts | Queue age and depth; Consumer errors and retries; Database connection pool; Backup age; Local uplink health; Transfer volume and egress; Fallback capacity |
| Fallback | Retain the durable cloud queue and restore managed consumers; cloud fallback is included in the proposed cost. |
| Maintenance hours month | 16 |
| On call | Business-hours response; verify incident coverage |
| Owner | Platform engineer |

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
