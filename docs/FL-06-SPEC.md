# FL-06 Agent Specification

## Agent Name

Clinical Reasoning AI Agent

## Purpose

An educational AI agent that demonstrates structured reasoning over synthetic cases.

## Core Job

Given a synthetic case, retrieve the case from a workspace dataset, analyze the available evidence, calculate educational probability scores, rank synthetic candidates, and generate a structured report.

## Input

A synthetic case ID or request to analyze an available synthetic case.

## Data Source

Synthetic JSON dataset stored in the workspace.

## Tools

- Filesystem
- Code Execution

## Output

A structured Markdown educational simulation report.

## MVP Workflow

1. Receive request.
2. Retrieve dataset.
3. Find case.
4. Analyze evidence.
5. Calculate scores.
6. Rank candidates.
7. Generate report.
8. Save report.
9. Verify report.
10. Return result.

## Constraints

- Synthetic data only.
- No real diagnosis.
- No treatment recommendations.
- No real patient information.
- No unnecessary production features.

## FL-07 MVP Goal

Demonstrate one complete end-to-end agent run with at least one real workspace data connection.
