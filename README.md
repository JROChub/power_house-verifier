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
- `adversarial` command for parameter sensitivity and correlated-failure analysis
- Multiple scenarios (pollution, asthma, ventilator, drug, copd, general)
- JSON output for integration and tooling
- Comprehensive test suite

## Real Data Demo (Flagship Example)

`examples/compound_verification_demo.py` demonstrates the core capability on **real-world data**:

```bash
python examples/compound_verification_demo.py --data path/to/real_air_quality.csv --scale region
```

The script:
- Loads real sensor/measurement data (CSV)
- Groups measurements by scale (city → region → larger area)
- Runs verification treating real values + uncertainty as probabilistic checks
- Shows how verification probability compounds across real scales

This is the concrete demonstration that rigorous, high-confidence verification of large-scale real systems is now practical on ordinary hardware.

## Performance

All core operations are designed to remain practical on ordinary hardware even at large scale.

Example benchmark results (consumer laptop, Python 3.9+, 5-run average):

```
Scenario        Verify (ms)   Scaling (ms)   Adversarial (ms)
Small                 0.312          0.085             2.140
Medium                0.418          0.112             2.870
Large                 0.651          0.168             4.210
High-Precision        1.240          0.195             5.890
```

See `benchmarks/run_benchmarks.py` and `benchmarks/results.txt` for methodology and reproduction instructions.

## Robustness & Adversarial Testing

The project includes a dedicated adversarial analysis module to stress-test the core assumptions of the probabilistic closure model.

### Available Analysis

- **Parameter Sensitivity**: Measures degradation when key parameters (`p`, `k`, `q`) are varied.
- **Correlated Failures**: Simulates reduced independence between checks.
- **Extreme Regime Notes**: Identifies conditions where results may become fragile.

### Usage

```bash
power_house-verifier adversarial --scenario general
power_house-verifier adversarial --scenario pollution --output json
```

The output includes base probability, observed degradation, correlated-failure impact, and a qualitative robustness assessment (High / Moderate / Low).

### Current Assessment

The model shows **moderate to high robustness** under moderate parameter variation and correlated failure assumptions. However, like all probabilistic models, it assumes a baseline level of independence and accurate parameter estimation. Results in very low-probability regimes or with highly correlated checks should be interpreted with appropriate caution.

## How to Extend and Cite

### Extending the Engine

Core logic resides in `power_house_verifier/engine.py`. Primary extension points include:

- Registration of new scenarios via `get_scenario_params()`
- Custom sensitivity or adversarial analyses in `adversarial.py`
- Replacement or augmentation of probability functions while preserving the log-space interface

All public functions are documented with type hints and docstrings. The design prioritizes determinism and numerical stability.

### Citation

If you use this software in academic or technical work, please cite:

```bibtex
@software{power_house_verifier,
  author = {MFENX},
  title  = {power_house-verifier: High-scale probabilistic verification with compounding efficiency},
  url    = {https://github.com/JROChub/power_house-verifier},
  year   = {2026}
}
```

### Reproducibility

All probability calculations are deterministic. No random sampling is employed. Core algorithms rely on closed-form expressions evaluated in log-space.

Tested environments: Python 3.9+. Core functionality has no external dependencies. High-precision mode uses the standard-library `decimal` module at 120-bit precision.

To reproduce results:
```bash
python -m pytest
python benchmarks/run_benchmarks.py
```

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