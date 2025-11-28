# KL Execution PoC 0.1.0

This repository implements a minimal execution layer built on top of the **[KL Kernel Logic](https://github.com/lukaspfisterch/kl-kernel-logic)** foundations.  
The goal is to provide a small, inspectable execution fabric that can:

- register operations (Psi + callable task)
- apply policy through CAEL
- execute operations through the KL Kernel
- load configuration from static JSON
- expose a clean command line interface
- integrate deterministic and pseudo nondeterministic operations (LLM stub)

The PoC does **not** extend or modify the KL Kernel Logic.  
It consumes it.

---

## 1. Components

### 1.1 Operation Registry
Located in `src/kl_exec_poc/registry.py`.

Maps operation keys to:
- `PsiDefinition` (from KL foundations)
- callable task (Python function)

The registry is intentionally small and in-memory.

---

### 1.2 Orchestrator
Located in `src/kl_exec_poc/orchestrator.py`.

Responsibilities:
- look up operation metadata from the registry
- build `ExecutionContext` via the KL bridge
- call the KL Kernel to execute the task under policy

The orchestrator does not implement any domain logic.  
It is a connector between **registry → KL Kernel**.

---

### 1.3 KL Bridge
Located in `src/kl_exec_poc/adapters/kl_bridge.py`.

Abstraction around the KL Kernel Logic.  
Creates:

- `ExecutionPolicy`
- `ExecutionContext`
- simple `PsiDefinition` templates  
- forwards execution into `Kernel.execute`

The bridge isolates the PoC from the foundations layout.

---

### 1.4 Configuration Layer
Located in `src/kl_exec_poc/config`.

Two parts:

- `load_config(path)`  
  Parses JSON files into `OperationConfig` + policy data.

- `build_registry_and_policies(configs)`  
  Produces:
  - `OperationRegistry`
  - `{operation_key: ExecutionPolicy}` map

The default config file is:

config/operations.json

Example entries:
- `text.simplify`
- `text.llm_stub`
- `signals.smooth`

---

### 1.5 CLI Layer
Located in:

- `src/kl_exec_poc/cli.py`
- `src/kl_exec_poc/__main__.py`

Supports:

```bash
python -m kl_exec_poc run --op text.simplify --input "Text..."
python -m kl_exec_poc run --op signals.smooth --values 1 2 3 4
python -m kl_exec_poc run --op text.llm_stub --input "Some text"
```

The CLI:
- loads config  
- builds registry and policies  
- executes the selected operation  
- prints the full KL bundle as formatted JSON (psi + execution + trace)

---

### 1.6 Examples
Located in `src/kl_exec_poc/examples/simple_chain.py`.

Two demonstration flows:
- text simplification
- numeric smoothing

Both run through the full KL path:
registry → KL bridge → Kernel → CAEL → result bundle.

---

### 1.7 LLM Stub
Located in `src/kl_exec_poc/adapters/llm_stub.py`.

A deterministic text transform used to model LLM-style operations without introducing external dependencies.

Modes:
- `"lower"` (default)
- `"upper"`
- `"echo"`

Mapped via config using:

```json
"kind": "llm_stub"
```


---

## 2. Project Structure

kl-exec-poc/
│
├── config/
│ └── operations.json
│
├── src/kl_exec_poc/
│ ├── adapters/ # KL bridge + LLM stub
│ ├── config/ # schemas + loader
│ ├── examples/ # simple demonstration chains
│ ├── registry.py # operation registry
│ ├── orchestrator.py # execution fabric
│ ├── cli.py # command line interface
│ └── main.py # enables python -m kl_exec_poc
│
└── tests/
├── test_registry.py
├── test_orchestrator_flow.py
├── test_config_loader.py
├── test_cli.py
└── test_llm_stub_integration.py

---

## 3. Quickstart

### 3.1 Requirements

- Python 3.10+
- `pip` and `venv`

### 3.2 Install

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

### 3.3 Run Example

```bash
python -m kl_exec_poc run --op text.simplify --input "  Hello   WORLD  "
```

Expected output (formatted JSON):

```json
{
  "psi": {
    "operation_type": "transform",
    "logical_binding": "text.simplify",
    "effect_class": "non-state-changing",
    "constraints": null
  },
  "execution": {
    "result": "Hello WORLD",
    "trace": [
      {"stage": "start", "user_id": "cli-user", "request_id": "..."},
      {"stage": "end", "user_id": "cli-user", "request_id": "..."}
    ]
  }
}
```

### 3.4 Run Tests

```bash
pytest
```

Should show all tests passing.

4. Architectural Intent
This PoC is intentionally constrained:

The KL Kernel Logic remains the source of truth.

The execution layer adds orchestration, not computation.

All operations (text, smoothing, LLM stub) flow through the same KL pipeline.

Everything is inspectable and deterministic:

Psi

ExecutionContext

ExecutionPolicy

full trace from CAEL

The result is a minimal but expressive execution fabric that demonstrates how arbitrary operations can be handled under a uniform, policy-verified KL runtime.

5. Status
Version: 0.1.0
Scope: Demonstration and exploration.
Next steps (optional):

enrich policy configuration (capabilities, effect classes)

add tracing backends

support composed multi-stage workflows

extend CLI to allow chained operations