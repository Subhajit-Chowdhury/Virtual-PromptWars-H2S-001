import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Import our custom handlers
from assistant.gemini_handler import GeminiHandler
from assistant.sheets_handler import SheetsHandler
from assistant.calendar_handler import CalendarHandler

load_dotenv()

app = Flask(__name__)

# Initialize handlers
try:
    gemini = GeminiHandler()
    sheets = SheetsHandler()
    calendar = CalendarHandler()
except Exception as e:
    # Error logged for production diagnosis
    print(f"Server Startup Log: Handlers initialized: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Step 1: Detect Intent
        intent = gemini.get_intent(user_message)
        
        context = ""
        response_text = ""

        # Step 2: Fetch data if needed based on intent
        if intent == 'SHEETS':
            context = sheets.get_sheet_data()
            response_text = gemini.get_response(user_message, context=f"SHEET_DATA:\n{context}")
        
        elif intent == 'CALENDAR':
            # Create a simple reminder based on user message
            result = calendar.create_reminder(summary=user_message)
            response_text = f"I've updated your schedule. {result}"
        
        else: # GENERAL
            response_text = gemini.get_response(user_message)

        return jsonify({
            'assistant': response_text,
            'intent': intent.lower()
        })

    except Exception as e:
        return jsonify({
            'assistant': f"I ran into a technical glitch: {str(e)}",
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Production-ready serving (Debug=False)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
