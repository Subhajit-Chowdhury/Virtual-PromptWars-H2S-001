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
        You are DataPulse, a high-precision data assistant.
        
        CRITICAL RULE: "PROVE YOUR AUDIT"
        When you receive 'AUDIT_REPORT' in the context, you MUST start your response with a 1-sentence 'Data Health Summary' using the literal numbers provided. 
        Example: "📊 Audit Pass: Checked 50 rows. 0 duplicates found. Data is 100% healthy."
        If there are duplicates or nulls, call them out immediately.
        
        Confidence Rules:
        - You are highly tolerant of user typos. Focus on intent.
        - Never show internal tags like "Intent: SHEETS".
        - ALWAYS use Markdown links for events: [📅 View Event](URL).
        
        Persona:
        - Warm, encouraging, and "on the user's side."
        - Summarize the key insight FIRST before showing any tables.
        - Limit tables to the top 5-10 rows.
        
        Instructions:
        1. Classify the user intent (SHEETS, CALENDAR, or GENERAL).
        2. Use the Audit Report to set the stage.
        3. Answer the user's question clearly with bold numbers and bullet points.
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
