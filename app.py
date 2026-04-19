import os
import json
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load .env (Local development only)
load_dotenv()

# Import our custom handlers
from assistant.gemini_handler import GeminiHandler
from assistant.sheets_handler import SheetsHandler
from assistant.calendar_handler import CalendarHandler

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'datapulse_secret_key_2026')

# Vercel uses /tmp as the only writable directory
UPLOAD_FOLDER = os.path.join('/tmp', 'datapulse_uploads')
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json'}

# Module-level state to track active file (sessions don't persist on Vercel serverless)
_active_file = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_dir():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/upload-file', methods=['POST'])
def upload_file():
    global _active_file
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if not file or not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Unsupported file type. Only .csv, .xlsx, and .json are allowed.'}), 400

    try:
        ensure_upload_dir()
        
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"active_data.{ext}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Clean up previous uploads
        if os.path.exists(UPLOAD_FOLDER):
            for f in os.listdir(UPLOAD_FOLDER):
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, f))
                except Exception:
                    pass
            
        file.save(file_path)
        
        # Pre-scan for audit report
        sheets = SheetsHandler()
        _, audit_report = sheets.get_local_data(file_path)
        
        _active_file = file_path
        
        report_summary = ""
        if audit_report:
            report_summary = f"📊 Audit Pass: Checked {audit_report['rows_checked']} rows. {audit_report['duplicates_found']} duplicates found."
        
        return jsonify({'success': True, 'report_summary': report_summary})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/reset-data', methods=['POST'])
def reset_data():
    global _active_file
    _active_file = None
    
    if os.path.exists(UPLOAD_FOLDER):
        for f in os.listdir(UPLOAD_FOLDER):
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, f))
            except Exception:
                pass
    return jsonify({'success': True})

@app.route('/chat', methods=['POST'])
def chat():
    global _active_file
    
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    if not os.getenv('GEMINI_API_KEY') and not os.getenv('GEMINI_API_KEYS'):
        return jsonify({'assistant': '⚠️ Setup Needed: Please add GEMINI_API_KEY to your Environment Variables.'}), 200
        
    try:
        gemini = GeminiHandler()
        intent = gemini.get_intent(user_message)
        response_text = ""

        if intent == 'SHEETS':
            sheets = SheetsHandler()
            
            # Priority: Use uploaded file if it exists
            if _active_file and os.path.exists(_active_file):
                data, audit_report = sheets.get_local_data(_active_file)
                context = f"AUDIT_REPORT: {json.dumps(audit_report)}\nUPLOADED_FILE_DATA:\n{data}"
                response_text = gemini.get_response(user_message, context=context)
            else:
                # Default: Use Google Sheets
                spreadsheet_id = os.getenv('SPREADSHEET_ID')
                if spreadsheet_id:
                    data, audit_report = sheets.get_sheet_data(spreadsheet_id)
                    context = f"AUDIT_REPORT: {json.dumps(audit_report)}\nSHEET_DATA:\n{data}"
                    response_text = gemini.get_response(user_message, context=context)
                else:
                    response_text = "⚠️ No data source configured. Please upload a file or set SPREADSHEET_ID."
        
        elif intent == 'CALENDAR':
            calendar = CalendarHandler()
            result = calendar.create_reminder(summary=user_message)
            response_text = gemini.get_response(
                user_message, 
                context=f"Calendar result: {result}. Format this nicely for the user."
            )
        
        else:
            response_text = gemini.get_response(user_message)

        return jsonify({
            'assistant': response_text,
            'intent': intent.lower()
        })

    except Exception as e:
        return jsonify({
            'assistant': f"⚠️ Something went wrong: {str(e)}",
            'error': str(e)
        }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
