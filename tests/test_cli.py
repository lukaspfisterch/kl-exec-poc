"""
Tests for the CLI layer of the KL Execution PoC.

Covers:
- running a text operation via the CLI main entry point
- running a numeric smoothing operation via the CLI main entry point
"""

from pathlib import Path
import json

from kl_exec_poc.cli import main


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_cli_text_simplify(capsys):
    """
    CLI should execute text.simplify and print a KL bundle with simplified text.
    """
    root = _project_root()
    cfg_path = root / "config" / "operations.json"

    rc = main(
        [
            "run",
            "--op",
            "text.simplify",
            "--input",
            "  CLI   Text  ",
            "--config",
            str(cfg_path),
        ]
    )

    assert rc == 0

    captured = capsys.readouterr()
    out = captured.out

    bundle = json.loads(out)

    # Basic structure
    assert "psi" in bundle
    assert "execution" in bundle

    result = bundle["execution"]["result"]
    assert result == "cli text"

    trace = bundle["execution"]["trace"]
    assert trace[0]["stage"] == "start"
    assert trace[-1]["stage"] == "end"


def test_cli_signals_smooth(capsys):
    """
    CLI should execute signals.smooth and print a KL bundle with smoothed values.
    """
    root = _project_root()
    cfg_path = root / "config" / "operations.json"

    rc = main(
        [
            "run",
            "--op",
            "signals.smooth",
            "--values",
            "1",
            "2",
            "3",
            "4",
            "--config",
            str(cfg_path),
        ]
    )

    assert rc == 0

    captured = capsys.readouterr()
    out = captured.out

    bundle = json.loads(out)

    # Basic structure
    assert "psi" in bundle
    assert "execution" in bundle

    result = bundle["execution"]["result"]
    assert result == [1.5, 2.0, 3.0, 3.5]

    trace = bundle["execution"]["trace"]
    assert trace[0]["stage"] == "start"
    assert trace[-1]["stage"] == "end"
