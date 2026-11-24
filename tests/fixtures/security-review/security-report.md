# Starbots local security review

Scope: Actual local synthetic fixtures only; no production, certification or execution approval

Readiness: BLOCKED

Hashes establish integrity, not authorship or execution approval.
No finding does not mean secure. Real model/host evaluations were not performed.

| Control | State | Evidence |
| --- | --- | --- |
| SB-AUTH | UNKNOWN | evidence-SB-AUTH |
| SB-RLS | UNKNOWN | evidence-SB-RLS |
| SB-SECRETS | UNKNOWN | evidence-SB-SECRETS |
| SB-DEPENDENCIES | UNKNOWN | evidence-SB-DEPENDENCIES |
| SB-IAC | UNKNOWN | evidence-SB-IAC |
| SB-AGENT-BOUNDARY | PASS | evidence-SB-AGENT-BOUNDARY |

Findings: 0
- api-fixture: tool did not complete successfully
- postgresql-rls: tool did not complete successfully
- gitleaks: tool did not complete successfully
- osv-scanner: tool did not complete successfully
- trivy: tool did not complete successfully
- Required coverage is missing
- SB-AUTH: control does not pass
- SB-RLS: control does not pass
- SB-SECRETS: control does not pass
- SB-DEPENDENCIES: control does not pass
- SB-IAC: control does not pass
