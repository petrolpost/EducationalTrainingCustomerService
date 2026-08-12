# Implementation Plan: Educational Training Customer Service Core

**Branch**: `001-edu-cs-core` | **Date**: 2026-08-12 | **Spec**: [spec.md](file:///e:/workspaces/self/EducationalTrainingCustomerService/specs/001-edu-cs-core/spec.md)

**Input**: Feature specification from `/specs/001-edu-cs-core/spec.md`

**Note**: This plan is generated from the approved design document and the feature specification derived from it.

## Summary

Build the first implementation slice of the Educational Training Customer Service system as a CLI/API-first replay core with a lightweight web control console. The plan centers on stable replay contracts, signal-production/consumption decoupling, provenance-rich record keeping, baseline configuration governance, and least-visibility multi-tenant query behavior.

## Technical Context

**Language/Version**: Python 3.12 for core service/CLI/API; TypeScript 5.x for lightweight web console

**Primary Dependencies**: FastAPI, Typer, Pydantic v2, SQLAlchemy, SQLite, React, Vite

**Storage**: SQLite for replay sessions, normalized outputs, provenance, feedback, and configuration metadata

**Testing**: pytest, pytest-asyncio, httpx, contract/replay regression tests, Playwright smoke tests for console

**Target Platform**: Local development on Windows/Linux and single-node service deployment for validation environments

**Project Type**: Backend service + CLI + lightweight web console

**Performance Goals**: Process a typical replay session of up to 500 events within 5 seconds on a developer machine; load replay review views and scoped aggregates under 500 ms p95 in validation environments

**Constraints**: Offline replay first; runtime remains open loop for signal governance; baseline configuration is code-owned; protocol must evolve via versioned core + extensions; least-visibility query behavior is mandatory

**Scale/Scope**: Initial validation scope targets dozens of tenants or school groups, thousands of replay sessions, and hundreds of events per session rather than production-scale real-time traffic

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The project constitution file at `.specify/memory/constitution.md` is still a template and does not yet contain enforceable project-specific rules. For this feature, the approved design document and feature spec define the working gates:

1. **CLI/API-first gate**: The core service must stay decoupled from any production client UI.
2. **Config-first gate**: Baseline behavior must be configuration-driven and version-controlled.
3. **Spec + TDD gate**: Contracts, replay behavior, and recording flows must be testable before implementation proceeds.
4. **Open-loop runtime gate**: Signal lifecycle changes cannot occur automatically in runtime execution.
5. **Least-visibility gate**: Query, aggregation, and review surfaces must enforce scoped visibility.

**Gate Status (pre-design)**: PASS  
**Gate Status (post-design)**: PASS

## Project Structure

### Documentation (this feature)

```text
specs/001-edu-cs-core/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── cli.md
│   ├── http-api.md
│   └── replay-protocol.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   └── edu_cs_core/
│       ├── api/
│       ├── cli/
│       ├── config/
│       ├── domain/
│       ├── governance/
│       ├── protocol/
│       ├── replay/
│       ├── storage/
│       └── services/
└── tests/
    ├── contract/
    ├── integration/
    ├── regression/
    └── unit/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── state/
└── tests/
    └── smoke/
```

**Structure Decision**: Use a split backend/frontend layout. Keep the core logic, protocol, governance, and persistence in the Python backend. Keep the validation-oriented console in a lightweight frontend that can later be replaced or embedded into a different control-plane shell.

## Complexity Tracking

No constitution violations are currently justified. The design intentionally avoids premature real-time integration, online configuration management, and production-grade UI scope.
