# Starbots Hybrid Infrastructure

Northstar Parts — fictional organization

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

### hybrid trust and failure domains

| Field | Value |
| --- | --- |
| Trust boundaries | Worker host; Cloud control plane; Managed database |
| Failure domains | correlated&#95;with: site-power-and-network; id: worker-site; independence&#95;evidence: UNKNOWN — required input or evidence; network: Single site uplink; outage test required; power: Single synthetic site; no independence proven; resource&#95;ids: local-worker |
| Actions | actions: keep; resource&#95;id: compute; actions: keep; resource&#95;id: db; actions: keep; resource&#95;id: network; actions: keep; resource&#95;id: observability; actions: keep; resource&#95;id: power; actions: keep; resource&#95;id: operations; actions: keep; resource&#95;id: local-worker; actions: keep; resource&#95;id: hardware; actions: keep; resource&#95;id: migration |

### local-only trust and failure domains

| Field | Value |
| --- | --- |
| Trust boundaries | Worker host; Cloud control plane; Managed database |
| Failure domains | correlated&#95;with: site-power-and-network; id: worker-site; independence&#95;evidence: UNKNOWN — required input or evidence; network: Single site uplink; outage test required; power: Single synthetic site; no independence proven; resource&#95;ids: compute |
| Actions | actions: keep; resource&#95;id: compute; actions: keep; resource&#95;id: db; actions: keep; resource&#95;id: network; actions: keep; resource&#95;id: observability; actions: keep; resource&#95;id: power; actions: keep; resource&#95;id: operations |

![Current architecture](architecture-current.svg)
![Proposed architecture](architecture-proposed.svg)

## 5. Resource bill

Each declared resource is listed with owner, quantity and region. A resource without a priced line is explicitly identified; this is an exclusion, not a zero-cost claim.

### current resource bill

| ID / service | Provider / region | Size / quantity | Owner / allocation |
| --- | --- | --- | --- |
| compute / Cloud workers and durable queue | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| db / Managed database | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| network / Network and egress | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| observability / Monitoring and security | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| operations / Operations labor | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |

### hybrid resource bill

| ID / service | Provider / region | Size / quantity | Owner / allocation |
| --- | --- | --- | --- |
| compute / Cloud control and fallback | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| db / Managed database | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| network / Network and egress | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| observability / Monitoring and security | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| power / Local power and connectivity | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| operations / Operations labor | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| local-worker / Optional local worker host | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / No separate line: cost assumed included in compute; verify completeness |
| hardware / Allocated existing hardware ownership | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| migration / Transition and training | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |

### local-only resource bill

| ID / service | Provider / region | Size / quantity | Owner / allocation |
| --- | --- | --- | --- |
| compute / Local worker and queue | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| db / Local database | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| network / Local network | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| observability / Monitoring | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| power / Power | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |
| operations / Operations labor | Synthetic architecture model / EU model boundary | Explicit capacity assumptions; no vendor SKU / 1 | Platform engineer / priced |

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

### hybrid / worker-db

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

### hybrid / local-worker-queue

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

### hybrid / local-worker-db

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

### local-only / worker-db

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
| demand&#95;case | Recoverable asynchronous jobs; managed database stays in cloud; local worker has cloud fallback |
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
| scenario&#95;sha256 | d5115e3f1e1a67d41ba4484f59f1f02418f7fbf820034bbae323217ca23ca4ee |
| target&#95;load&#95;rps | 1 |

### hybrid capacity

