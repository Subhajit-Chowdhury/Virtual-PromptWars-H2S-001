import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load .env (Local development)
load_dotenv()

# Import our custom handlers
from assistant.gemini_handler import GeminiHandler
from assistant.sheets_handler import SheetsHandler
from assistant.calendar_handler import CalendarHandler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Check if we have credentials (Production check)
    if not os.getenv('GEMINI_API_KEY'):
        return jsonify({'assistant': '⚠️ Vercel Setup Needed: Please add your GEMINI_API_KEY to Environment Variables.'}), 200
        
    try:
        gemini = GeminiHandler()
        sheets = SheetsHandler()
        calendar = CalendarHandler()
        
        # Step 1: Detect Intent
        intent = gemini.get_intent(user_message)
        
        response_text = ""

        # Step 2: Fetch data or execute action
        if intent == 'SHEETS':
            spreadsheet_id = os.getenv('SPREADSHEET_ID')
            data, audit_report = sheets.get_sheet_data(spreadsheet_id)
            
            # Pass BOTH data and audit logic to AI
            context = f"AUDIT_REPORT: {json.dumps(audit_report)}\nSHEET_DATA:\n{data}"
            response_text = gemini.get_response(user_message, context=context)
        
        elif intent == 'CALENDAR':
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
            'assistant': f"⚠️ Deployment Check: I can't connect to Google Services. Did you add GOOGLE_SERVICE_ACCOUNT_JSON and SPREADSHEET_ID to Vercel? (Error: {str(e)})",
            'error': str(e)
        }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
