# power_house-verifier

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)](https://www.docker.com/)

**High-scale probabilistic verification with compounding efficiency**

## Quick Start

### Using Docker (Recommended)

```bash
git clone https://github.com/JROChub/power_house-verifier.git
cd power_house-verifier
docker build -t power-house-verifier .
docker run --rm power-house-verifier
```

This runs the flagship real-data demo immediately with no additional setup.

### Using Python Directly

```bash
git clone https://github.com/JROChub/power_house-verifier.git
cd power_house-verifier
pip install -e .
python examples/compound_verification_demo.py
```

Both methods run the professional demo showing rigorous verification on real measurement data with baseline comparison.

## Vision and Contribution

This work introduces and implements a computationally efficient method for rigorous probabilistic verification at scales that have historically been intractable. By modeling verification as a compounding process and performing all calculations in log-space, the approach enables exact probability computations over extremely large effective state spaces while remaining practical on ordinary hardware.

The central contribution is a demonstration that verification cost need not scale linearly with system size when the verification protocol is structured to exploit compounding. This property has direct implications for any domain in which high-confidence assessment of large, complex systems is required, including environmental monitoring, distributed infrastructure, scientific simulation, and multi-agent or multi-planetary systems.

## Significance

Traditional approaches to large-scale verification have generally relied on either exhaustive enumeration, heavy Monte Carlo sampling, or substantial approximation. Each of these strategies imposes significant computational cost or sacrifices rigor, particularly in the tails of the distribution and under adversarial conditions.

The method presented here offers an alternative formulation in which verification probability compounds across independent checks and rounds. When properly parameterized, this compounding behavior allows strong probabilistic guarantees to be obtained with relatively modest per-round effort, even as the underlying system grows to planetary or greater scale. The approach is deterministic, numerically stable, and admits direct adversarial analysis.

While the current implementation focuses on a specific class of verification problems, the underlying primitive is general. It provides a foundation for future work on verifiable large-scale systems.

## Mathematical Foundation

The engine uses log-space arithmetic to compute exact verification probabilities efficiently.

Key operations:

- Per-participant success: `1 - (1 - p)^(q+1)`
- Per-round success: `(per_participant)^k`
- Verification probability after r rounds (log-space): `log(1 - exp(r * log(per_round)))`
- Expected rounds via finite geometric distribution

All calculations are deterministic and numerically stable even at extreme scales.

## Assumptions, Bounds, and Limitations

The method implemented in this package rests on several modeling assumptions:

- **Independence**: Individual checks within and across rounds are assumed to be statistically independent. Violations of this assumption (e.g., correlated sensor failures or systematic biases) can degrade the accuracy of the computed probabilities.
- **Parameter Accuracy**: The input parameters \(p\) (base success probability) and \(q\) (quality factor) must be reasonably well-estimated from domain knowledge or data. Significant misestimation directly affects the reliability of the output probabilities.
- **Stationarity**: The underlying success probabilities are assumed to be constant across rounds unless explicitly modified by the user.

### Known Bounds and Behavior

- The verification probability is monotonically non-decreasing in the number of rounds \(r\) and checks per round \(k\).
- In the limit of large \(r\) or strong per-round success probability, the verification probability converges to 1.
- The expected number of rounds is bounded above by the maximum allowed rounds \(r\).
- Log-space evaluation ensures numerical stability for very small per-round success probabilities; however, floating-point precision limits still apply in extreme regimes.

### Limitations

- The current formulation does not natively support dependent or hierarchical check structures.
- It is not a substitute for formal verification methods in safety-critical systems where absolute guarantees are required.
- Performance and accuracy in very low base-probability regimes (\(p \ll 0.5\)) or under strong correlation remain areas of active refinement.

Users are encouraged to apply the included adversarial analysis tools to assess sensitivity to these assumptions in their specific application domain.

## Features

- Log-space arithmetic for extreme numerical stability
- Optional high-precision mode (decimal arithmetic)
- `scaling` command that quantifies compounding effect and rounds needed for target certainty
- `adversarial` command for parameter sensitivity and correlated-failure analysis
- Multiple scenarios (pollution, asthma, ventilator, drug, copd, general)
- JSON output for integration and tooling
- Comprehensive test suite

## Real Data Demo (Primary Example)

`examples/compound_verification_demo.py` is the flagship demonstration. It runs **rigorous verification on real measurement data**:

```bash
python examples/compound_verification_demo.py --data path/to/real_data.csv --group region
```

The script:
- Loads and validates real CSV data (measurements + uncertainty)
- Groups data by scale (e.g. city → region)
- Runs verification treating real values as probabilistic checks
- Demonstrates how verification probability compounds across real scales

This is currently the clearest way to experience the core breakthrough: high-confidence verification of real large-scale systems is now practical on ordinary hardware.

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