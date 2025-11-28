"""
Simple example chains that use the registry and the orchestrator.

This module demonstrates:
- a basic text simplification operation (from the KL Kernel Logic foundations)
- an extended registry that also includes a numeric smoothing operation
"""

from typing import Dict, Any, List

import kl_kernel_logic
from kl_kernel_logic import PsiDefinition, ExecutionPolicy
from kl_kernel_logic.examples.text_simplify import simplify_text, build_psi
from kl_kernel_logic.examples_foundations import smooth_measurements

from ..adapters.kl_bridge import KLBridge
from ..registry import OperationRegistry, OperationMetadata
from ..orchestrator import Orchestrator


# ---------------------------------------------------------------------------
# 1) Single-operation example (text simplify)
# ---------------------------------------------------------------------------

def build_example_registry() -> OperationRegistry:
    """
    Register a single text simplification operation.
    """
    registry = OperationRegistry()

    psi: PsiDefinition = build_psi()
    metadata = OperationMetadata(
        psi=psi,
        task=simplify_text,
    )

    registry.register("text.simplify", metadata)
    return registry


def run_simple_chain(input_text: str) -> Dict[str, Any]:
    """
    Run a single operation through the orchestrator to demonstrate the flow.
    """
    registry = build_example_registry()
    bridge = KLBridge()
    orchestrator = Orchestrator(registry=registry, bridge=bridge)

    policy = ExecutionPolicy(
        allow_network=False,
        allow_filesystem=False,
        timeout_seconds=5,
    )

    result = orchestrator.execute_operation(
        key="text.simplify",
        user_id="demo-user",
        request_id="demo-request-001",
        policy=policy,
        text=input_text,
    )

    return result


# ---------------------------------------------------------------------------
# 2) Extended example (text simplify + numeric smoothing)
# ---------------------------------------------------------------------------

def build_extended_registry() -> OperationRegistry:
    """
    Register:
    - text simplification
    - numeric smoothing from KL foundational operations
    """
    registry = OperationRegistry()

    # Text simplify
    psi_text: PsiDefinition = build_psi()
    text_meta = OperationMetadata(
        psi=psi_text,
        task=simplify_text,
    )
    registry.register("text.simplify", text_meta)

    # Numeric smoothing
    psi_smooth = PsiDefinition(
        operation_type=kl_kernel_logic.OperationType.TRANSFORM,
        logical_binding="foundations.signals.smoothing",
        effect_class=kl_kernel_logic.EffectClass.NON_STATE_CHANGING,
        constraints=(
            "Input: 1D scalar series, length <= 10_000. "
            "Output: 1D scalar series of the same length. "
            "Deterministic three point moving average."
        ),
    )

    smooth_meta = OperationMetadata(
        psi=psi_smooth,
        task=smooth_measurements,
    )
    registry.register("signals.smooth", smooth_meta)

    return registry


def run_smoothing_chain(values: List[float]) -> Dict[str, Any]:
    """
    Run the smoothing operation through the orchestrator.
    """
    registry = build_extended_registry()
    bridge = KLBridge()
    orchestrator = Orchestrator(registry=registry, bridge=bridge)

    policy = ExecutionPolicy(
        allow_network=False,
        allow_filesystem=False,
        timeout_seconds=5,
    )

    result = orchestrator.execute_operation(
        key="signals.smooth",
        user_id="demo-user",
        request_id="smooth-demo-001",
        policy=policy,
        values=values,
    )

    return result
