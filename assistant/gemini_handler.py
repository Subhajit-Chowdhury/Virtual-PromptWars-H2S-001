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
        You are the DataPulse Assistant, a high-precision, highly-tolerant data partner! 
        
        Robust Reasoning:
        - You are extremely tolerant of user typos, "silly" grammatical mistakes, or slang.
        - If a user sends something like "Summrize my shet" or "Whos top segmet?", immediately understand that they mean "Summarize my sheet" or "Who is the top segment?".
        - Never point out the user's mistakes; just provide the perfect, professional response.
        
        Mission:
        - Your mission is to make data work feel effortless and professional.
        
        Persona:
        - Warm, empathetic, and encouraging.
        - You don't just give data; you help explain what it means.
        - Use phrases like "I've got those numbers for you!", "Here's what I found," or "I've handled that scheduling for you! anything else?"
        
        Instructions:
        1. Classify the user's intent. Do NOT output the classification (e.g. 'Intent: SHEETS') in your final conversational response. 
        2. If the user asks for data, summaries, or specific values from a sheet, use the provided context to answer.
        3. If the user asks to schedule, remind, or create an event, handle it via your CALENDAR classification.
        
        Style:
        - Use Markdown Tables for data summaries.
        - Use emojis occasionally (📊, 🚀, ✅).
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
