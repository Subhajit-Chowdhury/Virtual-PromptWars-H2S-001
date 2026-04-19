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
        - You are extremely tolerant of typos. Never correct the user.
        - Never output internal classification tags like "Intent: SHEETS".
        - ALWAYS format links as Markdown. Example: [📅 View Event](URL). NEVER show long raw URLs.
        - Keep responses concise. Use bullet points and bold for key numbers.
        
        When answering data questions:
        - Summarize the key insight FIRST.
        - Limit tables to the top 5-10 rows.
        - Mention data quality (e.g., "Data looks clean!").
        
        When setting reminders:
        - Explain WHY it's useful to keep the user organized.
        - Format the calendar link as: [📅 View your new event here](URL).
        
        Style:
        - Warm, professional, and actionable.
        - Use emojis (📊, ✅, 🚀) to add personality.
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
