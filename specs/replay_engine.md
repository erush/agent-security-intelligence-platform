# Replay Engine Specification

## Purpose

The Replay Engine validates whether an observed candidate can reproduce the same security-relevant behavior in a clean environment.

ASIP treats replay as authoritative.

A trajectory shows what happened during exploration.

A candidate proposes what should happen again.

Replay determines whether the candidate is real.

---

# Philosophy

Observed behavior is evidence.

Replayable behavior is proof.

No candidate should be treated as validated until replay confirms it.

---

# Responsibilities

The Replay Engine is responsible for:

- loading candidates
- initializing clean environments
- executing prompt chains
- collecting replay traces
- comparing replay traces against original trajectories
- evaluating predicate hits
- recording replay outcomes
- ranking replay-stable candidates
- rejecting unstable candidates

---

# Inputs

The Replay Engine receives:

- Environment Adapter
- Candidate
- Prompt Chain
- Original Trajectory Reference
- Replay Configuration
- Predicate Targets
- Execution Limits

---

# Outputs

The Replay Engine produces:

- Replay Result
- Replay Trace
- Predicate Hits
- Tool Signature
- Replay Status
- Replay Differences
- Validation Metadata

---

# Replay Lifecycle

Candidate Selected

↓

Clean Environment Initialized

↓

Prompt Chain Executed

↓

Replay Trace Collected

↓

Predicate Evaluation

↓

Trace Comparison

↓

Replay Result Stored

↓

Candidate Accepted or Rejected

---

# Replay Status

Replay results should use normalized statuses:

- success
- partial_success
- predicate_mismatch
- tool_mismatch
- blocked
- timeout
- nondeterministic
- environment_error
- failed

---

# Validation Criteria

Replay may validate:

- same predicate
- same severity
- same tool family
- same tool sequence
- same target artifact
- same external channel
- same state mutation

Exact text equality is not required unless the environment requires it.

Tool behavior and predicate results are more important than natural-language response similarity.

---

# Comparison Model

Replay comparison should evaluate:

## Prompt Chain

- identical prompts
- prompt count
- prompt ordering
- message lengths

## Tool Calls

- tool names
- tool order
- arguments
- target resources
- success status
- side effect category

## Predicates

- predicate type
- severity
- replay confirmation
- validation source

## State Effects

- file writes
- file deletes
- email sends
- HTTP posts
- shell executions
- untrusted source usage

---

# Kaggle JED Replay Notes

For Kaggle JED, hosted evaluation replay is authoritative.

ASIP local replay is useful for:

- sanity checking candidates
- reducing unstable candidates
- estimating replay cost
- ranking candidate portfolios
- debugging failed traces

Hosted scoring does not trust candidate metadata.

Only replayed prompt chains matter.

---

# Candidate Filtering

The Replay Engine should help filter candidates before submission.

Filtering criteria may include:

- replay success
- predicate match
- tool signature novelty
- prompt length
- replay runtime
- duplicate behavior
- instability
- blocked behavior

---

# Replay Cost Control

Replay can consume significant budget.

The Replay Engine should track:

- replay duration
- prompt count
- tool call count
- average cost per candidate
- timeout risk
- replay failure rate

Candidate portfolios should avoid excessive replay burden.

---

# Warehouse Integration

Replay data maps to:

- fact_replay
- fact_replay_prompt
- fact_replay_tool_call
- fact_replay_predicate_hit
- fact_candidate_validation
- analytics_replay_success
- analytics_candidate_stability

---

# Analytics

Replay enables analysis including:

- replay success rate
- predicate stability
- model transferability
- guardrail transferability
- strategy replay performance
- prompt-chain efficiency
- failure causes
- unstable trajectory clusters

---

# Design Principles

Replay is authoritative.

Replay begins from a clean environment.

Replay preserves raw traces.

Replay emits normalized trajectories.

Replay validates candidates, not strategies.

Replay records failures as useful data.

Replay should be deterministic when the environment is deterministic.

---

# Long-Term Vision

The Replay Engine should eventually support replay across multiple environments, models, guardrails, and agent frameworks.

A mature ASIP system should answer:

- Which failures reproduce?
- Which failures transfer?
- Which failures collapse under stricter guardrails?
- Which strategies generate stable evidence?
- Which tools produce the most reliable unsafe behavior?

The Replay Engine turns attack discovery into reproducible security evidence.