# Planner Specification

## Purpose

The Planner is the central orchestration component of the Agent Security Intelligence Platform (ASIP).

The Planner does not generate prompts directly.

Instead, it coordinates the complete security investigation by selecting attack strategies, allocating exploration budget, scheduling execution, monitoring search progress, and determining when an investigation has produced sufficient evidence.

The Planner separates investigation management from attack generation.

---

# Philosophy

Attack strategies generate attacks.

Search strategies explore possibilities.

Execution interacts with environments.

The Planner coordinates all of them.

---

# Responsibilities

The Planner is responsible for:

- initializing investigations
- selecting attack strategies
- selecting search strategies
- allocating exploration budget
- prioritizing experiments
- monitoring progress
- collecting trajectories
- evaluating exploration coverage
- deciding when to terminate exploration
- producing candidate portfolios

The Planner never directly communicates with the target environment.

---

# Inputs

The Planner receives:

Environment Adapter

Attack Registry

Search Registry

Configuration

Experiment Specification

Time Budget

Search Budget

Previous Results

Warehouse Statistics

Replay Statistics

---

# Outputs

The Planner produces:

Execution Plan

Selected Attack Strategies

Selected Search Strategy

Budget Allocation

Experiment Schedule

Candidate Portfolio

Investigation Summary

---

# Investigation Lifecycle

Experiment Created

↓

Planner Initialized

↓

Environment Analysis

↓

Strategy Selection

↓

Search Selection

↓

Budget Allocation

↓

Execution Scheduling

↓

Trajectory Collection

↓

Coverage Analysis

↓

Candidate Selection

↓

Replay Preparation

↓

Investigation Complete

---

# Planning Stages

## Stage 1

Environment Assessment

Determine:

- supported tools
- supported predicates
- available search budget
- environment capabilities
- replay constraints

---

## Stage 2

Strategy Selection

Determine which attack strategies should participate.

Selection may consider:

- historical performance
- replay success
- novelty
- predicate coverage
- transferability

---

## Stage 3

Search Selection

Choose an exploration algorithm.

Examples:

Beam Search

Breadth First Search

Novelty Search

Evolutionary Search

Hybrid Search

---

## Stage 4

Budget Allocation

Allocate:

time

iterations

candidate quota

memory

replay allowance

Budget allocation should remain adaptive.

---

## Stage 5

Execution Scheduling

Coordinate execution order.

Possible scheduling methods:

round robin

priority queue

adaptive scheduling

bandit scheduling

coverage-driven scheduling

---

## Stage 6

Monitoring

Continuously evaluate:

coverage

novelty

candidate quality

budget consumption

replay stability

---

## Stage 7

Termination

The Planner terminates when:

budget expires

coverage saturates

candidate limit reached

time limit reached

planner confidence threshold reached

---

# Planner State

The Planner maintains state including:

Current Budget

Active Strategy

Completed Strategies

Search Depth

Trajectory Count

Replay Count

Candidate Count

Coverage Metrics

Experiment Metadata

---

# Decision Factors

Planner decisions may consider:

strategy performance

tool diversity

predicate diversity

trajectory novelty

replay stability

search depth

candidate quality

execution cost

environment capabilities

---

# Interaction Model

Planner

↓

Attack Strategy

↓

Search Strategy

↓

Execution Engine

↓

Trajectory

↓

Warehouse

↓

Planner

The Planner operates as a closed feedback loop.

Each completed trajectory informs future planning decisions.

---

# Warehouse Integration

Planner statistics should be recorded.

Examples:

planner runs

planner duration

strategy selection frequency

budget allocation

coverage progression

termination reason

planner version

---

# Analytics

Planner analytics may include:

strategy utilization

coverage growth

candidate yield

budget efficiency

trajectory generation rate

planner convergence

search saturation

---

# Design Principles

The Planner is deterministic when configured with a fixed seed.

The Planner is modular.

The Planner is benchmark independent.

The Planner is observable.

The Planner records every planning decision.

The Planner should support adaptive exploration without changing external interfaces.

---

# Long-Term Vision

Future versions of the Planner may support:

multi-agent coordination

parallel exploration

distributed execution

online learning

strategy recommendation

adaptive replay scheduling

automatic experiment design

benchmark comparison

The Planner should evolve into a general-purpose orchestration engine for autonomous security investigations rather than remaining specific to any single benchmark.