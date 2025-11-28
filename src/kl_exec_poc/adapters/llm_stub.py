"""
Very small LLM like stub.

This is not a real language model. It is a controlled component that
simulates an external text generation system so that the PoC can exercise
nondeterministic style operations without depending on a real model.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class LLMStubConfig:
    """
    Configuration for the LLM stub.

    The mode flag gives a simple way to change the behaviour
    without touching the call sites.
    """

    mode: str = "lower"  # possible values: "lower", "upper", "echo"


class LLMStub:
    """
    Simple text transformation stub that mimics a language model interface.

    The goal is to keep the behaviour inspectable and deterministic
    for a given configuration and input.
    """

    def __init__(self, config: LLMStubConfig | None = None) -> None:
        self.config = config or LLMStubConfig()

    def generate(self, prompt: str, **kwargs: Any) -> Dict[str, str]:
        """
        Apply a trivial transformation based on the configured mode.
        """
        if self.config.mode == "upper":
            text = prompt.upper()
        elif self.config.mode == "echo":
            text = prompt
        else:
            text = prompt.lower()

        return {
            "prompt": prompt,
            "output": text,
        }
