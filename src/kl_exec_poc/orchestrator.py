"""
Minimal orchestrator for the KL Execution PoC.

The orchestrator connects:
- the OperationRegistry (what can be executed)
- the KLBridge (how it is executed through the Kernel)
"""

from typing import Any, Dict

from kl_kernel_logic import ExecutionPolicy

from .adapters.kl_bridge import KLBridge
from .registry import OperationRegistry, OperationMetadata


class Orchestrator:
    """
    Minimal orchestrator that looks up an operation in the registry,
    builds a KL context and executes through the KL bridge.
    """

    def __init__(self, registry: OperationRegistry, bridge: KLBridge | None = None) -> None:
        self.registry = registry
        self.bridge = bridge or KLBridge()

    def execute_operation(
        self,
        key: str,
        user_id: str,
        request_id: str,
        policy: ExecutionPolicy,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Execute a registered operation using the KL Kernel through the bridge.
        """
        meta: OperationMetadata = self.registry.get(key)
        ctx = self.bridge.build_ctx(user_id=user_id, request_id=request_id, policy=policy)
        return self.bridge.execute(psi=meta.psi, ctx=ctx, task=meta.task, **kwargs)
