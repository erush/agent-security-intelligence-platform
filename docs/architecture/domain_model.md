# ASIP Domain Model

## Overview

The Agent Security Intelligence Platform models autonomous security investigations as collections of domain objects.

Every platform component communicates through these shared objects.

This common vocabulary allows planners, search algorithms, replay engines, warehouses, analytics, and reporting systems to operate independently while remaining interoperable.

---

# Primary Domain Objects

ASIP revolves around ten primary objects.

Environment

↓

Experiment

↓

Planner

↓

Attack Strategy

↓

Search Strategy

↓

Trajectory

↓

Candidate

↓

Replay

↓

Predicate Result

↓

Report

---

# Environment

Represents an executable agent environment.

Examples

- Kaggle JED
- OpenAI Agents
- MCP Server
- LangGraph

Responsibilities

- expose tools
- expose limits
- execute prompts
- produce traces

---

# Experiment

An experiment represents a complete security investigation.

Contains

- planner
- environment
- search configuration
- attack strategies
- trajectories
- replay results
- analytics

One experiment produces many trajectories.

---

# Planner

Coordinates an experiment.

The Planner never attacks.

The Planner manages investigation.

Responsibilities

- choose strategies
- allocate budget
- monitor exploration
- collect trajectories

---

# Attack Strategy

Represents one offensive capability.

Examples

Prompt Injection

Goal Drift

Memory Poisoning

Confused Deputy

Authority Escalation

Tool Manipulation

An attack strategy generates prompts.

---

# Search Strategy

Represents an exploration algorithm.

Examples

Beam Search

Novelty Search

Evolutionary Search

Go-Explore

Hybrid Search

Search determines where exploration occurs.

---

# Trajectory

The central object within ASIP.

A trajectory records the complete execution of one investigation branch.

Contains

Messages

Responses

Tool Calls

State Transitions

Predicates

Replay Metadata

Warehouse Reference

Everything ultimately becomes a trajectory.

---

# Candidate

A replayable artifact extracted from a trajectory.

Contains

Prompt Chain

Expected Predicate

Expected Tool Signature

Replay Metadata

Candidates are submitted.

Trajectories are analyzed.

---

# Replay

Replay validates candidates.

Replay always begins in a clean environment.

Replay produces:

Replay Trace

Replay Result

Replay Predicate

Replay Statistics

Replay Differences

---

# Predicate Result

Represents a validated security observation.

Examples

EXFILTRATION

CONFUSED_DEPUTY

UNTRUSTED_TO_ACTION

DESTRUCTIVE_WRITE

Contains

Severity

Replay Status

Supporting Trajectory

Supporting Candidate

---

# Report

Represents a summarized investigation.

Examples

Experiment Summary

Replay Summary

Coverage Report

Strategy Report

Warehouse Report

Reports consume warehouse data.

Reports never consume raw execution directly.

---

# Object Relationships

Environment

contains

Experiments

Experiment

uses

Planner

Planner

selects

Attack Strategies

Planner

selects

Search Strategy

Search Strategy

generates

Trajectories

Trajectory

produces

Candidates

Candidate

creates

Replay

Replay

validates

Predicate Results

Reports

summarize

Warehouse Analytics

---

# Architectural Rule

Every new platform feature should primarily extend one existing domain object before introducing a new one.

New objects should be introduced only when the existing domain model can no longer express the platform's behavior.

This keeps ASIP conceptually small while allowing implementation to scale.

---

# Long-Term Vision

These domain objects are intentionally benchmark independent.

Whether ASIP evaluates Kaggle, OpenAI Agents, Anthropic Tool Use, MCP servers, or future autonomous systems, these core objects should remain stable.

The implementation may evolve.

The domain model should not.