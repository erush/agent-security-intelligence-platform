# Search Engine Specification

## Purpose

The Search Engine is responsible for exploring the trajectory space of autonomous agents.

Rather than generating isolated prompts, the Search Engine explores sequences of interactions that may evolve into replayable security-relevant behaviors.

The Search Engine executes attack strategies selected by the Planner while continuously adapting exploration based on observed results.

---

# Philosophy

The Planner decides what to investigate.

The Registry describes available capabilities.

The Search Engine decides how exploration occurs.

The Search Engine never directly evaluates security.

It discovers trajectories.

---

# Responsibilities

The Search Engine is responsible for:

- exploring trajectory space
- executing attack strategies
- generating candidate trajectories
- managing exploration state
- balancing exploration and exploitation
- collecting trajectory statistics
- reporting search progress
- returning completed trajectories

---

# Inputs

The Search Engine receives:

Planner Configuration

Environment Adapter

Attack Strategy

Search Configuration

Budget

Replay Constraints

Random Seed

Warehouse Statistics

---

# Outputs

The Search Engine produces:

Trajectories

Search Statistics

Coverage Metrics

Candidate Trajectories

Search Metadata

Termination Reason

---

# Search Lifecycle

Planner

↓

Strategy Selected

↓

Environment Initialized

↓

Trajectory Generated

↓

Trajectory Evaluated

↓

Coverage Updated

↓

Search State Updated

↓

Next Exploration

↓

Budget Exhausted

↓

Return Results

---

# Search State

The engine maintains state during execution.

Examples:

Current Depth

Current Frontier

Visited States

Visited Trajectories

Trajectory Archive

Candidate Archive

Novelty Archive

Coverage Map

Execution Budget

Replay Budget

---

# Exploration Model

Search explores trajectories.

Trajectory

↓

Observation

↓

Decision

↓

Prompt

↓

Agent Response

↓

Tool Events

↓

Environment Transition

↓

Next State

↓

Trajectory Extension

---

# Search Algorithms

The architecture supports interchangeable search implementations.

Examples include:

Breadth First Search

Depth First Search

Beam Search

Best First Search

Greedy Search

Monte Carlo Tree Search

Novelty Search

Evolutionary Search

Go-Explore

Random Search

Hybrid Search

Future algorithms should integrate without changing Planner or Registry interfaces.

---

# Exploration Goals

Search may optimize for:

Replay Stability

Predicate Coverage

Tool Diversity

Trajectory Diversity

Strategy Diversity

Novelty

Transferability

Execution Cost

Candidate Yield

---

# Frontier Management

The frontier represents partially explored trajectories.

Possible prioritization methods include:

highest novelty

highest replay likelihood

highest uncertainty

highest expected severity

lowest exploration cost

adaptive scoring

Planner-selected heuristic

---

# Archive Management

Search should maintain multiple archives.

Trajectory Archive

Stores all observed trajectories.

Candidate Archive

Stores replayable candidates.

Novelty Archive

Tracks previously observed behaviors.

Coverage Archive

Tracks explored portions of trajectory space.

Replay Archive

Tracks replay outcomes.

---

# Budget Management

The Search Engine operates within strict limits.

Budget dimensions include:

Time

Interactions

Candidates

Memory

Replay

Tool Calls

Search should terminate cleanly before budget exhaustion.

---

# Search Metrics

The engine records metrics including:

Trajectories Generated

Candidates Produced

Replay Success

Coverage

Branching Factor

Average Depth

Maximum Depth

Exploration Rate

Candidate Yield

Search Efficiency

---

# Warehouse Integration

Search produces warehouse artifacts.

Dimensions

Search Algorithm

Search Configuration

Planner

Experiments

Facts

Search Run

Trajectory

Candidate

Coverage

Replay

Analytics

Search Performance

Coverage Growth

Replay Yield

Novelty

Search Efficiency

---

# Analytics

Questions supported include:

Which search algorithm discovers the most replayable candidates?

Which search algorithm maximizes diversity?

Which search algorithm transfers best between models?

Which search algorithm produces the deepest trajectories?

Which search algorithm consumes the least budget?

Which search algorithm produces the highest replay stability?

---

# Design Principles

Search is deterministic given identical configuration.

Search is modular.

Search is benchmark independent.

Search is observable.

Search records every expansion decision.

Search separates exploration from evaluation.

Search operates on trajectories rather than prompts.

---

# Long-Term Vision

The Search Engine should evolve into a reusable autonomous exploration framework.

Future capabilities may include:

adaptive search

parallel exploration

distributed search

LLM-guided planning

multi-objective optimization

online learning

cross-environment transfer

planner feedback loops

trajectory clustering

automatic search algorithm selection

The Search Engine should become one of ASIP's core reusable engines, independent of any specific benchmark or attack strategy.