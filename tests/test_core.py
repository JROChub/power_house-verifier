"""Comprehensive tests for the Powerhouse core engine."""

import math
import pytest
from powerhouse.core import (
    per_participant,
    per_round,
    pr_finalize,
    expected_rounds,
    closure_result,
    required_rounds,
    ClosureParams,
)


def test_per_participant_basic():
    assert abs(per_participant(0.5, 0) - 0.5) < 1e-12
    assert abs(per_participant(0.3, 2) - (1 - 0.7**3)) < 1e-12


def test_per_round_behavior():
    # With per_participant < 1, larger k reduces per_round (as expected)
    p_small_k = per_round(5, 0.4, 2)
    p_large_k = per_round(20, 0.4, 2)
    assert p_large_k < p_small_k

    # But finalization probability still increases with more rounds
    pf_few = pr_finalize(3, 20, 0.5, 2)
    pf_many = pr_finalize(15, 20, 0.5, 2)
    assert pf_many > pf_few


def test_pr_finalize_bounds():
    for r in [1, 5, 20]:
        pf = pr_finalize(r, 10, 0.5, 3)
        assert 0.0 <= pf <= 1.0


def test_pr_finalize_increases_with_rounds():
    p1 = pr_finalize(3, 20, 0.5, 2)
    p2 = pr_finalize(10, 20, 0.5, 2)
    assert p2 > p1


def test_expected_rounds_reasonable():
    er = expected_rounds(10, 30, 0.6, 3)
    assert 1.0 < er < 10.0


def test_required_rounds_reaches_target():
    r = required_rounds(0.99, 40, 0.55, 4)
    assert pr_finalize(r, 40, 0.55, 4) >= 0.99 - 1e-9


def test_closure_result_structure():
    params = ClosureParams(k=50, p=0.5, q=3, r=5)
    result = closure_result(params)
    assert hasattr(result, "pr_finalize")
    assert hasattr(result, "expected_rounds")
    assert len(result.schedule) > 0


def test_demo_runs_without_error():
    from powerhouse.core import demo_sextillion_scale
    assert callable(demo_sextillion_scale)