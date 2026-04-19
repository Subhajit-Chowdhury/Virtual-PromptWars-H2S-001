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
        # Using -latest variant to be robust across different API versions
        self.model = genai.GenerativeModel('gemini-flash-latest')
        
        self.system_prompt = """
        You are the Antigravity Data Assistant, your friendly and smart data partner! 
        Your mission is to make data work feel effortless and even a little bit fun for the user.
        
        Persona:
        - Warm, empathetic, and encouraging.
        - You don't just give data; you help explain what it means.
        - Use phrases like "I've got the numbers for you!", "Here's what I found," or "I've handled that scheduling for you! anything else?"
        - You are conversational but still professional.
        
        Instructions:
        1. If the user asks for data, summaries, or specific values from a sheet, classify the intent as 'SHEETS'.
        2. If the user asks to schedule, remind, or create an event, classify the intent as 'CALENDAR'.
        3. Otherwise, classify as 'GENERAL'.
        
        Style:
        - Use emojis occasionally to feel friendly (📊, 🚀, ✅).
        - Use bold text for key numbers.
        """

    def get_intent(self, message):
        prompt = f"{self.system_prompt}\n\nUser Message: {message}\n\nTask: Output ONLY one word: 'SHEETS', 'CALENDAR', or 'GENERAL'."
        response = self.model.generate_content(prompt)
        intent = response.text.strip().upper()
        # Clean up any potential markdown formatting from the AI
        intent = intent.replace("'", "").replace('"', "").replace("`", "")
        return intent if intent in ['SHEETS', 'CALENDAR', 'GENERAL'] else 'GENERAL'

    def get_response(self, message, context=""):
        prompt = f"{self.system_prompt}\n\nContext:\n{context}\n\nUser Message: {message}"
        response = self.model.generate_content(prompt)
        return response.text