| Field | Value |
| --- | --- |
| assumptions | Synthetic steady-state slots and two-second service time; no measured benchmark.; Retry bursts, I/O ceilings and tail latency require separate tests. |
| bottlenecks | None declared |
| configuration | Declared parallel slots, memory, database connections and network ceilings |
| constraint&#95;results | actual: 2; dimension: capacity; evidence&#95;level: synthetic; id: model-throughput; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 1; actual: 20; dimension: capacity; evidence&#95;level: synthetic; id: model-db-connections; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 10; actual: 100; dimension: capacity; evidence&#95;level: synthetic; id: model-network; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 10 |
| critical&#95;paths | worker -&gt; durable queue -&gt; managed database |
| demand&#95;case | Recoverable asynchronous jobs; managed database stays in cloud; local worker has cloud fallback |
| estimated&#95;capacity&#95;rps | 2 |
| evidence&#95;refs | None declared |
| failure&#95;domains | correlated&#95;with: site-power-and-network; id: worker-site; independence&#95;evidence: UNKNOWN — required input or evidence; network: Single site uplink; outage test required; power: Single synthetic site; no independence proven; resource&#95;ids: local-worker |
| headroom&#95;percent | 50 |
| limits | No measured throughput, latency percentile, queue-drain or restore test is supplied.; Correlated power/network failures and cloud fallback capacity need independent tests.; Single workload, steady arrival rate and equal service times; no users-to-RPS conversion. |
| measured&#95;or&#95;estimated | estimated |
| method | min&#40;parallel slots, floor&#40;memory / memory per job&#41;&#41; / service time |
| recovery&#95;objectives | acceptance&#95;condition: gte; id: availability; indicator: availability; measurement: Availability percentage; test is pending; target: 99.5; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: restore; indicator: rto; measurement: Minutes to restore service; drill is pending; target: 60; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: data-loss; indicator: rpo; measurement: Minutes of potentially lost writes; drill is pending; target: 15; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: staffing; indicator: staffing; measurement: Maintenance hours per month; target: 20; window: Monthly steady demand; recovery per incident |
| restoration&#95;test&#95;refs | None declared |
| scenario&#95;id | hybrid |
| scenario&#95;sha256 | ef3fb9f1fd3984f82d81eb24cfd07c03f25175dc162033bb5cc420c22129e5af |
| target&#95;load&#95;rps | 1 |

### local-only capacity

| Field | Value |
| --- | --- |
| assumptions | Synthetic steady-state slots and two-second service time; no measured benchmark.; Retry bursts, I/O ceilings and tail latency require separate tests. |
| bottlenecks | None declared |
| configuration | Declared parallel slots, memory, database connections and network ceilings |
| constraint&#95;results | actual: 2; dimension: capacity; evidence&#95;level: synthetic; id: model-throughput; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 1; actual: 20; dimension: capacity; evidence&#95;level: synthetic; id: model-db-connections; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 10; actual: 100; dimension: capacity; evidence&#95;level: synthetic; id: model-network; mandatory: true; rationale: Analytical synthetic model only; benchmark and load test required; state: PASS; threshold: 10 |
| critical&#95;paths | worker -&gt; durable queue -&gt; managed database |
| demand&#95;case | Recoverable asynchronous jobs; managed database stays in cloud; local worker has cloud fallback |
| estimated&#95;capacity&#95;rps | 2 |
| evidence&#95;refs | None declared |
| failure&#95;domains | correlated&#95;with: site-power-and-network; id: worker-site; independence&#95;evidence: UNKNOWN — required input or evidence; network: Single site uplink; outage test required; power: Single synthetic site; no independence proven; resource&#95;ids: compute |
| headroom&#95;percent | 50 |
| limits | No measured throughput, latency percentile, queue-drain or restore test is supplied.; Correlated power/network failures and cloud fallback capacity need independent tests.; Single workload, steady arrival rate and equal service times; no users-to-RPS conversion. |
| measured&#95;or&#95;estimated | estimated |
| method | min&#40;parallel slots, floor&#40;memory / memory per job&#41;&#41; / service time |
| recovery&#95;objectives | acceptance&#95;condition: gte; id: availability; indicator: availability; measurement: Availability percentage; test is pending; target: 99.5; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: restore; indicator: rto; measurement: Minutes to restore service; drill is pending; target: 60; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: data-loss; indicator: rpo; measurement: Minutes of potentially lost writes; drill is pending; target: 15; window: Monthly steady demand; recovery per incident; acceptance&#95;condition: lte; id: staffing; indicator: staffing; measurement: Maintenance hours per month; target: 20; window: Monthly steady demand; recovery per incident |
| restoration&#95;test&#95;refs | None declared |
| scenario&#95;id | local-only |
| scenario&#95;sha256 | 44434ad823ecd65a04baaf3d1c2627a5dae10743e4a48206dba676fbada53617 |
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
| known&#95;monthly&#95;subtotal | 720 |
| monthly&#95;total | 720 |
| one&#95;time&#95;total | 0 |
| rounding&#95;delta | 0 |
| scenario&#95;id | current |
| stale&#95;line&#95;ids | None declared |
| unknown&#95;line&#95;ids | None declared |
| unrounded&#95;monthly&#95;total | 720 |
| view | incremental&#95;cash |

### current / incremental&#95;cash cost lines

