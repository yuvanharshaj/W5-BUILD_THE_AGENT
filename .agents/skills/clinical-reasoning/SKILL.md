# Clinical Reasoning Simulation Skill

## Purpose

Perform structured educational reasoning over synthetic cases.

## Process

### 1. Retrieve

Read `/workspace/data/synthetic_cases.json`.

Locate the requested case by case ID.

### 2. Extract

Extract:

- case ID;
- case title;
- symptoms;
- observations;
- candidate explanations;
- prior probabilities;
- evidence weights.

### 3. Match Evidence

For each candidate, compare the observed evidence with the candidate's supplied evidence weights.

### 4. Calculate

Calculate an educational score.

Use:

score = prior_probability × average_matching_evidence

Then normalize the scores across all candidates.

The calculation is educational and is not a clinically validated probability model.

### 5. Rank

Sort candidates from highest score to lowest score.

### 6. Summarize

Explain:

- strongest supporting evidence;
- weaker evidence;
- candidate ranking;
- uncertainty.

Do not expose hidden chain-of-thought.

### 7. Generate Report

Generate a Markdown report containing:

- case summary;
- evidence;
- candidate comparison;
- educational probability scores;
- calculation method;
- ranked result;
- reasoning summary;
- limitations.

### 8. Save

Save the report to:

`/workspace/outputs/<case-id>-analysis.md`

### 9. Verify

Check that the output file exists and contains the generated report.

### 10. Complete

Return the report summary to the user only after successful verification.
