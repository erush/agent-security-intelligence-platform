# Attack Registry Specification

## Purpose

The Attack Registry is the central catalog of all attack capabilities available to the Agent Security Intelligence Platform (ASIP).

Rather than embedding attack logic inside search algorithms or planners, every attack capability is represented as a reusable, self-describing strategy registered with the platform.

The registry allows planners and search algorithms to reason about attack capabilities instead of implementation details.

---

# Philosophy

Search explores.

Strategies generate.

The registry describes.

The registry is not responsible for executing attacks.

It provides a declarative inventory of attack capabilities.

---

# Objectives

The registry exists to:

- organize attack capabilities
- standardize attack metadata
- support planner decisions
- enable modular experimentation
- simplify extension
- measure strategy performance
- decouple planning from implementation

---

# Registry Model

Every attack strategy registers itself with the platform.

The registry maintains structured metadata describing each strategy.

The registry should never contain benchmark-specific logic.

---

# Registry Entry

Every strategy should expose:

Strategy ID

Strategy Name

Version

Description

Category

Target Predicates

Supported Environments

Supported Models

Required Tools

Optional Tools

Estimated Cost

Expected Replay Stability

Expected Novelty

Priority

Author

Implementation Class

---

# Categories

Strategies may belong to one or more categories.

Examples include:

Prompt Injection

Indirect Prompt Injection

Memory Poisoning

Goal Drift

Planning Manipulation

Tool Manipulation

Tool Confusion

Authority Escalation

Confused Deputy

Context Manipulation

Delayed Trigger

Instruction Override

Data Exfiltration

File Manipulation

Email Manipulation

Search Manipulation

State Poisoning

Hybrid

Experimental

---

# Predicate Mapping

Strategies should declare intended predicates.

Examples:

EXFILTRATION

UNTRUSTED_TO_ACTION

CONFUSED_DEPUTY

DESTRUCTIVE_WRITE

Multiple predicates may be supported.

---

# Environment Compatibility

Strategies declare compatible environments.

Examples:

Kaggle JED

OpenAI Agents

Anthropic Tool Use

MCP

LangGraph

CrewAI

AutoGen

Enterprise Agents

---

# Planner Integration

The Planner queries the registry rather than individual implementations.

Example planning questions:

Which strategies target EXFILTRATION?

Which strategies have high replay success?

Which strategies have not been executed?

Which strategies require shell access?

Which strategies support this environment?

Which strategies maximize diversity?

---

# Search Integration

Search algorithms receive strategies selected by the Planner.

Search remains independent of attack implementation.

Changing search algorithms should not require modifying registry entries.

---

# Strategy Lifecycle

Strategy Registered

↓

Planner Selection

↓

Search Execution

↓

Trajectory Generated

↓

Candidate Produced

↓

Replay Validation

↓

Analytics Updated

↓

Registry Statistics Updated

---

# Registry Statistics

The registry should maintain historical metrics.

Examples:

Execution Count

Replay Success Rate

Average Severity

Average Runtime

Average Candidate Yield

Average Replay Stability

Coverage Contribution

Transferability

Novelty Score

Failure Rate

---

# Warehouse Integration

Registry metadata should map into warehouse dimensions.

Examples:

dim_strategy

fact_strategy_execution

fact_strategy_performance

fact_strategy_replay

fact_strategy_transfer

analytics_strategy_summary

---

# Analytics

The registry enables questions including:

Most successful strategies

Highest replay stability

Highest predicate diversity

Highest transferability

Highest novelty

Lowest execution cost

Best candidate yield

Best replay efficiency

Most compatible environments

---

# Extensibility

Adding a new strategy should require:

1. Strategy implementation

2. Strategy specification

3. Registration

No Planner modifications should be required.

No Search modifications should be required.

---

# Design Principles

Strategies are modular.

Strategies are declarative.

Strategies are benchmark independent.

Strategies expose metadata.

Strategies are observable.

Strategies are measurable.

Strategies are versioned.

Strategies are independently testable.

---

# Long-Term Vision

The Attack Registry should evolve into a comprehensive taxonomy of autonomous agent attack techniques.

Future versions may include:

automatic capability discovery

strategy recommendation

adaptive prioritization

strategy composition

strategy mutation

strategy inheritance

cross-environment compatibility scoring

automatic benchmark mapping

The registry should become the canonical description of ASIP's offensive capabilities while remaining completely independent from the Planner, Search Engine, and Environment Adapters.