# Contributing

Thanks for your interest. Issues and pull requests are welcome.

- Work in an isolated Python 3.12 environment installed from the hash-locked requirement files (including `requirements-simulation.lock` for the simulator tests).
- Use synthetic data only. Keep customer data, credentials, signing keys, generated state and virtual environments out of Git.
- Add a failing test for a behavior change, then make it pass. Run both `python -m unittest discover -s tests -p "test_*.py" -v` and `python -m unittest discover -s tests/integration -p "test_*.py" -v` before opening a pull request.
- Keep cost and capacity assumptions explicit. New cost inputs need a dated source, currency, period, tax status and allocation semantics; never replace an unknown price with zero.
- Keep the versioned contracts and the vendored Security protocol byte-identical to their pins. If you change example inputs, regenerate them with `tools/make_demo.py` and `examples/flows/build_examples.py`, reseal, and regenerate the example reports.
- Report security issues through [SECURITY.md](SECURITY.md), not in public issues.

By contributing you agree that your contribution is licensed under the Apache License 2.0.