| Row ID | Resource / service | Quantity / rate / unit | Amount / currency | Source / evidence |
| --- | --- | --- | --- | --- |
| current&#124;incremental&#95;cash&#124;compute&#124;monthly | compute / Cloud workers and durable queue | 1 / 320 / month | 320 / USD | synthetic://flows/current/compute / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;incremental&#95;cash&#124;db&#124;monthly | db / Managed database | 1 / 100 / month | 100 / USD | synthetic://flows/current/db / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;incremental&#95;cash&#124;network&#124;monthly | network / Network and egress | 1 / 80 / month | 80 / USD | synthetic://flows/current/network / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;incremental&#95;cash&#124;observability&#124;monthly | observability / Monitoring and security | 1 / 40 / month | 40 / USD | synthetic://flows/current/observability / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;incremental&#95;cash&#124;operations&#124;monthly | operations / Operations labor | 1 / 180 / month | 180 / USD | synthetic://flows/current/operations / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |

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

### current / allocated&#95;tco cost lines

| Row ID | Resource / service | Quantity / rate / unit | Amount / currency | Source / evidence |
| --- | --- | --- | --- | --- |
| current&#124;allocated&#95;tco&#124;compute&#124;monthly | compute / Cloud workers and durable queue | 1 / 320 / month | 320 / USD | synthetic://flows/current/compute / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;allocated&#95;tco&#124;db&#124;monthly | db / Managed database | 1 / 100 / month | 100 / USD | synthetic://flows/current/db / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;allocated&#95;tco&#124;network&#124;monthly | network / Network and egress | 1 / 80 / month | 80 / USD | synthetic://flows/current/network / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;allocated&#95;tco&#124;observability&#124;monthly | observability / Monitoring and security | 1 / 40 / month | 40 / USD | synthetic://flows/current/observability / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| current&#124;allocated&#95;tco&#124;operations&#124;monthly | operations / Operations labor | 1 / 180 / month | 180 / USD | synthetic://flows/current/operations / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |

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

### hybrid / incremental&#95;cash cost lines

| Row ID | Resource / service | Quantity / rate / unit | Amount / currency | Source / evidence |
| --- | --- | --- | --- | --- |
| hybrid&#124;incremental&#95;cash&#124;compute&#124;monthly | compute / Cloud control and fallback | 1 / 100 / month | 100 / USD | synthetic://flows/hybrid/compute / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;incremental&#95;cash&#124;db&#124;monthly | db / Managed database | 1 / 100 / month | 100 / USD | synthetic://flows/hybrid/db / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;incremental&#95;cash&#124;network&#124;monthly | network / Network and egress | 1 / 50 / month | 50 / USD | synthetic://flows/hybrid/network / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;incremental&#95;cash&#124;observability&#124;monthly | observability / Monitoring and security | 1 / 40 / month | 40 / USD | synthetic://flows/hybrid/observability / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;incremental&#95;cash&#124;power&#124;monthly | power / Local power and connectivity | 1 / 50 / month | 50 / USD | synthetic://flows/hybrid/power / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;incremental&#95;cash&#124;operations&#124;monthly | operations / Operations labor | 1 / 160 / month | 160 / USD | synthetic://flows/hybrid/operations / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;incremental&#95;cash&#124;migration&#124;one&#95;time | migration / Transition and training | 1 / 1200 / one&#95;time | 1200 / USD | synthetic://flows/hybrid/migration / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours. |

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

### hybrid / allocated&#95;tco cost lines

| Row ID | Resource / service | Quantity / rate / unit | Amount / currency | Source / evidence |
| --- | --- | --- | --- | --- |
| hybrid&#124;allocated&#95;tco&#124;compute&#124;monthly | compute / Cloud control and fallback | 1 / 100 / month | 100 / USD | synthetic://flows/hybrid/compute / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;allocated&#95;tco&#124;db&#124;monthly | db / Managed database | 1 / 100 / month | 100 / USD | synthetic://flows/hybrid/db / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;allocated&#95;tco&#124;network&#124;monthly | network / Network and egress | 1 / 50 / month | 50 / USD | synthetic://flows/hybrid/network / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;allocated&#95;tco&#124;observability&#124;monthly | observability / Monitoring and security | 1 / 40 / month | 40 / USD | synthetic://flows/hybrid/observability / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;allocated&#95;tco&#124;power&#124;monthly | power / Local power and connectivity | 1 / 50 / month | 50 / USD | synthetic://flows/hybrid/power / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;allocated&#95;tco&#124;operations&#124;monthly | operations / Operations labor | 1 / 160 / month | 160 / USD | synthetic://flows/hybrid/operations / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;allocated&#95;tco&#124;hardware&#124;monthly | hardware / Allocated existing hardware ownership | 1 / 40 / month | 40 / USD | synthetic://flows/hybrid/hardware / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| hybrid&#124;allocated&#95;tco&#124;migration&#124;one&#95;time | migration / Transition and training | 1 / 1200 / one&#95;time | 1200 / USD | synthetic://flows/hybrid/migration / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours. |

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

