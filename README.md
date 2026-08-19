# VTU Study Notes Agent

This repository contains the MVP for the **FL-07: Build the Agent** assignment.

## Overview
The **VTU Study Notes Agent** reads your raw study notes, connects to the Google Gemini API, and condenses them into clean, exam-ready bullet points.

### Features
- **Live Tool Connection:** Connects directly to the Google Gemini API via `@google/genai`.
- **End-to-End Workflow:** Reads `input/sample-notes.txt`, generates structured notes, and saves them to the `output/` directory—all in one run.

## Setup Instructions

1. Ensure you have [Node.js](https://nodejs.org/) installed.
2. Clone this repository and navigate into the folder.
3. Install the dependencies:
   ```bash
   npm install
   ```
4. Create a `.env` file in the root directory (you can rename `.env.example`) and add your API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   *(You can get an API key from Google AI Studio).*

## How to Run

1. Place your raw notes inside `input/sample-notes.txt`.
2. Run the agent via the CLI, passing the topic name as an argument:
   ```bash
   node src/index.js "Operating Systems"
   ```
3. The generated notes will appear in the `output/` folder.

## Submission Requirements Checklist
- [x] Agent completes its core job end to end without mid-run hand-editing.
- [x] At least one live tool, file, or data connection in use (Gemini API & local File System).
- [x] Build log shows real iteration.
- [ ] Run capture unedited (Please see submission links for the video).
