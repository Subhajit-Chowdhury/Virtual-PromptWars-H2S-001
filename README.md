# 📊 DataPulse Assistant

> **Your data shouldn't just sit in a spreadsheet. It should talk to you.**

🌐 **Live Demo**: [virtual-prompt-wars-h2s-001.vercel.app](https://virtual-prompt-wars-h2s-001.vercel.app) · [Mirror](https://antigravity-data-assistant-i3z33o2a3.vercel.app/)  
🧑‍💻 **Built by**: [Subhajit Chowdhury](https://github.com/Subhajit-Chowdhury) · AWS Data Engineer  
🤝 **Connect**: [LinkedIn](https://linkedin.com/in/subhajit00100/) · [GitHub](https://github.com/Subhajit-Chowdhury) · [Medium](https://subhajitchowdhury.medium.com/)

---

## 🎯 Chosen Vertical

**Data & Productivity Assistant** — built for analysts, operations teams, and business users who work with spreadsheets daily.

---

## 🤔 The Problem

Every analyst knows this pain:

You open Google Sheets. You scroll through rows. You filter columns. You squint at numbers — and by the time you figure out what matters, you've already forgotten why you opened the tab.

Then you switch to Google Calendar to schedule a follow-up. By then, you've lost context completely.

This cycle — **context-switching between insight and action** — is where valuable business decisions get delayed or missed entirely.

DataPulse was built to close that gap.

---

## 💡 What DataPulse Does

DataPulse is a conversational AI assistant that connects directly to your Google Sheets and Google Calendar. Instead of switching between tabs and tools, you ask a question in plain English and get a clear, accurate answer — instantly.

Here's what that looks like in practice:

| What you type | What happens |
| :--- | :--- |
| *"What is our top-selling region?"* | Reads your live sheet, runs a quality audit, and gives you a clear answer with numbers. |
| *"Show me a breakdown of Q1 revenue"* | Generates a clean, formatted table directly in the chat. |
| *"Remind me to review sales data on Friday"* | Creates a real Google Calendar event and shares the link. |
| *"Whch prodct had the hihgest margins?"* | Understands what you meant despite the typos — and answers correctly. |
| 📎 *Upload a CSV or Excel file* | Instantly analyzes your custom dataset with the same audit pipeline. |

---

## 🏗️ Architecture & Approach

The system is modular by design. Each component handles one responsibility and can be swapped or scaled independently.

```
User (Chat Interface)
        ↓
  Flask Backend (app.py)
        ↓
  Gemini AI → Classifies intent: Data? Calendar? General?
        ↓
  ┌───────────────────┐    ┌─────────────────────┐
  │  Sheets Handler   │    │  Calendar Handler   │
  │  • Live data read │    │  • Real event       │
  │  • Quality audit  │    │    creation          │
  │  • File uploads   │    │  • Clean link output │
  └───────────────────┘    └─────────────────────┘
```

**How it works, step by step:**

1. **You type a question** in the chat window.
2. **Gemini classifies your intent** — is this about data, scheduling, or a general question?
3. **The right handler activates.** For data questions, the Sheets Handler fetches your spreadsheet and runs a quality audit. For scheduling, the Calendar Handler creates a real event.
4. **The AI responds** with a clear, structured answer — including the audit results, so you know the data is trustworthy.

---

## 🔍 What's Happening Under the Hood

### 🧠 Intent Classification
Every message passes through an intent router before being answered. Gemini determines whether the message is a **data query**, a **calendar request**, or a **general question**. This prevents the AI from guessing and keeps responses focused.

### 🛡️ Data Integrity Auditor
Before the AI reasons on any data, a validation pass runs automatically:
- Scans for **empty cells** that could skew analysis
- Detects **duplicate rows** that could inflate totals

The AI receives the quality report alongside the raw data and reports it transparently: *"Checked 48 rows. 0 duplicates found. Data is clean."* This is visible to the user in every response.

### 📎 Universal File Analyzer
Users can upload `.csv`, `.xlsx`, or `.json` files directly in the chat. The assistant switches seamlessly to analyzing the uploaded data — using the same audit pipeline. A **Reset** button in the header returns to the live Google Sheet.

### 🔁 Multi-Agent API Pool
DataPulse supports a pool of Gemini API keys via the `GEMINI_API_KEYS` environment variable. Keys are rotated using a round-robin strategy. If one key hits its quota, the system automatically fails over to the next — invisible to the user.

### 🔐 Cloud-Safe Credential Handling
Two credential modes are supported, detected automatically at startup:
- **Local development**: Point to a `service_account.json` file via `GOOGLE_CREDENTIALS_PATH`
- **Cloud (Vercel)**: Provide a Base64-encoded string via `GOOGLE_SERVICE_ACCOUNT_JSON`

No manual flags or config switches needed.

---

## 🌐 Google Services Used

| Service | Purpose in DataPulse |
| :--- | :--- |
| **Google Gemini API** | Core AI — understands questions, classifies intent, generates structured answers |
| **Google Sheets API** | Fetches live spreadsheet data for every query; enables real-time analysis |
| **Google Calendar API** | Creates real calendar events from natural language commands |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- A Google Cloud project with **Sheets API** and **Calendar API** enabled
- A **Gemini API key** from [Google AI Studio](https://aistudio.google.com/)
- A **Service Account** JSON file with read access to your Google Sheet

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/Subhajit-Chowdhury/Virtual-PromptWars-H2S-001.git
cd Virtual-PromptWars-H2S-001

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file in the root directory
GEMINI_API_KEY=your_gemini_key_here
SPREADSHEET_ID=your_google_sheet_id_here
GOOGLE_CREDENTIALS_PATH=service_account.json

# 4. Run the application
python app.py
```

Open `http://localhost:5000` in your browser. Start asking questions.

### Deploying to Vercel

1. Push your code to GitHub.
2. Import the repository into [Vercel](https://vercel.com).
3. Add the following **Environment Variables** in Vercel Settings:

   | Variable | Value |
   | :--- | :--- |
   | `GEMINI_API_KEY` | Your Gemini API key |
   | `SPREADSHEET_ID` | Your Google Sheet ID (from the URL) |
   | `GOOGLE_SERVICE_ACCOUNT_JSON` | Base64-encoded service account JSON |

4. Deploy.

> **To get the Base64 string (PowerShell):**
> ```powershell
> [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content service_account.json -Raw)))
> ```

---

## 📌 Assumptions

- The Google Sheet has headers in the first row and data starting from the second row.
- The service account has been shared with the target spreadsheet (Editor or Viewer access).
- The Gemini API key is from a project with the Generative AI API enabled.
- Uploaded files are well-formed CSV, XLSX, or JSON. Corrupted files will return a graceful error message.

---

## 🧪 Testing

**Automated tests** — run the full suite with:

```bash
python -m pytest tests/test_handlers.py -v
```

The test suite covers **22 tests** across 4 categories:

| Category | Tests | What it validates |
| :--- | :--- | :--- |
| Input Sanitization | 5 | HTML stripping, length limits, null byte removal |
| File Validation | 8 | Allowed/rejected extensions, edge cases |
| Flask Routes | 6 | Homepage, health check, chat, upload, reset |
| Handler Imports | 3 | All modules load without credential errors |

All tests pass without API credentials, making them safe to run in any environment.

**Manual testing:**

1. **Live**: Visit the [deployed app](https://virtual-prompt-wars-h2s-001.vercel.app) and type a data question.
2. **File upload**: Click the 📎 icon, upload any CSV or Excel file, and ask questions about it.
3. **Local**: Run `python app.py` and open `http://localhost:5000`.

---

## 📋 Project Structure

```
Virtual-PromptWars-H2S-001/
├── app.py                      # Flask server + route logic
├── assistant/
│   ├── __init__.py
│   ├── gemini_handler.py       # AI brain with multi-key rotation
│   ├── sheets_handler.py       # Google Sheets + file parser + auditor
│   └── calendar_handler.py     # Google Calendar event creation
├── static/
│   ├── css/style.css           # Dark-themed responsive UI
│   └── js/chat.js              # Frontend chat logic + file upload
├── templates/
│   └── index.html              # Single-page chat interface
├── vercel.json                 # Vercel deployment config
├── requirements.txt            # Python dependencies
├── .gitignore                  # Protects secrets and build artifacts
└── README.md
```

---

## 🎯 Why This Matters

Most AI demos show a chatbot that talks about data.

DataPulse is different because it **acts** on data:
- It reads **live** spreadsheets — not pre-loaded samples.
- It **audits data quality** before reasoning — so it does not make assumptions on bad data.
- It creates **real** calendar events — so insights lead to action, not just conversation.

The goal is not just intelligence. It is **accountability**.

---

*Built for the [Virtual: PromptWars](https://hack2skill.com) competition by [Hack2Skill](https://hack2skill.com).*  
*© 2026 [Subhajit Chowdhury](https://github.com/Subhajit-Chowdhury) · AWS Data Engineer*
