# Third-party notices

Original Starbots code is licensed under Apache-2.0. Dependencies keep their own licenses; no third-party source is relicensed or vendored.

## Python dependencies (installed from PyPI, not bundled)

Exact versions and SHA-256 hashes are in `requirements-runtime.lock`, `requirements-dev.lock` and `requirements-simulation.lock`.

| Package | Use | License |
| --- | --- | --- |
| jsonschema, attrs, jsonschema-specifications, referencing, rpds-py | Runtime | MIT |
| typing-extensions | Runtime | PSF-2.0 |
| setuptools, wheel | Build | MIT |
| packaging | Build | Apache-2.0 OR BSD-2-Clause |
| cryptography | Optional SQS simulator | Apache-2.0 OR BSD-3-Clause |
| cffi | Optional SQS simulator | MIT-0 |
| pycparser | Optional SQS simulator | BSD-3-Clause |

The locks target CPython 3.12 on Windows x64 (including platform-specific wheel hashes). Other platforms need their own reviewed hashes.

## Starbots Security Skills protocol

`vendor/security-protocol/` and `vendor/local-review-policy/` (mirrored in `src/starbots_hybrid/data/`) are byte-identical, Apache-2.0 data files from [Starbots Security Skills](https://github.com/Starbots-devv/security-skills), pinned by SHA-256.
