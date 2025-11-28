"""
Tests for the OperationRegistry used in the KL Execution PoC.
"""

import pytest

from kl_exec_poc import OperationRegistry, OperationMetadata
from kl_kernel_logic import PsiDefinition, OperationType, EffectClass


def _dummy_psi() -> PsiDefinition:
    return PsiDefinition(
        operation_type=OperationType.TRANSFORM,
        logical_binding="test.domain",
        effect_class=EffectClass.NON_STATE_CHANGING,
        constraints=None,
    )


def _dummy_task(value: str) -> str:
    return value


def test_register_and_get_operation():
    registry = OperationRegistry()
    meta = OperationMetadata(psi=_dummy_psi(), task=_dummy_task)

    registry.register("test.op", meta)

    loaded = registry.get("test.op")
    assert loaded.psi.logical_binding == "test.domain"
    assert loaded.task("x") == "x"
    assert "test.op" in registry.keys()


def test_register_duplicate_key_raises():
    registry = OperationRegistry()
    meta = OperationMetadata(psi=_dummy_psi(), task=_dummy_task)

    registry.register("test.op", meta)
    with pytest.raises(ValueError):
        registry.register("test.op", meta)


def test_unknown_key_raises():
    registry = OperationRegistry()
    with pytest.raises(KeyError):
        registry.get("missing.op")
