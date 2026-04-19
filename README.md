# 📊 DataPulse Assistant

> **Data shouldn't stop at analysis. It should help drive the next step.**

🌐 **Live Demo**: [virtual-prompt-wars-h2s-001.vercel.app](https://virtual-prompt-wars-h2s-001.vercel.app) · [Mirror](https://antigravity-data-assistant-i3z33o2a3.vercel.app/)  
🧑‍💻 **Built by**: [Subhajit Chowdhury](https://github.com/Subhajit-Chowdhury) · AWS Data Engineer  
🤝 **Connect**: [LinkedIn](https://linkedin.com/in/subhajit00100/) · [GitHub](https://github.com/Subhajit-Chowdhury) · [Medium](https://subhajitchowdhury.medium.com/)

---

## 🧩 Context

In many day-to-day workflows, data exploration and follow-up actions happen in different places.

Data is reviewed in spreadsheets or files. Decisions and next steps are handled separately — in meetings, chats, or calendars.

This separation introduces friction:

- Context can become fragmented between tools
- Small but important observations may not lead to immediate action
- Follow-ups depend on manual coordination

This project explores whether that gap can be reduced within a single workflow.

---

## 🎯 Objective

Design a system that can:

- Read and analyze live data
- Respond to questions in natural language
- Enable immediate follow-up actions
- Maintain data reliability through validation

**Constraint:** All of the above should happen within a single interaction flow, without requiring users to switch between multiple tools.

---

## ⚙️ Approach

DataPulse is a conversational assistant that connects data access with action handling.

### System Flow

1. A query is submitted through the chat interface
2. Gemini classifies the intent (data, calendar, or general)
3. The appropriate handler processes the request
4. A structured response is returned

```
User Input
   ↓
Flask Backend
   ↓
Gemini (Intent Classification)
   ↓
 ┌───────────────┐   ┌────────────────┐
 │ Sheets Handler│   │Calendar Handler│
 │ - Data fetch  │   │ - Event create │
 │ - Validation  │   │ - Link output  │
 └───────────────┘   └────────────────┘
```

---

## 🛠️ Key Design Decisions

### 🧠 Intent-Based Routing

Each query is classified before execution:

- Data queries → Sheets handler
- Scheduling requests → Calendar handler
- General queries → handled separately

This keeps system behavior predictable and reduces ambiguity.

---

### 🛡️ Data Validation Before Response

Before any analysis:

- Missing values are identified
- Duplicate rows are detected

The validation result is included in responses to improve transparency.

---

### 📎 Support for Real Data Inputs

- Works with live Google Sheets
- Accepts CSV, Excel, and JSON uploads (up to 2MB)
- Uses a consistent validation and analysis pipeline

---

### 🔁 API Key Rotation (Reliability)

- Supports multiple Gemini API keys
- Uses round-robin rotation
- Automatically switches when limits are reached

---

### 📅 Integrated Action Handling

- Calendar events can be created directly from user input
- A usable event link is returned in the response

---

### 🔐 Secure Credential Handling

Two modes are supported:

- **Local**: Service account via file path
- **Cloud**: Base64-encoded credentials via environment variables

Credentials are managed through environment variables and are not hardcoded.

---

## 🧱 Tech Stack

- Python (Flask)
- Google Gemini 2.0 Flash
- Google Sheets API
- Google Calendar API
- Vercel (deployment)

---

## 🧪 Testing & Validation

22 automated tests covering:

- Input sanitization
- File validation
- Flask routes (chat, upload, reset, health)
- Module imports

Tests run without requiring external API credentials.

```bash
python -m pytest tests/test_handlers.py -v
```

---

## ⚖️ Evaluation Alignment

### ✔ Code Quality

- Modular handler-based architecture
- Clear separation of responsibilities

### ✔ Security

- Environment-based credential management
- Input validation and sanitization

### ✔ Efficiency

- Intent routing avoids unnecessary processing
- API key rotation maintains availability

### ✔ Testing

- 22 automated tests covering core functionality

### ✔ Accessibility & Usability

- Single chat interface
- Natural language interaction
- No need for query syntax

### ✔ Google Services Integration

- Gemini → intent classification and responses
- Sheets API → live data access
- Calendar API → event creation

---

## 📂 Project Structure

```
Virtual-PromptWars-H2S-001/
├── app.py
├── assistant/
│   ├── gemini_handler.py
│   ├── sheets_handler.py
│   └── calendar_handler.py
├── static/
│   ├── css/style.css
│   └── js/chat.js
├── templates/
│   └── index.html
├── tests/
│   └── test_handlers.py
├── vercel.json
├── requirements.txt
└── README.md
```

---

## 📌 Assumptions

- Google Sheet contains headers in the first row
- Service account has access to the target spreadsheet
- Uploaded files are valid CSV, XLSX, or JSON
- Gemini API is enabled in the Google Cloud project

---

## 🚀 Getting Started

```bash
git clone https://github.com/Subhajit-Chowdhury/Virtual-PromptWars-H2S-001.git
cd Virtual-PromptWars-H2S-001
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.

### Environment Variables

```
GEMINI_API_KEY=your_gemini_key
SPREADSHEET_ID=your_google_sheet_id
GOOGLE_CREDENTIALS_PATH=service_account.json
```

---

## 🚀 Outcome

This project demonstrates a practical approach to reducing the gap between data exploration and follow-up actions within a single interface.

From testing:

- Data can be queried and validated in one step
- Follow-up actions can be triggered immediately
- Context is preserved within a single interaction

The system is designed as an exploration of integrating insight and action, not as a replacement for full analytics platforms.

---

## 🧠 Notes

- No assumptions are made about data quality
- All responses are based on actual data reads
- Behavior is deterministic outside of AI interpretation

---

*Built for [Virtual: PromptWars](https://hack2skill.com) by Hack2Skill*  
*© 2026 [Subhajit Chowdhury](https://github.com/Subhajit-Chowdhury)*
