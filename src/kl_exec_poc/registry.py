"""
Operation registry for the KL Execution PoC.

The registry maps operation keys to Psi definitions and callable tasks.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict

from kl_kernel_logic import PsiDefinition


@dataclass
class OperationMetadata:
    """
    Holds the Psi definition and the callable task for a single operation.
    """

    psi: PsiDefinition
    task: Callable[..., Any]


class OperationRegistry:
    """
    Simple in memory registry that maps keys to operation metadata.
    """

    def __init__(self) -> None:
        self._operations: Dict[str, OperationMetadata] = {}

    def register(self, key: str, meta: OperationMetadata) -> None:
        """
        Register a new operation under a unique key.
        """
        if key in self._operations:
            raise ValueError(f"Operation key already registered: {key}")
        self._operations[key] = meta

    def get(self, key: str) -> OperationMetadata:
        """
        Retrieve the metadata for a registered operation.
        """
        try:
            return self._operations[key]
        except KeyError as exc:
            raise KeyError(f"Unknown operation key: {key}") from exc

    def keys(self) -> list[str]:
        """
        Return a list of all registered operation keys.
        """
        return list(self._operations.keys())
