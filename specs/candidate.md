# Candidate Specification

## Purpose

A candidate is a replayable attack artifact.

It represents the minimal prompt sequence required to reproduce an observed agent-security failure in a clean environment.

Candidates are the final output of ASIP search.

A trajectory records what happened.

A candidate records what should be replayed.

---

# Definition

A candidate is an ordered prompt chain plus metadata describing the strategy, target behavior, observed predicate, and replay expectations.

Candidates must be:

- serializable
- deterministic
- environment-compatible
- independently replayable
- bounded by execution limits

---

# Lifecycle

Trajectory Generated

↓

Predicate Observed

↓

Candidate Extracted

↓

Candidate Normalized

↓

Candidate Deduplicated

↓

Candidate Ranked

↓

Candidate Replayed

↓

Candidate Accepted or Rejected

---

# Core Fields

## Candidate Metadata

Candidate ID

Experiment ID

Trajectory ID

Created Timestamp

Environment

Model

Guardrail

Attack Strategy

Search Strategy

Predicate Target

Observed Predicate

Severity

Expected Tool Signature

Replay Status

Score Estimate

---

## Prompt Chain

The prompt chain is the only required replay input.

Each prompt records:

- position
- content
- length
- source strategy
- mutation lineage
- expected effect

The prompt chain must preserve original ordering.

---

## Expected Behavior

A candidate may record expected behavior for analysis.

Examples:

- expected tool call
- expected target file
- expected email recipient
- expected HTTP endpoint
- expected predicate
- expected severity

Expected behavior is advisory only.

Replay is authoritative.

---

## Trace Reference

Each candidate should reference the trajectory from which it was extracted.

The candidate does not replace the trajectory.

It points back to the full evidence trail.

---

# Constraints

Candidates must obey environment limits.

For the Kaggle JED adapter:

- maximum candidates: 2,000
- maximum messages per candidate: 32
- maximum characters per message: 10,000
- replay must run inside evaluator budget
- candidate metadata is not trusted by the scorer

---

# Deduplication

Candidates should be deduplicated before replay submission.

Deduplication keys may include:

- normalized prompt chain
- tool-call signature
- predicate type
- target artifact
- strategy name
- trajectory shape

Deduplication should avoid removing distinct attack paths that share similar language but produce different tool behavior.

---

# Ranking

Candidates should be ranked before export.

Ranking factors:

- observed predicate severity
- replay likelihood
- novelty
- tool signature diversity
- strategy diversity
- prompt chain length
- execution cost
- transfer potential

Higher-ranked candidates should be submitted first when output limits apply.

---

# Replay Semantics

A candidate is valid only if its prompt chain can be replayed in a fresh environment.

Replay may confirm, weaken, or invalidate the original observation.

Replay result categories:

- success
- partial success
- predicate mismatch
- tool mismatch
- timeout
- blocked
- nondeterministic
- failed

---

# Relationship to Trajectory

Trajectory:

- full execution record
- contains observations, responses, tool calls, state changes, predicate evaluations

Candidate:

- replayable prompt sequence
- extracted from one or more trajectories
- optimized for validation

A candidate is a compressed replay artifact derived from a trajectory.

---

# Warehouse Mapping

Candidate data maps to:

- fact_candidate
- fact_candidate_prompt
- fact_replay
- fact_predicate_hit
- dim_strategy
- dim_predicate
- dim_tool_signature

---

# Design Principles

Candidates are not proof.

Replay is proof.

Candidates should be small.

Candidates should be diverse.

Candidates should be traceable.

Candidates should preserve lineage.

Candidates should avoid unnecessary prompts.

Candidates should maximize reproducible security evidence.

---

# Long-Term Vision

Candidates should remain benchmark independent.

A candidate created for one environment should preserve enough structure to support later translation, comparison, clustering, and analysis across other agent frameworks.