### local-only / incremental&#95;cash cost lines

| Row ID | Resource / service | Quantity / rate / unit | Amount / currency | Source / evidence |
| --- | --- | --- | --- | --- |
| local-only&#124;incremental&#95;cash&#124;compute&#124;monthly | compute / Local worker and queue | 1 / 30 / month | 30 / USD | synthetic://flows/local-only/compute / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| local-only&#124;incremental&#95;cash&#124;db&#124;monthly | db / Local database | 1 / 20 / month | 20 / USD | synthetic://flows/local-only/db / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| local-only&#124;incremental&#95;cash&#124;network&#124;monthly | network / Local network | 1 / 20 / month | 20 / USD | synthetic://flows/local-only/network / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| local-only&#124;incremental&#95;cash&#124;observability&#124;monthly | observability / Monitoring | 1 / 10 / month | 10 / USD | synthetic://flows/local-only/observability / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| local-only&#124;incremental&#95;cash&#124;power&#124;monthly | power / Power | 1 / 30 / month | 30 / USD | synthetic://flows/local-only/power / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| local-only&#124;incremental&#95;cash&#124;operations&#124;monthly | operations / Operations labor | 1 / 40 / month | 40 / USD | synthetic://flows/local-only/operations / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |

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

### local-only / allocated&#95;tco cost lines

| Row ID | Resource / service | Quantity / rate / unit | Amount / currency | Source / evidence |
| --- | --- | --- | --- | --- |
| local-only&#124;allocated&#95;tco&#124;compute&#124;monthly | compute / Local worker and queue | 1 / 30 / month | 30 / USD | synthetic://flows/local-only/compute / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| local-only&#124;allocated&#95;tco&#124;db&#124;monthly | db / Local database | 1 / 20 / month | 20 / USD | synthetic://flows/local-only/db / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| local-only&#124;allocated&#95;tco&#124;network&#124;monthly | network / Local network | 1 / 20 / month | 20 / USD | synthetic://flows/local-only/network / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| local-only&#124;allocated&#95;tco&#124;observability&#124;monthly | observability / Monitoring | 1 / 10 / month | 10 / USD | synthetic://flows/local-only/observability / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| local-only&#124;allocated&#95;tco&#124;power&#124;monthly | power / Power | 1 / 30 / month | 30 / USD | synthetic://flows/local-only/power / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |
| local-only&#124;allocated&#95;tco&#124;operations&#124;monthly | operations / Operations labor | 1 / 40 / month | 40 / USD | synthetic://flows/local-only/operations / synthetic / Nominal USD, no FX or inflation; tax UNKNOWN.; Explicit synthetic full-cost allocation.; Decimal precision=50; ROUND&#95;HALF&#95;UP; inexact=false; Period: calendar&#95;month starting 2026-10; hourly quantity uses actual calendar days or explicit fixed 730 hours.; Month 1 of the hash-bound FinOps schedule; later months appear in the monthly series. |

### Comparable monthly economics

| Scenario / view | Month 1 saving | Net12 / net36 | Investment / recovery | Comparability |
| --- | --- | --- | --- | --- |
| current / incremental&#95;cash | 0 USD | 0 / 0 | 0 / 1 | True / None declared |
| current / allocated&#95;tco | 0 USD | 0 / 0 | 0 / 1 | True / None declared |
| hybrid / incremental&#95;cash | 220 USD | 1440 / 6720 | 1200 / 6 | True / Decimal inexact flag set by division/presentation; declared context preserved |
| hybrid / allocated&#95;tco | 180 USD | 960 / 5280 | 1200 / 7 | True / None declared |
| local-only / incremental&#95;cash | 570 USD | 6840 / 20520 | 0 / 1 | True / Decimal inexact flag set by division/presentation; declared context preserved |
| local-only / allocated&#95;tco | 570 USD | 6840 / 20520 | 0 / 1 | True / Decimal inexact flag set by division/presentation; declared context preserved |

### current / incremental&#95;cash monthly series

