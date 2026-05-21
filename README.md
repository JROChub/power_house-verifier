# power_house-verifier

**High-scale probabilistic verification with compounding efficiency**

A numerically stable implementation of probabilistic closure for verification at extreme scales. Small per-round probabilistic effort can compound into verification of massive systems when the protocol is structured correctly.

## Core Insight

Massive systems may be verifiable with tiny probabilistic effort if verification compounds correctly.

This is not merely an optimization. It is a different way of thinking about scaling verification: instead of linear growth in effort with system size, properly designed compounding allows verification cost to remain small even as the underlying system grows to planetary or sextillion scale.

This idea has the potential to reshape how people think about what is computationally feasible in verification, consensus, and large-scale systems.

## Mathematical Foundation

The engine uses log-space arithmetic to compute exact verification probabilities efficiently.

Key operations:

- Per-participant success: `1 - (1 - p)^(q+1)`
- Per-round success: `(per_participant)^k`
- Verification probability after r rounds (log-space): `log(1 - exp(r * log(per_round)))`
- Expected rounds via finite geometric distribution

All calculations are deterministic and numerically stable even at extreme scales.

## Features

- Log-space arithmetic for extreme numerical stability
- Optional high-precision mode (decimal arithmetic)
- `scaling` command that quantifies compounding effect and rounds needed for target certainty
- Multiple scenarios (pollution, asthma, ventilator, drug, copd, general)
- JSON output for integration and tooling
- Comprehensive test suite

## Usage

```bash
power_house-verifier scaling --scenario general
power_house-verifier verify --scenario pollution --output json
power_house-verifier adversarial --scenario general
```

Example `scaling` output shows rounds required for 99% and 99.999% certainty, the compounding factor, and qualitative asymptotic behavior.

## Robustness & Adversarial Testing

The project includes a dedicated adversarial analysis module to stress-test the core assumptions of the probabilistic closure model.

### Available Analysis

- **Parameter Sensitivity**: Measures how much verification probability degrades when key parameters (`p`, `k`, `q`) are varied.
- **Correlated Failures**: Simulates reduced independence between checks and reports the impact on overall probability.
- **Extreme Regime Notes**: Flags conditions where results may become fragile (very low base probability, low check count per round, etc.).

### Usage

```bash
power_house-verifier adversarial --scenario general
power_house-verifier adversarial --scenario pollution --output json
```

The output includes:
- Base probability under nominal parameters
- Degradation observed across tested parameter ranges
- Impact of correlated failures
- Qualitative robustness assessment ("High / Moderate / Low")

### Current Assessment

The model shows **moderate to high robustness** under moderate parameter variation and correlated failure assumptions. However, like all probabilistic models, it assumes a baseline level of independence and accurate parameter estimation. Results in very low-probability regimes or with highly correlated checks should be interpreted with caution.

This adversarial tooling is intended to make the limitations of the approach explicit and to support future hardening of the protocol.

## Current Status & Path Forward

This project is no longer dismissible as probabilistic theater. It demonstrates a real, efficient mechanism for high-scale verification.

It will become influential if:
- The protocol is hardened
- Adversarial assumptions are rigorously tested
- Performance claims survive real deployment
- Outside researchers engage with it

The core primitive is sound. The work now is to make it robust, reproducible, and accessible.

## Installation

```bash
pip install git+https://github.com/JROChub/power_house-verifier.git
```

## Testing

```bash
python -m pytest
```

## License

MIT License