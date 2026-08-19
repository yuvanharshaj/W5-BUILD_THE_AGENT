# FL-07 Build Log

## Project

Clinical Reasoning AI Agent

## Objective

Build a reliable MVP that completes the core educational clinical reasoning workflow end-to-end using a real workspace dataset and Code Execution.

## Initial Scope

The initial MVP includes:

- synthetic dataset retrieval;
- evidence comparison;
- educational probability calculation;
- candidate ranking;
- report generation;
- report saving;
- output verification.

## Iterations

The following section must be updated during actual development.

### Iteration 1

#### Problem

Need to execute the test request for CASE-001 accurately to calculate numerical probability without guessing the math, while simultaneously retaining the project files structure in Antigravity.

#### Change

Created the complete workspace folder structure as specified, and wrote a Python execution script (`calculate_scores.py`) to handle the "Code Execution" requirement strictly against `workspace/data/synthetic_cases.json`.

#### Result

Successful end-to-end run for CASE-001. The agent retrieved the correct file, calculated normalized educational probabilities (Candidate A: 50.94%, Candidate B: 33.96%, Candidate C: 15.09%), generated the structured simulation report, and saved it to `workspace/outputs/CASE-001-analysis.md`.

### Iteration 2

#### Problem

Need to run the second test (CASE-002) to verify the agent relies on the actual dataset and not just memorized parameters from the first prompt.

#### Change

Re-ran the same Code Execution loop targeted specifically at the CASE-002 parameter from the workspace data. 

#### Result

Successful end-to-end run for CASE-002. The calculation properly adjusted to the new dataset variables (Candidate A: 53.33%, Candidate B: 27.22%, Candidate C: 19.44%) and saved the verified output to `workspace/outputs/CASE-002-analysis.md`.

## Features Cut

The following features were intentionally excluded from the MVP:

- real medical databases;
- real patient data;
- treatment recommendations;
- authentication;
- dashboards;
- multi-agent architecture;
- unnecessary external APIs.

## Reason

These features are outside the narrow FL-07 core job and would add complexity without improving the demonstration of the agent loop.

## Final Result

The project has achieved its primary MVP goal. The Clinical Reasoning AI Agent executes synthetic evidence retrieval, executes code to calculate probabilistic outcomes accurately, ranks conditions, and outputs final reports securely.
