# power_house-verifier

**High-scale probabilistic verification using log-space arithmetic**

This package provides a numerically stable implementation of probabilistic closure for computing verification and finalization probabilities at very large scales.

## Purpose

The goal is to enable efficient, exact probability calculations for verification processes involving large numbers of independent checks, where traditional methods become computationally infeasible or numerically unstable.

## Mathematical Foundation

The method is based on repeated independent probabilistic checks. All calculations are performed in log-space to maintain precision across extreme probability ranges.

### Core Formulas

**Per-participant success probability:**

\[
\text{per_participant}(p, q) = 1 - (1 - p)^{q+1}
\]

**Per-round success probability:**

\[
\text{per_round}(k, p, q) = [\text{per_participant}(p, q)]^k
\]

**Verification probability after \( r \) rounds (log-space):**

\[
\log P = \log(1 - e^{r \cdot \log(\text{per_round})})
\]

**Expected number of rounds:**

Computed via finite-horizon geometric distribution summation.

All derivations and edge-case handling are implemented directly in the source code.

## Key Features

- Log-space arithmetic for numerical stability at extreme scales
- Optional high-precision mode using arbitrary-precision arithmetic
- Deterministic results (no sampling)
- Multiple pre-configured scenarios
- JSON output for integration
- Comprehensive test suite

## Limitations (Known)

- Assumes statistical independence between checks
- Parameter estimation (\( p \), \( q \)) must be done externally
- Not a substitute for formal verification in safety-critical systems
- Floating-point precision limits still apply in extreme regimes (mitigated by log-space and high-precision modes)

## Installation

```bash
pip install git+https://github.com/JROChub/power_house-verifier.git
```

## Usage

```bash
power_house-verifier verify --scenario asthma
power_house-verifier verify --scenario pollution --output json
power_house-verifier compare --scenario copd
```

## Testing

```bash
python -m pytest
```

## License

MIT License

## Citation

If used in academic work, please cite the repository.