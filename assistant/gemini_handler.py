import os
import json
import warnings
import random
import google.generativeai as genai

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
            raise ValueError("No Gemini API keys found. Set GEMINI_API_KEY or GEMINI_API_KEYS.")
        
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

    def _call_model(self, prompt):
        """
        Calls the Gemini API with automatic key rotation and failover.
        """
        attempts = 0
        max_attempts = len(self.api_keys)
        last_error = None
        
        while attempts < max_attempts:
            key = self._get_next_key()
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                if 'quota' in error_str or 'resource' in error_str or '429' in error_str:
                    print(f"Key {attempts+1} quota hit. Rotating...")
                    attempts += 1
                    continue
                else:
                    # Non-quota error — still try next key
                    print(f"Key {attempts+1} error: {str(e)}. Rotating...")
                    attempts += 1
                    continue
        
        raise Exception(f"All {max_attempts} API keys exhausted. Last error: {str(last_error)}")

    def get_intent(self, message):
        prompt = f"{self.system_prompt}\n\nUser Message: {message}\n\nTask: Output ONLY one word: 'SHEETS', 'CALENDAR', or 'GENERAL'."
        response_text = self._call_model(prompt)
        
        intent = response_text.strip().upper()
        intent = intent.replace("'", "").replace('"', "").replace("`", "")
        return intent if intent in ['SHEETS', 'CALENDAR', 'GENERAL'] else 'GENERAL'

    def get_response(self, message, context=""):
        prompt = f"{self.system_prompt}\n\nContext:\n{context}\n\nUser Message: {message}"
        return self._call_model(prompt)
