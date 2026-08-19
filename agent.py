import json
import os
from pathlib import Path

from google import genai
from google.genai import types


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent

DATA_FILE = ROOT / "workspace" / "data" / "synthetic_cases.json"

OUTPUT_DIR = ROOT / "workspace" / "outputs"

MODEL = "gemini-3.6-flash"


# ============================================================
# TOOL 1 — READ REAL WORKSPACE DATA
# ============================================================

def load_case(case_id: str) -> dict:
    """
    Reads the synthetic dataset from the real project
    workspace and retrieves the requested case.
    """

    if not DATA_FILE.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    with DATA_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    for case in data.get("cases", []):
        if case.get("id") == case_id:
            return case

    available_cases = [
        case.get("id", "UNKNOWN")
        for case in data.get("cases", [])
    ]

    raise ValueError(
        f"{case_id} was not found. "
        f"Available cases: {', '.join(available_cases)}"
    )


# ============================================================
# TOOL 2 — SAVE REPORT
# ============================================================

def save_report(
    case_id: str,
    report: str
) -> Path:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        OUTPUT_DIR /
        f"{case_id}-analysis.md"
    )

    output_file.write_text(
        report.strip() + "\n",
        encoding="utf-8"
    )

    return output_file


# ============================================================
# TOOL 3 — VERIFY REPORT
# ============================================================

def verify_report(
    output_file: Path
) -> int:

    if not output_file.is_file():
        raise RuntimeError(
            "Report verification failed: "
            "output file does not exist."
        )

    file_size = output_file.stat().st_size

    if file_size == 0:
        raise RuntimeError(
            "Report verification failed: "
            "output file is empty."
        )

    return file_size


# ============================================================
# MAIN AGENT
# ============================================================

