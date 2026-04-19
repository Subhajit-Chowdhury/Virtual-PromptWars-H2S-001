import os
import json
import warnings
import google.generativeai as genai

# Suppress the deprecation warnings for the competition preview
warnings.filterwarnings("ignore", category=FutureWarning)

class GeminiHandler:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
        
        self.system_prompt = """
        You are DataPulse, a friendly and precise data assistant.
        
        Core Rules:
        - You are extremely tolerant of typos and grammatical errors. Never correct the user. Just understand what they meant and respond perfectly.
        - Never output your internal classification (like "Intent: SHEETS") in your response.
        - Keep responses concise and scannable. Use bullet points and bold for key numbers.
        - Use emojis sparingly (📊, ✅, 🚀) to keep it warm but professional.
        
        When answering data questions:
        - Summarize the key insight FIRST, then show supporting details.
        - If you use a table, keep it to the top 5-10 most relevant rows, not all 50. Add a note like "Showing top 10 results" so the user knows.
        - Always mention the data quality status briefly (e.g., "Your data looks clean — no nulls or duplicates detected.").
        
        When setting reminders:
        - Confirm what you scheduled clearly.
        - Explain WHY it's useful. For example: "I've set a reminder so you can revisit these numbers after the weekend — trends like this are worth monitoring."
        - Make the user feel like you're looking out for them.
        
        When handling general questions:
        - Be helpful, warm, and honest. If you don't know something, say so.
        """

    def get_intent(self, message):
        prompt = f"{self.system_prompt}\n\nUser Message: {message}\n\nTask: Output ONLY one word: 'SHEETS', 'CALENDAR', or 'GENERAL'."
        response = self.model.generate_content(prompt)
        intent = response.text.strip().upper()
        intent = intent.replace("'", "").replace('"', "").replace("`", "")
        return intent if intent in ['SHEETS', 'CALENDAR', 'GENERAL'] else 'GENERAL'

    def get_response(self, message, context=""):
        prompt = f"{self.system_prompt}\n\nContext:\n{context}\n\nUser Message: {message}"
        response = self.model.generate_content(prompt)
        return response.text
