# Build Log: VTU Study Notes Agent

## Goal
Build an MVP Agent that performs a core job end-to-end with at least one live tool connection.

## Spec (from FL-06)
- **Core Job:** Condense raw notes into exam-ready bullet points for a given topic.
- **Tool:** Google Gemini API (via `@google/genai`).
- **Scope:** Narrowest version - read `sample-notes.txt`, call the Gemini API, and write the output to a new markdown file.

## Iteration & Changes

### Attempt 1: Setup and Basic Connection
- **Action:** Initialized the Node.js project, installed `dotenv` and `@google/genai`.
- **Issue:** Needed to verify the API key and connection before building the main loop.
- **Change:** Set up a quick `geminiClient.js` test.

### Attempt 2: Building the Core Agent Loop
- **Action:** Built `agent.js` to read from the `input` folder, pass it to `geminiClient`, and write to the `output` folder.
- **Issue:** Node's `fs` module needs the directories to exist before writing. 
- **Change:** Added `fs.mkdirSync` with `{ recursive: true }` before writing the output file.

### Attempt 3: CLI integration
- **Action:** Wired up `index.js` to accept command line arguments so the topic can be passed dynamically (e.g., `node src/index.js "Data Structures"`).
- **Result:** Agent runs successfully end-to-end without mid-run intervention.

## Cut from spec
- **Multi-file input:** Intended to read a whole directory of notes, but cut down to a single `sample-notes.txt` to ensure the MVP works flawlessly first.
- **Chat Memory:** Removed conversational aspects. The agent does a single shot generation to keep the core loop simple and reliable.
