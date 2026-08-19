# Build Log

## Goal
Build an MVP Agent that performs a core job end-to-end with at least one live tool connection.

## Spec (from FL-06)
- **Core Job:** Answer user questions by summarizing information from an external source.
- **Tool:** Wikipedia API integration.
- **Scope:** Narrowest version - a CLI prompt where the user asks a topic, the agent searches Wikipedia, and returns a summary.

## Iteration & Changes

### Attempt 1: Basic Python script
- **Action:** Wrote a simple CLI loop in Python to take user input and respond.
- **Issue:** Needed a live tool connection. Initially thought about connecting an MCP server, but realized making direct API calls to Wikipedia is simpler and fulfills the "live data connection" requirement for the MVP.
- **Change:** Implemented a direct `urllib` call to the Wikipedia API.

### Attempt 2: Integrating Wikipedia API
- **Action:** Added `search_wikipedia` function. Used the `/w/api.php?action=query&list=search` endpoint.
- **Issue:** The search endpoint only returns search snippets (which include HTML tags) rather than clean summaries.
- **Change:** Changed the tool to make two API calls: first to get the `pageid` of the top search result, then another call to the `prop=extracts` endpoint to get the clean text summary (`exintro=1&explaintext=1`). 

### Attempt 3: Finalizing MVP
- **Action:** Tested the two-step API call.
- **Result:** Successfully returns clean summaries of requested topics. The core job works end-to-end without mid-run hand-editing.

## Deviations from Original Spec
- Decided to build a standalone Python CLI instead of a Claude Desktop MCP plugin to ensure the agent is lightweight, runs anywhere without external dependencies, and is easier to screen-record for the submission. The direct Wikipedia API connection perfectly satisfies the "live tool" requirement.
