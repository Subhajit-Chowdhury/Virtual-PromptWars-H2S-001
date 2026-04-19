import os
import json
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load .env (Local development)
load_dotenv()

# Import our custom handlers
from assistant.gemini_handler import GeminiHandler
from assistant.sheets_handler import SheetsHandler
from assistant.calendar_handler import CalendarHandler

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'datapulse_secret_key_123')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"active_data.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Clean up any previous uploads
        for f in os.listdir(UPLOAD_FOLDER):
            os.remove(os.path.join(UPLOAD_FOLDER, f))
            
        file.save(file_path)
        
        # Pre-scan for audit report
        sheets = SheetsHandler()
        _, audit_report = sheets.get_local_data(file_path)
        
        report_summary = ""
        if audit_report:
           report_summary = f"Audit Pass: Checked {audit_report['rows_checked']} rows. {audit_report['duplicates_found']} duplicates found."
        
        session['active_mode'] = 'upload'
        session['active_file'] = filename
        
        return jsonify({'success': True, 'report_summary': report_summary})
    
    return jsonify({'success': False, 'error': 'Unsupported file type'}), 400

@app.route('/reset-data', methods=['POST'])
def reset_data():
    session['active_mode'] = 'sheets'
    # Clean up uploads
    for f in os.listdir(UPLOAD_FOLDER):
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, f))
        except:
            pass
    return jsonify({'success': True})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    if not os.getenv('GEMINI_API_KEY'):
        return jsonify({'assistant': '⚠️ Vercel Setup Needed: Please add your GEMINI_API_KEY to Environment Variables.'}), 200
        
    try:
        gemini = GeminiHandler()
        sheets = SheetsHandler()
        calendar = CalendarHandler()
        
        intent = gemini.get_intent(user_message)
        response_text = ""

        if intent == 'SHEETS':
            # Priority: Check if an uploaded file exists
            if session.get('active_mode') == 'upload':
                filename = session.get('active_file')
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(file_path):
                    data, audit_report = sheets.get_local_data(file_path)
                    context = f"AUDIT_REPORT: {json.dumps(audit_report)}\nUPLOADED_FILE_DATA:\n{data}"
                    response_text = gemini.get_response(user_message, context=context)
                else:
                    session['active_mode'] = 'sheets' # Fallback
            
            # Default: Use Google Sheets
            if not response_text:
                spreadsheet_id = os.getenv('SPREADSHEET_ID')
                data, audit_report = sheets.get_sheet_data(spreadsheet_id)
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
            'assistant': f"⚠️ Deployment Check: I can't connect to Google Services. (Error: {str(e)})",
            'error': str(e)
        }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
