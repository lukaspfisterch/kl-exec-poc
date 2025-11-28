"""
Command line interface for the KL Execution PoC.

Usage examples (from the project root):

    python -m kl_exec_poc run --op text.simplify --input "  Hello   WORLD  "
    python -m kl_exec_poc run --op signals.smooth --values 1 2 3 4

The CLI:
- loads operation and policy config from JSON
- builds a registry and policy map
- executes the selected operation through the orchestrator
- prints the KL bundle as JSON to stdout
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence

from .config import load_config, build_registry_and_policies
from .adapters import KLBridge
from .orchestrator import Orchestrator


def _default_config_path() -> Path:
    """
    Resolve the default config path relative to the project root.

    Layout assumption:
    src/kl_exec_poc/cli.py
    config/operations.json  (one level above src)
    """
    return Path(__file__).resolve().parents[3] / "config" / "operations.json"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kl-exec-poc",
        description="KL Execution PoC command line interface.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(
        "run",
        help="Run a configured operation.",
    )
    run_parser.add_argument(
        "--op",
        required=True,
        help="Operation key, for example 'text.simplify' or 'signals.smooth'.",
    )
    run_parser.add_argument(
        "--input",
        help="Text input for text operations (for example 'text.simplify').",
    )
    run_parser.add_argument(
        "--values",
        nargs="+",
        type=float,
        help="Numeric values for smoothing operations (for example 'signals.smooth').",
    )
    run_parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Optional path to a JSON config file. Defaults to config/operations.json.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """
    CLI entry point.

    Returns:
        Process exit code (0 on success, non-zero on failure).
    """
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command == "run":
        return _handle_run(args, parser)

    parser.error(f"Unknown command: {args.command}")
    return 1


def _handle_run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    # Resolve config path
    cfg_path = Path(args.config) if args.config is not None else _default_config_path()

    if not cfg_path.exists():
        parser.error(f"Config file not found: {cfg_path}")

    # Load config and build registry + policies
    configs = load_config(cfg_path)
    registry, policy_map = build_registry_and_policies(configs)

    if args.op not in policy_map:
        parser.error(f"Unknown operation key: {args.op}")

    policy = policy_map[args.op]

    bridge = KLBridge()
    orchestrator = Orchestrator(registry=registry, bridge=bridge)

    # Dispatch based on operation key
    if args.op == "text.simplify":
        if not args.input:
            parser.error("text.simplify requires --input <text>.")
        result = orchestrator.execute_operation(
            key=args.op,
            user_id="cli-user",
            request_id="cli-text-001",
            policy=policy,
            text=args.input,
        )
    elif args.op == "signals.smooth":
        if not args.values:
            parser.error("signals.smooth requires --values <v1> <v2> ...")
        result = orchestrator.execute_operation(
            key=args.op,
            user_id="cli-user",
            request_id="cli-smooth-001",
            policy=policy,
            values=list(args.values),
        )
    else:
        parser.error(f"Operation not supported by CLI dispatch: {args.op}")
        return 1

    # Print KL bundle as JSON
    _print_json(result)
    return 0


def _print_json(bundle: Dict[str, Any]) -> None:
    """
    Print the KL bundle as formatted JSON.
    """
    text = json.dumps(bundle, indent=2)
    print(text)
