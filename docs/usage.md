# Usage and input format

Install the package as described in the [README](../README.md). The analysis needs no cloud credentials, network access, language model or Security package. Protocol data from Starbots Security Skills is vendored and byte-pinned.

## Analyze your own (or a fictional) company

1. Copy `examples/hybrid-saving` to a new local directory. Do not put confidential data in tracked examples.
2. Edit `profile.json`: goals, mandatory service objectives, residency, the workload, budget, team and open questions. A bundle models one steady-state workload. Keep `synthetic: true` for a fictional exercise.
3. Edit every scenario: resources, directed connections, matched mandatory objectives, capacity inputs, costs, implementation parameters and recovery. Every profile objective is mandatory in each candidate and must keep its ID, dimension, rule and target. Unmeasured observations remain assumptions. Reference actual resource IDs; action groups cannot overlap.
4. Edit the dated cost snapshots. Each candidate uses one snapshot, one comparable currency per view and matching period definitions. Quantities and rates are decimal strings, never JSON floats. Recurring and one-time items stay separate. A `null` rate or an expired validity makes the total incomplete, not zero. The synthetic example explicitly excludes taxes and FX; real material exclusions must set `material: true`.
5. Seal, then validate and analyze:

```powershell
.venv/Scripts/sb-hybrid.exe seal-bundle --bundle <copied-input>/bundle.json
.venv/Scripts/sb-hybrid.exe validate --bundle <copied-input>/bundle.json
.venv/Scripts/sb-hybrid.exe analyze --bundle <copied-input>/bundle.json --as-of 2026-10-17T00:00:00Z --policy offline-demo-1.0.0 --locale en --output-dir .local-output/my-company
```

`seal-bundle` only refreshes byte hashes and binds scenarios to the edited profile and the current security protocol. It never signs, measures, repairs a requirement or approves execution. Version or identity mismatches, bad hashes, unsafe paths and incompatible periods fail with a JSON error code and exit code 2. A valid provisional report exits 0 while still declaring UNKNOWN items and blocked execution.

The profile's `service_objectives` use `indicator` = a supported constraint dimension and `acceptance_condition` = `equals`, `includes`, `lte` or `gte`; `target` is the exact threshold. Candidates may add extra restrictions. The tool does not infer a provider catalog or discover alternatives on its own.

Use `--policy strict-analysis-1.0.0` to keep unmeasured capacity UNKNOWN, so no recommendation is made from capacity assumptions.

## Review and regenerate

Open `dossier.html`, then consult `executive-summary.md`, `implementation-guide.md`, `evaluation.json`, `costs.csv` and `cashflow.csv`. The two SVG diagrams are also embedded in the HTML. `subject-manifest.json` covers the immutable proposal inputs, the completed capacity models and the control profile; its identity depends only on those proposal artifacts. `artifact-manifest.json` covers the complete exported report except itself. SHA-256 provides integrity; these files are not signatures or approvals.

```powershell
.venv/Scripts/sb-hybrid.exe dossier --evaluation .local-output/my-company/evaluation.json --locale en --audience both --output-dir .local-output/my-company-copy
```

The complete report directory is required. Every manifest artifact is verified before regeneration; no prices are queried or recalculated, and the same result reproduces the same bytes. Existing output directories and link or junction traversal are refused. A failed local write can leave an incomplete directory; use a new directory after resolving the error.

## Outputs and rendering rules

`evaluation.json` is the only source for every rendered file. CSV, Markdown and HTML keep each scenario, view, line and period ID and amount from the JSON; rendering performs no new arithmetic. Cash and allocated TCO stay separate. Currency rounding uses `ROUND_HALF_UP` with 50-digit decimal precision, and line totals, unrounded totals and rounding deltas stay visible.

Each implementation step keeps its owner, prerequisites, parameters, required inputs, expected result, validation and stop condition. Each connection keeps its direction, port and protocol, TLS, identity and permissions, route, secret references and test. Real hostnames, timeouts, versions and identities remain required inputs instead of invented defaults.

The HTML uses local static CSS, inline SVG, escaped imported text and a restrictive Content Security Policy; it loads no fonts, scripts or remote assets. Markdown escapes imported HTML and link syntax. CSV prefixes formula-like cells with an apostrophe; treat those cells as text. `shareable-summary.html` keeps only a fixed allowlist of decision status, synthetic flag and numeric commercial values, and `redaction-manifest.json` lists the removed categories. That is not an anonymity guarantee, and nothing is published automatically.
