"""
Tests for the config layer of the KL Execution PoC.

Covers:
- loading operations and policies from JSON
- building registry and default policies
- executing operations via the orchestrator using config data
"""

from pathlib import Path

from kl_exec_poc.config import load_config, build_registry_and_policies
from kl_exec_poc import Orchestrator
from kl_exec_poc.adapters import KLBridge


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_load_config_and_build_registry_and_policies():
    project_root = _project_root()
    cfg_path = project_root / "config" / "operations.json"

    configs = load_config(cfg_path)
    assert len(configs) == 3

    registry, policy_map = build_registry_and_policies(configs)

    # Registry keys
    keys = sorted(registry.keys())
    assert keys == ["signals.smooth", "text.llm_stub", "text.simplify"]

    # Policy map matches keys
    assert set(policy_map.keys()) == set(keys)


def test_execute_operations_from_json_config():
    project_root = _project_root()
    cfg_path = project_root / "config" / "operations.json"

    configs = load_config(cfg_path)
    registry, policy_map = build_registry_and_policies(configs)

    bridge = KLBridge()
    orchestrator = Orchestrator(registry=registry, bridge=bridge)

    # Text simplify from config
    text_policy = policy_map["text.simplify"]
    text_result = orchestrator.execute_operation(
        key="text.simplify",
        user_id="test-user",
        request_id="cfg-text-1",
        policy=text_policy,
        text="  Config BASED   Text  ",
    )

    simplified = text_result["execution"]["result"]
    assert simplified == "config based text"

    # LLM stub from config
    llm_policy = policy_map["text.llm_stub"]
    llm_result = orchestrator.execute_operation(
        key="text.llm_stub",
        user_id="test-user",
        request_id="cfg-llm-1",
        policy=llm_policy,
        prompt="MiXeD Case TEXT",
    )

    llm_output = llm_result["execution"]["result"]
    # Default mode is "lower"
    assert llm_output == "mixed case text"

    # Smoothing from config
    smooth_policy = policy_map["signals.smooth"]
    smooth_result = orchestrator.execute_operation(
        key="signals.smooth",
        user_id="test-user",
        request_id="cfg-smooth-1",
        policy=smooth_policy,
        values=[1.0, 2.0, 3.0, 4.0],
    )

    smoothed = smooth_result["execution"]["result"]
    assert smoothed == [1.5, 2.0, 3.0, 3.5]

    # Trace integrity
    trace_text = text_result["execution"]["trace"]
    assert trace_text[0]["stage"] == "start"
    assert trace_text[-1]["stage"] == "end"

    trace_llm = llm_result["execution"]["trace"]
    assert trace_llm[0]["stage"] == "start"
    assert trace_llm[-1]["stage"] == "end"

    trace_smooth = smooth_result["execution"]["trace"]
    assert trace_smooth[0]["stage"] == "start"
    assert trace_smooth[-1]["stage"] == "end"