| Month | Baseline | Proposed | Saving | Cumulative net |
| --- | --- | --- | --- | --- |
| Month 1 | 720 | 720 | 0 | 0 |
| Month 2 | 720 | 720 | 0 | 0 |
| Month 3 | 720 | 720 | 0 | 0 |
| Month 4 | 720 | 720 | 0 | 0 |
| Month 5 | 720 | 720 | 0 | 0 |
| Month 6 | 720 | 720 | 0 | 0 |
| Month 7 | 720 | 720 | 0 | 0 |
| Month 8 | 720 | 720 | 0 | 0 |
| Month 9 | 720 | 720 | 0 | 0 |
| Month 10 | 720 | 720 | 0 | 0 |
| Month 11 | 720 | 720 | 0 | 0 |
| Month 12 | 720 | 720 | 0 | 0 |
| Month 13 | 720 | 720 | 0 | 0 |
| Month 14 | 720 | 720 | 0 | 0 |
| Month 15 | 720 | 720 | 0 | 0 |
| Month 16 | 720 | 720 | 0 | 0 |
| Month 17 | 720 | 720 | 0 | 0 |
| Month 18 | 720 | 720 | 0 | 0 |
| Month 19 | 720 | 720 | 0 | 0 |
| Month 20 | 720 | 720 | 0 | 0 |
| Month 21 | 720 | 720 | 0 | 0 |
| Month 22 | 720 | 720 | 0 | 0 |
| Month 23 | 720 | 720 | 0 | 0 |
| Month 24 | 720 | 720 | 0 | 0 |
| Month 25 | 720 | 720 | 0 | 0 |
| Month 26 | 720 | 720 | 0 | 0 |
| Month 27 | 720 | 720 | 0 | 0 |
| Month 28 | 720 | 720 | 0 | 0 |
| Month 29 | 720 | 720 | 0 | 0 |
| Month 30 | 720 | 720 | 0 | 0 |
| Month 31 | 720 | 720 | 0 | 0 |
| Month 32 | 720 | 720 | 0 | 0 |
| Month 33 | 720 | 720 | 0 | 0 |
| Month 34 | 720 | 720 | 0 | 0 |
| Month 35 | 720 | 720 | 0 | 0 |
| Month 36 | 720 | 720 | 0 | 0 |

### current / allocated&#95;tco monthly series

| Month | Baseline | Proposed | Saving | Cumulative net |
| --- | --- | --- | --- | --- |
| Month 1 | 720 | 720 | 0 | 0 |
| Month 2 | 720 | 720 | 0 | 0 |
| Month 3 | 720 | 720 | 0 | 0 |
| Month 4 | 720 | 720 | 0 | 0 |
| Month 5 | 720 | 720 | 0 | 0 |
| Month 6 | 720 | 720 | 0 | 0 |
| Month 7 | 720 | 720 | 0 | 0 |
| Month 8 | 720 | 720 | 0 | 0 |
| Month 9 | 720 | 720 | 0 | 0 |
| Month 10 | 720 | 720 | 0 | 0 |
| Month 11 | 720 | 720 | 0 | 0 |
| Month 12 | 720 | 720 | 0 | 0 |
| Month 13 | 720 | 720 | 0 | 0 |
| Month 14 | 720 | 720 | 0 | 0 |
| Month 15 | 720 | 720 | 0 | 0 |
| Month 16 | 720 | 720 | 0 | 0 |
| Month 17 | 720 | 720 | 0 | 0 |
| Month 18 | 720 | 720 | 0 | 0 |
| Month 19 | 720 | 720 | 0 | 0 |
| Month 20 | 720 | 720 | 0 | 0 |
| Month 21 | 720 | 720 | 0 | 0 |
| Month 22 | 720 | 720 | 0 | 0 |
| Month 23 | 720 | 720 | 0 | 0 |
| Month 24 | 720 | 720 | 0 | 0 |
| Month 25 | 720 | 720 | 0 | 0 |
| Month 26 | 720 | 720 | 0 | 0 |
| Month 27 | 720 | 720 | 0 | 0 |
| Month 28 | 720 | 720 | 0 | 0 |
| Month 29 | 720 | 720 | 0 | 0 |
| Month 30 | 720 | 720 | 0 | 0 |
| Month 31 | 720 | 720 | 0 | 0 |
| Month 32 | 720 | 720 | 0 | 0 |
| Month 33 | 720 | 720 | 0 | 0 |
| Month 34 | 720 | 720 | 0 | 0 |
| Month 35 | 720 | 720 | 0 | 0 |
| Month 36 | 720 | 720 | 0 | 0 |

### hybrid / incremental&#95;cash monthly series

