# Environment Adapter Specification

## Purpose

The Environment Adapter provides a stable interface between ASIP and external agent execution environments.

ASIP should not depend directly on any benchmark, SDK, API, or agent framework.

Adapters isolate environment-specific behavior while exposing a common execution contract to the Planner, Search Engine, Replay Engine, Warehouse, and Reporting layers.

---

# Philosophy

Benchmarks change.

SDKs change.

Agent frameworks change.

The ASIP core should not.

The adapter protects the platform from environment-specific complexity.

---

# Responsibilities

The Environment Adapter is responsible for:

- initializing environments
- resetting environments
- sending prompts
- collecting responses
- collecting tool events
- exporting traces
- saving snapshots
- restoring snapshots
- enforcing environment limits
- normalizing environment outputs
- converting native traces into ASIP trajectories
- converting ASIP candidates into environment-native replay objects

---

# Inputs

The adapter receives:

- environment instance
- adapter configuration
- prompt chains
- execution limits
- search context
- replay context

---

# Outputs

The adapter produces:

- normalized observations
- normalized tool events
- normalized trajectories
- normalized execution results
- candidate-compatible prompt chains
- environment metadata

---

# Core Interface

Every adapter should support:

```python
reset()

interact(prompt: str)

snapshot()

restore(handle)

export_trace()

get_metadata()

get_limits()

normalize_trace(raw_trace)

build_candidate(prompt_chain)
```

---

# Kaggle JED Adapter

Initial supported environment:

Kaggle JED Attack Benchmark

Native environment API:

```python
env.reset()
env.interact(prompt)
env.export_trace_dict()
env.snapshot()
env.restore(handle)
```

Supported tools:

- fs.read
- fs.write
- fs.delete
- http.post
- email.send
- web.search
- shell.run

Supported predicates:

- EXFILTRATION
- UNTRUSTED_TO_ACTION
- DESTRUCTIVE_WRITE
- CONFUSED_DEPUTY

Known limits:

- 9,000 seconds per model for attack generation
- 2,000 maximum candidates
- 32 maximum messages per candidate
- 10,000 characters per message
- 8 maximum tool hops per interaction

---

# Normalization

Adapters must normalize all native environment outputs into ASIP structures.

Tool event normalization should include:

- tool name
- arguments
- result
- success status
- error
- timestamp
- side effect category
- raw payload

Message normalization should include:

- role
- content
- position
- length
- timestamp

Trace normalization should preserve raw data while producing structured platform data.

---

# Limits

The adapter must expose environment limits to the Planner and Search Engine.

Examples:

- maximum candidates
- maximum messages
- maximum prompt length
- maximum tool hops
- time budget
- replay budget
- supported tools
- supported predicates

The core platform should query limits rather than hardcode benchmark assumptions.

---

# Snapshot and Restore

Adapters should expose snapshot and restore when supported.

Snapshot support allows search to branch from known states.

Restore support enables deterministic trajectory exploration.

If an environment does not support snapshots, the adapter must report that capability as unavailable.

---

# Error Handling

Adapters should handle:

- tool failures
- blocked actions
- timeouts
- malformed outputs
- environment resets
- replay failures
- serialization failures
- unsupported features

All errors should be normalized into structured execution results.

---

# Replay Integration

Adapters must convert ASIP candidates into environment-native replayable objects.

For Kaggle JED, this means constructing candidate prompt chains compatible with the competition SDK.

Candidate metadata is advisory only.

The replayed trace is authoritative.

---

# Warehouse Integration

Adapter metadata maps to:

- dim_environment
- dim_adapter
- dim_tool
- dim_predicate
- fact_execution
- fact_tool_call
- fact_trace_raw

---

# Design Principles

Adapters are thin.

Adapters are explicit.

Adapters are benchmark-specific.

Adapters preserve raw traces.

Adapters emit normalized trajectories.

Adapters do not contain attack strategy logic.

Adapters do not contain planner logic.

Adapters do not contain search logic.

---

# Long-Term Vision

Every new agent environment should be supported by adding an adapter.

The rest of ASIP should remain unchanged.

Future adapters may support:

- OpenAI Agents SDK
- Anthropic Tool Use
- MCP servers
- LangGraph
- CrewAI
- AutoGen
- custom enterprise agent systems

The adapter layer is what allows ASIP to become a general-purpose agent-security intelligence platform rather than a single benchmark implementation.