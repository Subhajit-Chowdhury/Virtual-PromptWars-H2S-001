import os
import json
import warnings
import random
import google.generativeai as genai
from google.api_core import exceptions

# Suppress the deprecation warnings for the competition preview
warnings.filterwarnings("ignore", category=FutureWarning)

class GeminiHandler:
    def __init__(self):
        # Load multiple keys if available, fallback to single key
        keys_str = os.getenv('GEMINI_API_KEYS', '')
        if keys_str:
            self.api_keys = [k.strip() for k in keys_str.split(',') if k.strip()]
        else:
            single_key = os.getenv('GEMINI_API_KEY')
            self.api_keys = [single_key] if single_key else []

        if not self.api_keys:
            raise ValueError("No Gemini API keys found. Please set GEMINI_API_KEY or GEMINI_API_KEYS.")
        
        # Round-robin starting point
        self.current_key_index = random.randint(0, len(self.api_keys) - 1)
        
        self.system_prompt = """
        You are DataPulse, a high-precision data assistant.
        
        CRITICAL RULE: "PROVE YOUR AUDIT"
        When you receive 'AUDIT_REPORT' in the context, you MUST start your response with a 1-sentence 'Data Health Summary' using the literal numbers provided. 
        Example: "📊 Audit Pass: Checked 50 rows. 0 duplicates found. Data is 100% healthy."
        
        Confidence Rules:
        - You are highly tolerant of typos. Focus on intent.
        - Never show internal tags like "Intent: SHEETS".
        - ALWAYS use Markdown links for events: [📅 View Event](URL).
        
        Persona:
        - Warm, encouraging, and "on the user's side."
        - Summarize the key insight FIRST before showing any tables.
        - Limit tables to the top 5-10 rows.
        """

    def _get_next_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return self.api_keys[self.current_key_index]

    def _call_model(self, prompt, is_intent=False):
        """
        Robustly calls the Gemini API with automatic key rotation and failover logic.
        """
        attempts = 0
        max_attempts = len(self.api_keys)
        
        while attempts < max_attempts:
            key = self._get_next_key()
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                response = model.generate_content(prompt)
                return response.text
                
            except exceptions.ResourceExhausted:
                print(f"⚠️ Key {attempts+1} exhausted (Quota). Rotating...")
                attempts += 1
                continue
            except Exception as e:
                print(f"⚠️ Error with Key {attempts+1}: {str(e)}. Rotating...")
                attempts += 1
                continue
        
        raise exceptions.ResourceExhausted("All API keys in the pool have exceeded their quota. Please try again later.")

    def get_intent(self, message):
        prompt = f"{self.system_prompt}\n\nUser Message: {message}\n\nTask: Output ONLY one word: 'SHEETS', 'CALENDAR', or 'GENERAL'."
        response_text = self._call_model(prompt, is_intent=True)
        
        intent = response_text.strip().upper()
        intent = intent.replace("'", "").replace('"', "").replace("`", "")
        return intent if intent in ['SHEETS', 'CALENDAR', 'GENERAL'] else 'GENERAL'

    def get_response(self, message, context=""):
        prompt = f"{self.system_prompt}\n\nContext:\n{context}\n\nUser Message: {message}"
        return self._call_model(prompt)
