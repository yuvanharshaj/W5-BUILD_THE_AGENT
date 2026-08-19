const fs = require('fs');
const path = require('path');
const { generateNotes } = require('./geminiClient');

async function runAgent(topic) {
    console.log(`Starting VTU Study Notes Agent for topic: "${topic}"...`);
    
    const inputPath = path.join(__dirname, '../input/sample-notes.txt');
    const outputDir = path.join(__dirname, '../output');
    const outputPath = path.join(outputDir, `${topic.replace(/[^a-zA-Z0-9]/g, '_')}-notes.md`);
    
    try {
        console.log("Reading raw notes from input/sample-notes.txt...");
        if (!fs.existsSync(inputPath)) {
            throw new Error("Input file not found. Please create input/sample-notes.txt.");
        }
        const rawNotes = fs.readFileSync(inputPath, 'utf8');
        
        console.log("Connecting to Google Gemini API to generate exam-ready notes...");
        const cleanNotes = await generateNotes(topic, rawNotes);
        
        console.log("Notes generated successfully. Writing to output directory...");
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }
        
        fs.writeFileSync(outputPath, cleanNotes, 'utf8');
        console.log(`Done! Your notes are ready at: output/${path.basename(outputPath)}`);
        
    } catch (error) {
        console.error("Agent failed to complete the task:", error.message);
        process.exit(1);
    }
}

module.exports = { runAgent };
