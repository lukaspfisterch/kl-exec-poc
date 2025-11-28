"""
Config schemas for the KL Execution PoC.

These are simple data structures that can be populated from
static files (for example JSON) and then mapped to KL primitives.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class OperationPolicyConfig:
    """
    High level policy configuration for a single operation.

    This is a coarse grained view. The technical details are
    still handled by the KL ExecutionPolicy once mapped.
    """

    allow_network: bool = False
    allow_filesystem: bool = False
    timeout_seconds: Optional[int] = None


@dataclass
class OperationConfig:
    """
    Logical description of an operation entry in the registry,
    including a simple policy configuration.
    """

    key: str
    kind: str
    logical_binding: str
    constraints: Optional[str]
    policy: OperationPolicyConfig