def run_agent(
    case_id: str
) -> None:

    # --------------------------------------------------------
    # Check API key
    # --------------------------------------------------------

    api_key = os.environ.get(
        "GEMINI_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured "
            "in this PowerShell session."
        )

    print()
    print("=" * 72)
    print(
        "FL-07 — CLINICAL REASONING AI AGENT"
    )
    print("=" * 72)

    # --------------------------------------------------------
    # STEP 1 — Read workspace data
    # --------------------------------------------------------

    print()
    print(
        "STEP 1/5 — Reading workspace dataset..."
    )

    case = load_case(
        case_id
    )

    print(
        f"✓ Retrieved {case_id} from "
        "workspace/data/synthetic_cases.json"
    )

    # --------------------------------------------------------
    # Convert retrieved case into text
    #
    # IMPORTANT:
    # We deliberately send TEXT to Code Execution,
    # not application/json.
    # --------------------------------------------------------

    case_text = json.dumps(
        case,
        indent=2,
        ensure_ascii=False
    )

    # --------------------------------------------------------
    # STEP 2 — Initialize Gemini
    # --------------------------------------------------------

    print()
    print(
        "STEP 2/5 — Connecting to Gemini..."
    )

    client = genai.Client(
        api_key=api_key
    )

    print(
        f"✓ Gemini model: {MODEL}"
    )

    # --------------------------------------------------------
    # STEP 3 — Gemini Code Execution
    # --------------------------------------------------------

    print()
    print(
        "STEP 3/5 — Gemini using Code Execution..."
    )

    prompt = f"""
You are the Clinical Reasoning AI Agent
for the FlyRank FL-07 assignment.

This is an educational simulation using
synthetic data only.

The requested case is:

{case_id}

The following case was retrieved directly
from the project's real workspace dataset:

--- BEGIN CASE DATA ---

{case_text}

--- END CASE DATA ---

Your task is to analyze this synthetic case.

IMPORTANT REQUIREMENTS:

1. Use the supplied case data as the source
   of truth.

2. Compare every candidate condition.

3. You MUST use the Code Execution tool
   to perform the numerical scoring.

4. Write and execute Python code.

5. For every candidate calculate:

   average_matching_evidence =
   sum of matching evidence weights
   divided by number of symptoms

   raw_score =
   prior_probability × average_matching_evidence

   normalized_score =
   raw_score / sum of all raw scores

6. The calculation must actually be
   executed by the Code Execution tool.

7. Do not invent evidence.

8. If a candidate does not contain a weight
   for a symptom, use 0.0.

9. Rank candidates from highest normalized
   score to lowest.

10. The scores are educational only.
    They are NOT medically validated
    probabilities.

11. Do not provide real medical diagnosis.

12. Do not provide treatment advice.

13. Do not provide medication instructions.

14. Do not reveal private chain-of-thought.

15. Provide only a concise reasoning summary
    based on the supplied evidence and the
    executed calculations.

After completing the calculation, produce
the final report.

Use exactly this Markdown structure:

# Clinical Reasoning Simulation Report

**Case:** {case_id}

> Educational simulation using synthetic data.
> This is not a medical diagnosis, medical advice,
> or treatment recommendation.

## 1. Case Summary

Brief summary of the synthetic case.

## 2. Evidence

List the symptoms and observations.

## 3. Candidate Comparison

Use:

| Candidate | Educational Score | Supporting Evidence | Weak/Conflicting Evidence |
|---|---:|---|---|

## 4. Calculation

Explain:

score =
prior_probability × average_matching_evidence

Show the normalized scores produced
by Code Execution.

State that this is an educational
scoring method.

## 5. Ranked Result

List all candidates from highest
to lowest score.

## 6. Reasoning Summary

Give a concise explanation of the
ranking based on the supplied evidence.

Do not reveal hidden chain-of-thought.

## 7. Limitations

State that:

- all data is synthetic;
- candidate labels are fictional;
- the scoring method is educational;
- the system is not clinically validated;
- the result is not a medical diagnosis.

Return only the final Markdown report.
"""

    import time
    
    chat = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            temperature=0,
            tools=[
                types.Tool(
                    code_execution=types.ToolCodeExecution()
                )
            ]
        )
    )

    response = None
    max_retries = 5
    for attempt in range(max_retries):
        try:
            print(f"    (Attempt {attempt + 1}/{max_retries})...")
            response = chat.send_message(prompt)
            break
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < max_retries - 1:
                    print("    Model is experiencing high demand (503). Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    raise e
            else:
                raise e

    # --------------------------------------------------------
    # Check whether Code Execution was actually used
    # --------------------------------------------------------

    code_execution_used = False

    if response.candidates:

        for candidate in response.candidates:

            if not candidate.content:
                continue

            if not candidate.content.parts:
                continue

            for part in candidate.content.parts:

                if part.executable_code is not None:

                    code_execution_used = True

                    print()
                    print(
                        "✓ Gemini generated executable Python"
                    )

                    print()
                    print(
                        "EXECUTED CODE:"
                    )

                    print(
                        part.executable_code.code
                    )

                if part.code_execution_result is not None:

                    code_execution_used = True

                    print()
                    print(
                        "✓ Code Execution completed"
                    )

                    result_output = (
                        part.code_execution_result.output
                        or ""
                    )

                    print()
                    print(
                        "CODE EXECUTION RESULT:"
                    )

                    print(
                        result_output
                    )

    if not code_execution_used:

        raise RuntimeError(
            "Gemini did not use Code Execution. "
            "The run is not considered successful "
            "for FL-07."
        )

    # --------------------------------------------------------
    # Retrieve final report
    # --------------------------------------------------------

    report = (
        response.text.strip()
        if response.text
        else ""
    )

    if not report:

        raise RuntimeError(
            "Gemini returned an empty report."
        )

    print()
    print(
        "✓ Gemini generated the final report"
    )

    # --------------------------------------------------------
    # STEP 4 — Save report
    # --------------------------------------------------------

    print()
    print(
        "STEP 4/5 — Saving report..."
    )

    output_file = save_report(
        case_id,
        report
    )

    print(
        f"✓ Report saved to:"
    )

    print(
        f"  {output_file}"
    )

    # --------------------------------------------------------
    # STEP 5 — Verify report
    # --------------------------------------------------------

    print()
    print(
        "STEP 5/5 — Verifying report..."
    )

    file_size = verify_report(
        output_file
    )

    print(
        f"✓ Report verified successfully "
        f"({file_size} bytes)"
    )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print()
    print("=" * 72)
    print(
        "FINAL REPORT"
    )
    print("=" * 72)

    print()

    print(
        report
    )

    print()
    print("=" * 72)
    print(
        "END-TO-END AGENT RUN SUCCESSFUL"
    )
    print("=" * 72)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

def main():

    print()
    print(
        "Enter synthetic case ID "
        "(default: CASE-001)"
    )

    requested_case = input(
        "> "
    ).strip().upper()

    if not requested_case:

        requested_case = "CASE-001"

    try:

        run_agent(
            requested_case
        )

    except Exception as error:

        print()
        print("=" * 72)
        print(
            "AGENT RUN FAILED"
        )
        print("=" * 72)

        print()
        print(
            f"Error: {error}"
        )

        raise SystemExit(1)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()