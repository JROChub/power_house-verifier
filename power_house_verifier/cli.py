import argparse
from .engine import run_verification, get_scenario_params
import json


def main():
    parser = argparse.ArgumentParser(description="power_house-verifier (High-Scale)")
    subparsers = parser.add_subparsers(dest="command")

    v = subparsers.add_parser("verify")
    v.add_argument("--scenario", default="general")
    v.add_argument("--k", type=int)
    v.add_argument("--r", type=int)
    v.add_argument("--high-precision", action="store_true")
    v.add_argument("--output", choices=["text", "json"], default="text")

    c = subparsers.add_parser("compare")
    c.add_argument("--scenario", default="general")

    subparsers.add_parser("scenarios")

    args = parser.parse_args()

    if args.command == "verify":
        params = get_scenario_params(args.scenario)
        if args.k: params.k = args.k
        if args.r: params.r = args.r
        params.high_precision = args.high_precision

        result = run_verification(params)

        if args.output == "json":
            print(json.dumps({
                "probability": result.probability,
                "log_probability": result.log_probability,
                "expected_rounds": result.expected_rounds,
                "schedule": result.schedule,
                "theoretical_bound": result.theoretical_bound
            }, indent=2))
        else:
            print(f"\nScenario: {args.scenario}")
            print(f"Probability: {result.probability*100:.8f}%")
            print(f"Log Probability: {result.log_probability}")
            print(f"Expected Rounds: {result.expected_rounds}")
            print(f"Theoretical Bound: {result.theoretical_bound*100:.8f}%")

    elif args.command == "compare":
        params = get_scenario_params(args.scenario)
        result = run_verification(params)
        print(f"\n{args.scenario.upper()}")
        print(f"Probability: {result.probability*100:.6f}%")
        print(f"Expected Rounds: {result.expected_rounds}")

    elif args.command == "scenarios":
        print("pollution, asthma, ventilator, drug, copd, general")

    else:
        parser.print_help()