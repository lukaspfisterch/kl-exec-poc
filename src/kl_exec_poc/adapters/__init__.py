"""
Adapters that connect the PoC orchestrator to external systems.

Currently this includes:
- a bridge into the KL Kernel Logic foundations
- a simple LLM stub for controlled experiments
"""

from .kl_bridge import KLBridge
from .llm_stub import LLMStub

__all__ = [
    "KLBridge",
    "LLMStub",
]