| Month | Baseline | Proposed | Saving | Cumulative net |
| --- | --- | --- | --- | --- |
| Month 1 | 720 | 500 | 220 | -980 |
| Month 2 | 720 | 500 | 220 | -760 |
| Month 3 | 720 | 500 | 220 | -540 |
| Month 4 | 720 | 500 | 220 | -320 |
| Month 5 | 720 | 500 | 220 | -100 |
| Month 6 | 720 | 500 | 220 | 120 |
| Month 7 | 720 | 500 | 220 | 340 |
| Month 8 | 720 | 500 | 220 | 560 |
| Month 9 | 720 | 500 | 220 | 780 |
| Month 10 | 720 | 500 | 220 | 1000 |
| Month 11 | 720 | 500 | 220 | 1220 |
| Month 12 | 720 | 500 | 220 | 1440 |
| Month 13 | 720 | 500 | 220 | 1660 |
| Month 14 | 720 | 500 | 220 | 1880 |
| Month 15 | 720 | 500 | 220 | 2100 |
| Month 16 | 720 | 500 | 220 | 2320 |
| Month 17 | 720 | 500 | 220 | 2540 |
| Month 18 | 720 | 500 | 220 | 2760 |
| Month 19 | 720 | 500 | 220 | 2980 |
| Month 20 | 720 | 500 | 220 | 3200 |
| Month 21 | 720 | 500 | 220 | 3420 |
| Month 22 | 720 | 500 | 220 | 3640 |
| Month 23 | 720 | 500 | 220 | 3860 |
| Month 24 | 720 | 500 | 220 | 4080 |
| Month 25 | 720 | 500 | 220 | 4300 |
| Month 26 | 720 | 500 | 220 | 4520 |
| Month 27 | 720 | 500 | 220 | 4740 |
| Month 28 | 720 | 500 | 220 | 4960 |
| Month 29 | 720 | 500 | 220 | 5180 |
| Month 30 | 720 | 500 | 220 | 5400 |
| Month 31 | 720 | 500 | 220 | 5620 |
| Month 32 | 720 | 500 | 220 | 5840 |
| Month 33 | 720 | 500 | 220 | 6060 |
| Month 34 | 720 | 500 | 220 | 6280 |
| Month 35 | 720 | 500 | 220 | 6500 |
| Month 36 | 720 | 500 | 220 | 6720 |

### hybrid / allocated&#95;tco monthly series

| Month | Baseline | Proposed | Saving | Cumulative net |
| --- | --- | --- | --- | --- |
| Month 1 | 720 | 540 | 180 | -1020 |
| Month 2 | 720 | 540 | 180 | -840 |
| Month 3 | 720 | 540 | 180 | -660 |
| Month 4 | 720 | 540 | 180 | -480 |
| Month 5 | 720 | 540 | 180 | -300 |
| Month 6 | 720 | 540 | 180 | -120 |
| Month 7 | 720 | 540 | 180 | 60 |
| Month 8 | 720 | 540 | 180 | 240 |
| Month 9 | 720 | 540 | 180 | 420 |
| Month 10 | 720 | 540 | 180 | 600 |
| Month 11 | 720 | 540 | 180 | 780 |
| Month 12 | 720 | 540 | 180 | 960 |
| Month 13 | 720 | 540 | 180 | 1140 |
| Month 14 | 720 | 540 | 180 | 1320 |
| Month 15 | 720 | 540 | 180 | 1500 |
| Month 16 | 720 | 540 | 180 | 1680 |
| Month 17 | 720 | 540 | 180 | 1860 |
| Month 18 | 720 | 540 | 180 | 2040 |
| Month 19 | 720 | 540 | 180 | 2220 |
| Month 20 | 720 | 540 | 180 | 2400 |
| Month 21 | 720 | 540 | 180 | 2580 |
| Month 22 | 720 | 540 | 180 | 2760 |
| Month 23 | 720 | 540 | 180 | 2940 |
| Month 24 | 720 | 540 | 180 | 3120 |
| Month 25 | 720 | 540 | 180 | 3300 |
| Month 26 | 720 | 540 | 180 | 3480 |
| Month 27 | 720 | 540 | 180 | 3660 |
| Month 28 | 720 | 540 | 180 | 3840 |
| Month 29 | 720 | 540 | 180 | 4020 |
| Month 30 | 720 | 540 | 180 | 4200 |
| Month 31 | 720 | 540 | 180 | 4380 |
| Month 32 | 720 | 540 | 180 | 4560 |
| Month 33 | 720 | 540 | 180 | 4740 |
| Month 34 | 720 | 540 | 180 | 4920 |
| Month 35 | 720 | 540 | 180 | 5100 |
| Month 36 | 720 | 540 | 180 | 5280 |

### local-only / incremental&#95;cash monthly series

