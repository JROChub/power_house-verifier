# power_house-verifier

High-scale probabilistic verification engine using log-space arithmetic for numerical stability.

## Overview

This package implements an efficient method for computing verification and finalization probabilities at very large scales using closed-form mathematics in log-space. It is designed for scenarios where standard floating-point calculations become unstable.

## Mathematical Approach

The engine uses log-space computations to maintain precision across extreme probability ranges. Key functions include:

- `verification_probability_log()` — Returns log-probability for numerical stability
- `verification_probability()` — Converts to linear probability when needed
- `expected_rounds()` — Computes expected number of rounds using finite geometric series

All calculations are deterministic and O(r) time complexity.

## Features

- Log-space arithmetic for extreme scale stability
- Optional high-precision mode using decimal arithmetic
- Multiple pre-configured scenarios
- JSON and text output modes
- Comprehensive test coverage

## Installation

```bash
pip install -e .
```

## Usage

```bash
power_house-verifier verify --scenario pollution --output json
power_house-verifier compare --scenario asthma
```

## Testing

```bash
python -m pytest
```

## License

MIT