# KL Execution PoC 0.1.0

## Overview
This repository builds on the **KL Kernel Logic foundations** and explores how KL can be used as a small execution fabric.

## Capabilities
- an operation registry
- an orchestrator that calls into the KL Kernel
- deterministic and later non deterministic example operations
- config-driven policies (network, filesystem, timeouts) via `config/operations.json`
- CLI entry point: `python -m kl_exec_poc run --op <key> ...`

## Scope
- Keep the code inspectable and compact.
- Focus on structure, policy and traceability.
- Avoid premature infrastructure concerns.

## Layout
- `config/operations.json` — operation definitions and default policies
- `src/kl_exec_poc/` — registry, orchestrator, adapters (KL bridge, LLM stub), CLI, examples
- `tests/` — coverage of registry, orchestrator flow, config loader, and CLI paths

## Foundations
The KL foundations themselves live in a separate repository that defines Psi, CAEL and the Kernel with deterministic examples.
