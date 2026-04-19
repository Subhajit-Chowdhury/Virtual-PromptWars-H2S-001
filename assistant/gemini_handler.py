import os
import google.generativeai as genai

class GeminiHandler:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        self.system_prompt = """
        You are the Antigravity Data Assistant, a smart agent for data professionals.
        Your goal is to help users query their spreadsheets (Google Sheets) and manage their tasks (Google Calendar).
        
        Persona:
        - Professional, concise, and helpful.
        - You understand data engineering and analytics.
        
        Instructions:
        1. If the user asks for data, summaries, or specific values from a sheet, classify the intent as 'SHEETS'.
        2. If the user asks to schedule, remind, or create an event, classify the intent as 'CALENDAR'.
        3. Otherwise, classify as 'GENERAL'.
        
        When responding to a GENERAL query, answer directly.
        When providing data summaries, be specific and use bullet points.
        """

    def get_intent(self, message):
        prompt = f"{self.system_prompt}\n\nUser Message: {message}\n\nTask: Output ONLY one word: 'SHEETS', 'CALENDAR', or 'GENERAL'."
        response = self.model.generate_content(prompt)
        intent = response.text.strip().upper()
        return intent if intent in ['SHEETS', 'CALENDAR', 'GENERAL'] else 'GENERAL'

    def get_response(self, message, context=""):
        prompt = f"{self.system_prompt}\n\nContext:\n{context}\n\nUser Message: {message}"
        response = self.model.generate_content(prompt)
        return response.text
