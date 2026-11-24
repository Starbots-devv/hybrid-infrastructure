# Cost methodology

The tool compares a finite set of user-supplied architectures. Every rate in the bundled examples is **synthetic**. The product does not fetch provider prices, estimate a vendor quote, infer a tax rule, or measure production demand.

## Reproducible inputs

The original `CostSnapshot` contract remains at version 1.0.0. A bundle with `schema_version: "1.1.0"` adds one `finops` file reference per scenario. Each reference has a relative path and SHA-256 digest; the report's input and subject manifests bind the exact bytes. The FinOps plan format is `starbots-finops-1`, with matching client, project, scenario, currency, start month, observation time, expiry, source URI, tax status, line rules and promotions. Version 1.0.0 bundles keep their original constant-demand behavior.

Plans cover 36 explicit months. A line segment names months 1–36 and can override quantity or rate, specify compound monthly quantity growth, marginal tiers, block pricing or a minimum. Unspecified months use the dated base snapshot. Hourly rates multiply by actual calendar days × 24 or by an explicitly selected fixed 730-hour month. Decimal arithmetic uses 50 digits and `ROUND_HALF_UP`; displayed lines are rounded to the currency's minor unit before summing. `cashflow.csv`, JSON, Markdown and HTML all read the same calculated monthly series. A missing or stale price blocks comparison; it is never treated as zero.

Promotions state eligible line IDs, eligible months, monthly cap and a total pool. A pool is consumed once per alternative, since alternatives are mutually exclusive. Multiple credits cannot reduce the same line below zero. Month after expiry or exhaustion returns to the regular rate. A noncancelable commitment must appear as its own residual cost line during its remaining months; stopping a replacement resource does not remove that obligation.

The cash view includes incremental spending and migration. Allocated TCO adds ownership or depreciation as an allocation. Views are compared separately and never summed. A historical purchase is excluded from new cash spending; if its depreciation appears in TCO, the same purchase must not be charged again in that view. Allocation IDs must be unique within each view. The input owner must document unavoidable charges, overlap, operations, transfer, support, backup, fallback, security and migration as applicable. An omitted material category makes the result incomplete.

An optional `asset_rules` entry links a cash-only purchase line (or `null` for previously owned equipment) to one TCO-only depreciation line, purchase cost, residual value and a stated life covering the model horizon. The monthly depreciation must reconcile to `(purchase cost − residual value) / life months` at the currency minor unit. Demand overrides cannot change that line. These declared rules guard a named asset; they do not infer undisclosed historical purchases.

`net[h] = Σ(baseline monthly cost[t] − proposed monthly cost[t]) − incremental one-time cost`, for months 1 through `h`. The first cumulative nonnegative month is reported as the initial break-even, while the entire monthly series shows any later reversal. Percentages are omitted when the baseline is zero. Ranking uses allocated TCO over the requested horizon only for candidates whose mandatory constraints and cost data remain comparable. A modeled conditional recommendation grants no execution authority.

The sensitivity table uses those same 12- and 36-month net results. For each nonbaseline alternative and accounting view, it states the exact cumulative proposal-cost increase that would erase a modeled saving, or the decrease needed to erase a loss, while all other assumptions stay fixed. Zero-net and incomparable cases have explicit nonnumeric states. This one-variable threshold is deterministic; it is not a probability, price forecast, or substitute for workload and provider evidence.

FX is optional and explicit: a versioned `fx` quote specifies source and target currency, multiply direction, positive rate, spread percent, observation, expiry and source URI. Only matching source-currency lines convert. An absent, expired, unused or incompatible quote blocks the comparison. The supported tax status is `pre_tax_unknown`; the result is not an after-tax estimate. No implicit FX or tax conversion occurs.

## Manual provider context

These prompts describe information a reviewer must supply; they are not claims that a particular service or price is available.

| Context | Relevant role | Inputs to verify manually |
|---|---|---|
| AWS | Compute, queue, managed database, network or fallback where used | Region, quota, minimum, transfer, identity, backup and operations |
| Cloudflare | DNS, CDN, edge or tunnel where used | Runtime limits, data location, route, TLS and origin dependency |
| Hetzner | VM, dedicated server or storage where used | Region, private/interprovider traffic, IP, backup and operation |
| DigitalOcean | VM, application or managed database where used | Region, plan, backup, availability and connection limits |
| Supabase | PostgreSQL, Auth or Storage where used | Region, RLS roles, connections, backup, transfer and used features |
| Vercel | Frontend and functions where used | Region, runtime duration, quotas and transfer; resident workers require separate evidence |
| On-premise | Recoverable worker or optional compute | Measured hardware, energy, UPS, ISP, maintenance, latency and budgeted fallback |

## Scope

The example savings are outputs of synthetic inputs; they do not describe a return from using this tool. The release excludes live pricing, billing ingestion, cloud inventory, tax engines, automatic provider provisioning and a production AWS executor. A customer estimate needs current quotes, measured capacity, dated complete costs, restore evidence and an independently verified security review before an implementation decision.