| Month | Baseline | Proposed | Saving | Cumulative net |
| --- | --- | --- | --- | --- |
| Month 1 | 720 | 150 | 570 | 570 |
| Month 2 | 720 | 150 | 570 | 1140 |
| Month 3 | 720 | 150 | 570 | 1710 |
| Month 4 | 720 | 150 | 570 | 2280 |
| Month 5 | 720 | 150 | 570 | 2850 |
| Month 6 | 720 | 150 | 570 | 3420 |
| Month 7 | 720 | 150 | 570 | 3990 |
| Month 8 | 720 | 150 | 570 | 4560 |
| Month 9 | 720 | 150 | 570 | 5130 |
| Month 10 | 720 | 150 | 570 | 5700 |
| Month 11 | 720 | 150 | 570 | 6270 |
| Month 12 | 720 | 150 | 570 | 6840 |
| Month 13 | 720 | 150 | 570 | 7410 |
| Month 14 | 720 | 150 | 570 | 7980 |
| Month 15 | 720 | 150 | 570 | 8550 |
| Month 16 | 720 | 150 | 570 | 9120 |
| Month 17 | 720 | 150 | 570 | 9690 |
| Month 18 | 720 | 150 | 570 | 10260 |
| Month 19 | 720 | 150 | 570 | 10830 |
| Month 20 | 720 | 150 | 570 | 11400 |
| Month 21 | 720 | 150 | 570 | 11970 |
| Month 22 | 720 | 150 | 570 | 12540 |
| Month 23 | 720 | 150 | 570 | 13110 |
| Month 24 | 720 | 150 | 570 | 13680 |
| Month 25 | 720 | 150 | 570 | 14250 |
| Month 26 | 720 | 150 | 570 | 14820 |
| Month 27 | 720 | 150 | 570 | 15390 |
| Month 28 | 720 | 150 | 570 | 15960 |
| Month 29 | 720 | 150 | 570 | 16530 |
| Month 30 | 720 | 150 | 570 | 17100 |
| Month 31 | 720 | 150 | 570 | 17670 |
| Month 32 | 720 | 150 | 570 | 18240 |
| Month 33 | 720 | 150 | 570 | 18810 |
| Month 34 | 720 | 150 | 570 | 19380 |
| Month 35 | 720 | 150 | 570 | 19950 |
| Month 36 | 720 | 150 | 570 | 20520 |

### local-only / allocated&#95;tco monthly series

| Month | Baseline | Proposed | Saving | Cumulative net |
| --- | --- | --- | --- | --- |
| Month 1 | 720 | 150 | 570 | 570 |
| Month 2 | 720 | 150 | 570 | 1140 |
| Month 3 | 720 | 150 | 570 | 1710 |
| Month 4 | 720 | 150 | 570 | 2280 |
| Month 5 | 720 | 150 | 570 | 2850 |
| Month 6 | 720 | 150 | 570 | 3420 |
| Month 7 | 720 | 150 | 570 | 3990 |
| Month 8 | 720 | 150 | 570 | 4560 |
| Month 9 | 720 | 150 | 570 | 5130 |
| Month 10 | 720 | 150 | 570 | 5700 |
| Month 11 | 720 | 150 | 570 | 6270 |
| Month 12 | 720 | 150 | 570 | 6840 |
| Month 13 | 720 | 150 | 570 | 7410 |
| Month 14 | 720 | 150 | 570 | 7980 |
| Month 15 | 720 | 150 | 570 | 8550 |
| Month 16 | 720 | 150 | 570 | 9120 |
| Month 17 | 720 | 150 | 570 | 9690 |
| Month 18 | 720 | 150 | 570 | 10260 |
| Month 19 | 720 | 150 | 570 | 10830 |
| Month 20 | 720 | 150 | 570 | 11400 |
| Month 21 | 720 | 150 | 570 | 11970 |
| Month 22 | 720 | 150 | 570 | 12540 |
| Month 23 | 720 | 150 | 570 | 13110 |
| Month 24 | 720 | 150 | 570 | 13680 |
| Month 25 | 720 | 150 | 570 | 14250 |
| Month 26 | 720 | 150 | 570 | 14820 |
| Month 27 | 720 | 150 | 570 | 15390 |
| Month 28 | 720 | 150 | 570 | 15960 |
| Month 29 | 720 | 150 | 570 | 16530 |
| Month 30 | 720 | 150 | 570 | 17100 |
| Month 31 | 720 | 150 | 570 | 17670 |
| Month 32 | 720 | 150 | 570 | 18240 |
| Month 33 | 720 | 150 | 570 | 18810 |
| Month 34 | 720 | 150 | 570 | 19380 |
| Month 35 | 720 | 150 | 570 | 19950 |
| Month 36 | 720 | 150 | 570 | 20520 |

