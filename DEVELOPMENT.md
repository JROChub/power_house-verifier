# Development Guide

This document describes how to set up a development environment, run tests, and contribute to `power_house-verifier`.

## Environment Setup

```bash
git clone https://github.com/JROChub/power_house-verifier.git
cd power_house-verifier
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

The package has no mandatory external dependencies for core functionality. High-precision mode uses only the standard-library `decimal` module.

## Running Tests

```bash
python -m pytest
```

All tests are deterministic. No random seeding is required.

## Running Benchmarks

```bash
python benchmarks/run_benchmarks.py
```

Results are written to stdout. Example output is stored in `benchmarks/results.txt`.

## Code Style

- Follow PEP 8 with a maximum line length of 100 characters.
- All public functions must have type hints and docstrings.
- Prefer explicit, readable code over clever one-liners.
- Log-space arithmetic should be used wherever numerical stability is a concern.

## Adding New Scenarios

Register new scenarios in `power_house_verifier/engine.py` inside the `get_scenario_params()` function. Each scenario should return a `VerificationParams` instance with well-chosen defaults.

## Extending the Adversarial Module

New stress tests or sensitivity analyses should be added to `power_house_verifier/adversarial.py`. The `run_adversarial_analysis()` function serves as the main entry point and should remain the primary public interface.

## Releasing

1. Update `__version__` in `power_house_verifier/__init__.py`.
2. Update `CHANGELOG.md` (if present) with notable changes.
3. Tag the release on GitHub.

## Questions

Open an issue on the GitHub repository for bugs, feature requests, or clarification.