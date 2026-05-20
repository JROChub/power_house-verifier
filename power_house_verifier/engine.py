"""
power_house-verifier Engine

Numerically stable implementation using log-space arithmetic
for high-scale verification probability calculations.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List
import math
from decimal import Decimal, getcontext

getcontext().prec = 80


@dataclass
class VerificationParams:
    k: int = 100
    p: float = 0.65
    q: int = 6
    r: int = 8
    high_precision: bool = False


@dataclass
class VerificationResult:
    probability: float
    log_probability: float
    expected_rounds: float
    schedule: List[dict]
    theoretical_bound: float


def _log_per_participant(p: float, q: int) -> float:
    p = max(1e-12, min(1.0 - 1e-12, p))
    return math.log1p(-math.pow(1.0 - p, q + 1))


def _log_per_round(k: int, p: float, q: int) -> float:
    return _log_per_participant(p, q) * max(1, k)


def verification_probability_log(r: int, k: int, p: float, q: int) -> float:
    r = max(1, r)
    log_pr = _log_per_round(k, p, q)
    if log_pr >= 0:
        return 0.0
    return math.log1p(-math.exp(r * log_pr))


def verification_probability(r: int, k: int, p: float, q: int, high_precision: bool = False) -> float:
    if high_precision:
        getcontext().prec = 120
        log_pr = _log_per_round(k, p, q)
        return float(Decimal(1) - Decimal(-1).exp(Decimal(r) * Decimal(log_pr)))
    return math.exp(verification_probability_log(r, k, p, q))


def expected_rounds(r: int, k: int, p: float, q: int) -> float:
    log_pr = _log_per_round(k, p, q)
    if log_pr >= 0:
        return 1.0
    pr = math.exp(log_pr)
    expected = 0.0
    fail = 1.0
    for i in range(1, r + 1):
        success = fail * pr
        expected += i * success
        fail *= (1.0 - pr)
    return expected + r * fail


def run_verification(params: VerificationParams) -> VerificationResult:
    prob = verification_probability(params.r, params.k, params.p, params.q, params.high_precision)
    log_prob = verification_probability_log(params.r, params.k, params.p, params.q)
    exp = expected_rounds(params.r, params.k, params.p, params.q)

    schedule = []
    for i in range(1, params.r + 1):
        p_eff = verification_probability(i, params.k, params.p, params.q)
        schedule.append({
            "round": i,
            "probability": round(p_eff, 12),
            "log_probability": round(verification_probability_log(i, params.k, params.p, params.q), 8)
        })

    log_pr = _log_per_round(params.k, params.p, params.q)
    bound = 1.0 - math.exp(-params.r * math.exp(log_pr))

    return VerificationResult(
        probability=round(prob, 12),
        log_probability=round(log_prob, 8),
        expected_rounds=round(exp, 4),
        schedule=schedule,
        theoretical_bound=round(bound, 12)
    )


def get_scenario_params(name: str) -> VerificationParams:
    scenarios = {
        "pollution": VerificationParams(k=90, p=0.62, q=5, r=5),
        "asthma": VerificationParams(k=70, p=0.58, q=4, r=6),
        "ventilator": VerificationParams(k=85, p=0.65, q=6, r=5),
        "drug": VerificationParams(k=75, p=0.60, q=5, r=6),
        "copd": VerificationParams(k=80, p=0.57, q=5, r=7),
        "general": VerificationParams(k=100, p=0.65, q=6, r=8),
    }
    return scenarios.get(name, scenarios["general"])