### Sensitivity

| Variable | Condition | Effect |
| --- | --- | --- |
| hybrid / incremental&#95;cash / 12 months | If proposal cost increases by USD 1440 over 12 months with other assumptions fixed. | Modeled net saving reaches zero; this is a threshold, not a probability. |
| hybrid / incremental&#95;cash / 36 months | If proposal cost increases by USD 6720 over 36 months with other assumptions fixed. | Modeled net saving reaches zero; this is a threshold, not a probability. |
| hybrid / allocated&#95;tco / 12 months | If proposal cost increases by USD 960 over 12 months with other assumptions fixed. | Modeled net saving reaches zero; this is a threshold, not a probability. |
| hybrid / allocated&#95;tco / 36 months | If proposal cost increases by USD 5280 over 36 months with other assumptions fixed. | Modeled net saving reaches zero; this is a threshold, not a probability. |
| local-only / incremental&#95;cash / 12 months | If proposal cost increases by USD 6840 over 12 months with other assumptions fixed. | Modeled net saving reaches zero; this is a threshold, not a probability. |
| local-only / incremental&#95;cash / 36 months | If proposal cost increases by USD 20520 over 36 months with other assumptions fixed. | Modeled net saving reaches zero; this is a threshold, not a probability. |
| local-only / allocated&#95;tco / 12 months | If proposal cost increases by USD 6840 over 12 months with other assumptions fixed. | Modeled net saving reaches zero; this is a threshold, not a probability. |
| local-only / allocated&#95;tco / 36 months | If proposal cost increases by USD 20520 over 36 months with other assumptions fixed. | Modeled net saving reaches zero; this is a threshold, not a probability. |
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

### hybrid / inventory

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

### hybrid / identity

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

### hybrid / sandbox

| Step field | Procedure |
| --- | --- |
| Action | In a separately approved nonproduction sandbox, configure durable jobs, idempotent consumers and managed DB backups |
| Artifact | UNKNOWN — required input or evidence |
| Expected result | Repeatable job processing with duplicate suppression |
| Id | sandbox |
| Owner | Platform engineer |
| Parameters | name: Environment; required: true; value: Nonproduction only; actual account, region and names remain required inputs; name: Database hostname; required: true; value: UNKNOWN — required input or evidence; name: Database port; required: true; value: 5432; name: Database TLS mode; required: true; value: verify-full; name: Queue endpoint; required: true; value: UNKNOWN — required input or evidence; name: Queue transport; required: true; value: HTTPS on port 443; AWS remains simulated; name: Queue visibility timeout seconds; required: true; value: UNKNOWN — required input or evidence; name: Worker parallel slots; required: true; value: 4; name: Database maximum pool connections; required: true; value: 10; name: Idempotency key; required: true; value: job&#95;id; persist before acknowledgment; name: Acknowledgment order; required: true; value: Commit database transaction, then acknowledge queue message; name: Retry policy; required: true; value: Bounded retries and dead-letter handling; counts require workload review; name: Application and provider versions; required: true; value: UNKNOWN — required input or evidence |
| Prerequisites | identity |
| Required inputs | Approved account and region; Actual resource names and versions; Independent reviewer; Separate execution approval; Measured worst-case job duration for visibility timeout; Validated backup and retention settings; Compatible application, database and queue versions |
| Stop condition | Stop on lost jobs, duplicate side effects or untested backup |
| Validation | Replay synthetic jobs, interrupt consumer before acknowledgment, verify deduplication and retained queue |

### hybrid / capacity

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

### hybrid / restore

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

### hybrid / approval

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

### hybrid migration and rollback

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

### hybrid operating model

| Field | Value |
| --- | --- |
| Alerts | Queue age and depth; Consumer errors and retries; Database connection pool; Backup age; Local uplink health |
| Fallback | Retain the durable cloud queue and restore managed consumers; cloud fallback is included in the proposed cost. |
| Maintenance hours month | 16 |
| On call | Business-hours response; verify incident coverage |
| Owner | Platform engineer |

### local-only operating model

| Field | Value |
| --- | --- |
| Alerts | Queue age and depth; Consumer errors and retries; Database connection pool; Backup age; Local uplink health |
| Fallback | No independent fallback is modeled; local power and network are one failure domain. |
| Maintenance hours month | 18 |
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
