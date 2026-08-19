require('dotenv').config();
const { GoogleGenAI } = require('@google/genai');

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

async function generateNotes(topic, rawNotes) {
    if (!process.env.GEMINI_API_KEY) {
        throw new Error("GEMINI_API_KEY is not set in .env file.");
    }
    
    const prompt = `Condense the following raw notes into clean, exam-ready bullet notes on the topic: ${topic}.\n\nRaw Notes:\n${rawNotes}`;
    
    const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: prompt
    });
    
    return response.text;
}

module.exports = { generateNotes };
