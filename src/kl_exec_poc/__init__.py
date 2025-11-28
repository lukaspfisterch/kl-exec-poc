"""
KL Execution PoC.

This package provides:
- a small operation registry
- a minimal orchestrator that executes operations through the KL Kernel Logic foundations
- adapters that bridge into the KL Kernel (Psi, CAEL, Kernel)

The focus is on structure, policy and traceability.
"""

from .registry import OperationRegistry, OperationMetadata
from .orchestrator import Orchestrator

__all__ = [
    "OperationRegistry",
    "OperationMetadata",
    "Orchestrator",
]
