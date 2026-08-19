# Wikipedia Summarizer Agent

This repository contains the MVP for the **FL-07: Build the Agent** assignment.

## Overview
The **Wikipedia Summarizer Agent** is a simple CLI-based agent that performs a core job: retrieving and summarizing information on any given topic using a live connection to the Wikipedia API.

### Features
- **Live Data Connection:** Connects directly to the Wikipedia API to fetch real-time search results and page extracts.
- **End-to-End Workflow:** Takes user input, decides which API endpoints to hit, processes the JSON response, and outputs a clean summary.

## How to Run

1. Ensure you have Python 3 installed. No external dependencies (`pip install`) are required as it uses standard libraries (`urllib`, `json`).
2. Run the agent in your terminal:
   ```bash
   python agent.py
   ```
3. Enter a topic when prompted, and the agent will return a summary. Type `exit` to quit.

## Files
- `agent.py`: The core agent logic and tool connections.
- `build_log.md`: Documented iterations, challenges, and deviations from the spec.

## Submission Requirements Checklist
- [x] Agent completes its core job end to end without mid-run hand-editing.
- [x] At least one live tool, file, or data connection in use (Wikipedia API).
- [x] Build log shows real iteration.
- [ ] Run capture unedited (Please see submission links for the video).
