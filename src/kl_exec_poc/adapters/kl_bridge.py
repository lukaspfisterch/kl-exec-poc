"""
Bridge into the KL Kernel Logic foundations.

This keeps the PoC orchestrator independent from the concrete
foundations layout and provides thin helper methods to build
policies, contexts and Psi definitions.
"""

from typing import Any, Callable, Dict

from kl_kernel_logic import (
    Kernel,
    PsiDefinition,
    ExecutionContext,
    ExecutionPolicy,
    OperationType,
    EffectClass,
)


class KLBridge:
    """
    Thin helper around the KL Kernel.

    The bridge is responsible for:
    - creating ExecutionPolicy and ExecutionContext objects
    - building simple PsiDefinition templates
    - forwarding execution calls into the Kernel
    """

    def __init__(self) -> None:
        self.kernel = Kernel()

    def execute(
        self,
        psi: PsiDefinition,
        ctx: ExecutionContext,
        task: Callable[..., Any],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Execute a task through the KL Kernel and return the bundle.
        """
        return self.kernel.execute(psi=psi, ctx=ctx, task=task, **kwargs)

    @staticmethod
    def build_policy(
        allow_network: bool = False,
        allow_filesystem: bool = False,
        timeout_seconds: int | None = None,
    ) -> ExecutionPolicy:
        """
        Build a simple ExecutionPolicy with the most relevant flags.
        """
        return ExecutionPolicy(
            allow_network=allow_network,
            allow_filesystem=allow_filesystem,
            timeout_seconds=timeout_seconds,
        )

    @staticmethod
    def build_ctx(
        user_id: str,
        request_id: str,
        policy: ExecutionPolicy,
    ) -> ExecutionContext:
        """
        Build an ExecutionContext for a single execution path.
        """
        return ExecutionContext(
            user_id=user_id,
            request_id=request_id,
            policy=policy,
        )

    @staticmethod
    def build_transform_psi(
        logical_binding: str,
        constraints: str | None = None,
    ) -> PsiDefinition:
        """
        Build a simple PsiDefinition for a transform operation.

        This uses NON_STATE_CHANGING as a default effect class, which
        matches most read only or pure transformation operations.
        """
        return PsiDefinition(
            operation_type=OperationType.TRANSFORM,
            logical_binding=logical_binding,
            effect_class=EffectClass.NON_STATE_CHANGING,
            constraints=constraints,
        )
