"""
End-to-end tests for the KL Execution PoC orchestrator.

Covers:
- text simplification via KL foundations
- numeric smoothing via foundational operations
"""

from kl_kernel_logic import (
    ExecutionPolicy,
    PsiDefinition,
    OperationType,
    EffectClass,
)
from kl_kernel_logic.examples.text_simplify import simplify_text, build_psi
from kl_kernel_logic.examples_foundations import smooth_measurements

from kl_exec_poc import OperationRegistry, OperationMetadata, Orchestrator
from kl_exec_poc.adapters import KLBridge


def test_orchestrator_executes_text_simplify_operation():
    registry = OperationRegistry()

    psi = build_psi()
    meta = OperationMetadata(psi=psi, task=simplify_text)
    registry.register("text.simplify", meta)

    bridge = KLBridge()
    orchestrator = Orchestrator(registry=registry, bridge=bridge)

    policy = ExecutionPolicy(
        allow_network=False,
        allow_filesystem=False,
        timeout_seconds=5,
    )

    input_text = "  This Is   A DEMO Text   "
    result = orchestrator.execute_operation(
        key="text.simplify",
        user_id="test-user",
        request_id="req-123",
        policy=policy,
        text=input_text,
    )

    # Kernel bundle structure
    assert "psi" in result
    assert "execution" in result
    assert result["psi"]["logical_binding"] == psi.logical_binding

    simplified = result["execution"]["result"]
    assert simplified == "this is a demo text"

    trace = result["execution"]["trace"]
    assert trace[0]["stage"] == "start"
    assert trace[-1]["stage"] == "end"


def test_orchestrator_executes_smoothing_operation():
    registry = OperationRegistry()

    psi = PsiDefinition(
        operation_type=OperationType.TRANSFORM,
        logical_binding="foundations.signals.smoothing",
        effect_class=EffectClass.NON_STATE_CHANGING,
        constraints=(
            "Input: 1D scalar series, length <= 10_000. "
            "Output: 1D scalar series of the same length. "
            "Deterministic three point moving average."
        ),
    )
    meta = OperationMetadata(psi=psi, task=smooth_measurements)
    registry.register("signals.smooth", meta)

    bridge = KLBridge()
    orchestrator = Orchestrator(registry=registry, bridge=bridge)

    policy = ExecutionPolicy(
        allow_network=False,
        allow_filesystem=False,
        timeout_seconds=5,
    )

    result = orchestrator.execute_operation(
        key="signals.smooth",
        user_id="test-user",
        request_id="req-smooth-1",
        policy=policy,
        values=[1.0, 2.0, 3.0, 4.0],
    )

    smoothed = result["execution"]["result"]
    assert smoothed == [1.5, 2.0, 3.0, 3.5]

    trace = result["execution"]["trace"]
    assert trace[0]["stage"] == "start"
    assert trace[-1]["stage"] == "end"
