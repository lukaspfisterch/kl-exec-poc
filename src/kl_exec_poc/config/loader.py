"""
Config loader for the KL Execution PoC.

Loads operations and their policies from JSON and builds:
- OperationConfig objects
- a registry and policy map for the orchestrator
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from kl_kernel_logic import (
    PsiDefinition,
    OperationType,
    EffectClass,
    ExecutionPolicy,
)
from kl_kernel_logic.examples.text_simplify import simplify_text
from kl_kernel_logic.examples_foundations import smooth_measurements

from ..registry import OperationRegistry, OperationMetadata
from .schemas import OperationConfig, OperationPolicyConfig
from ..adapters.llm_stub import llm_stub_generate


# Mapping from config "kind" to concrete task callables.
OPERATION_KIND_MAP: Dict[str, Any] = {
    "text_simplify": simplify_text,
    "signals_smooth": smooth_measurements,
    "llm_stub": llm_stub_generate,
}


def load_config(path: str | Path) -> List[OperationConfig]:
    """
    Load operation configuration from a JSON file.

    The JSON is expected to have the structure:

    {
      "operations": [
        {
          "key": "...",
          "kind": "...",
          "logical_binding": "...",
          "constraints": "...",
          "policy": {
            "allow_network": false,
            "allow_filesystem": false,
            "timeout_seconds": 5
          }
        }
      ]
    }
    """
    cfg_path = Path(path)
    raw_text = cfg_path.read_text(encoding="utf-8")
    data = json.loads(raw_text)

    configs: List[OperationConfig] = []
    for raw in data.get("operations", []):
        policy_raw: Dict[str, Any] = raw.get("policy", {})
        policy = OperationPolicyConfig(
            allow_network=bool(policy_raw.get("allow_network", False)),
            allow_filesystem=bool(policy_raw.get("allow_filesystem", False)),
            timeout_seconds=policy_raw.get("timeout_seconds"),
        )

        cfg = OperationConfig(
            key=str(raw["key"]),
            kind=str(raw["kind"]),
            logical_binding=str(raw["logical_binding"]),
            constraints=raw.get("constraints"),
            policy=policy,
        )
        configs.append(cfg)

    return configs


def build_registry_and_policies(
    configs: List[OperationConfig],
) -> Tuple[OperationRegistry, Dict[str, ExecutionPolicy]]:
    """
    Build an OperationRegistry and a map of default ExecutionPolicy objects
    from a list of OperationConfig entries.

    The registry maps operation keys to PsiDefinition and task callables.
    The policy map provides a default ExecutionPolicy per operation key.
    """
    registry = OperationRegistry()
    policies: Dict[str, ExecutionPolicy] = {}

    for cfg in configs:
        try:
            task = OPERATION_KIND_MAP[cfg.kind]
        except KeyError as exc:
            raise KeyError(f"Unknown operation kind in config: {cfg.kind}") from exc

        psi = PsiDefinition(
            operation_type=OperationType.TRANSFORM,
            logical_binding=cfg.logical_binding,
            effect_class=EffectClass.NON_STATE_CHANGING,
            constraints=cfg.constraints,
        )

        meta = OperationMetadata(psi=psi, task=task)
        registry.register(cfg.key, meta)

        policies[cfg.key] = ExecutionPolicy(
            allow_network=cfg.policy.allow_network,
            allow_filesystem=cfg.policy.allow_filesystem,
            timeout_seconds=cfg.policy.timeout_seconds,
        )

    return registry, policies
