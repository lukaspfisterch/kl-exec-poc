"""
Config schemas for the KL Execution PoC.

These are simple data structures that can be populated from
static files (for example JSON or YAML) in later stages.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class PolicyConfig:
    """
    High level policy configuration for an operation class.

    This is a coarse grained view. The technical details are
    still handled by the KL ExecutionPolicy once mapped.
    """

    allow_network: bool = False
    allow_filesystem: bool = False
    timeout_seconds: Optional[int] = None


@dataclass
class OperationConfig:
    """
    Logical description of an operation entry in the registry.
    """

    key: str
    logical_binding: str
    constraints: Optional[str] = None


@dataclass
class RegistryConfig:
    """
    Container for all operation configurations in a registry.
    """

    operations: Dict[str, OperationConfig]
