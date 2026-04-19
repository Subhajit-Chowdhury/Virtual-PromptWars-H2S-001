# 📊 Antigravity Data Assistant
> **A Smart, Dynamic Intelligence Layer for Data Professionals.**

The **Antigravity Data Assistant** simplifies data engineering and analytics by allowing users to interact with their Google Sheets and Google Calendar using natural language. No more manual filtering or complex lookups—just ask.

---

## 🎯 Chosen Vertical
**Data & Analytics Assistant**
Chosen because it leverages the high-precision reasoning of Gemini to bridge the gap between static data (Sheets) and action-oriented scheduling (Calendar).

---

## 🏗️ Architecture & Approach
The solution uses a **Decoupled Handler Architecture**:
1. **Frontend**: Vanilla JS + CSS3 (Glassmorphism) for a premium, lightweight UI.
2. **Brain**: Google Gemini 1.5 Flash for high-speed NLU and intent classification.
3. **Connectors**: Python-based handlers for Google Sheets API (Data Retrieval) and Google Calendar API (Action Execution).
4. **Logic Router**: A Flask-based back-end that coordinates intent detection and service execution.

---

## 🔗 Google Services Integrated
| Service | Purpose |
| :--- | :--- |
| **Google Gemini API** | Intent classification, natural language querying, and summaries. |
| **Google Sheets API** | Real-time data retrieval from project-specific spreadsheets. |
| **Google Calendar API** | Automated scheduling and task reminders for data professionals. |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- Google Cloud Project with Sheets and Calendar APIs enabled.
- Gemini API Key from Google AI Studio.

### Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-link>
   cd Virtual-PromptWars-H2S-001
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env`:
   ```env
   GEMINI_API_KEY=your_key
   GOOGLE_CREDENTIALS_PATH=service_account.json
   SPREADSHEET_ID=your_id
   ```
4. Run the application:
   ```bash
   python app.py
   ```

---

## 💡 How It Works
1. **Intent Detection**: Gemini analyzes the user query to detect if it's a data query (SHEETS), a scheduling task (CALENDAR), or a general question.
2. **Context Retrieval**: If the intent is data-related, the `SheetsHandler` fetches the spreadsheet content and feeds it back to Gemini.
3. **Reasoned Response**: Gemini synthesizes the raw data into a human-readable, professional insight.
4. **Action Execution**: Scheduling tasks trigger the `CalendarHandler` to create events on the user's primary calendar.

---

## 🧪 Testing
Run unit tests with:
```bash
pytest
```
*Note: Tests include mocks for Google Services to enable validation without API quota usage.*

---

## 📌 Assumptions
- The user has shared the Target Sheet with the Service Account email.
- The spreadsheet has a sheet tab named `SalesData`.
- The `service_account.json` has appropriate role permissions (Editor/Viewer).

---
**Build for the Google Antigravity Competition 2026**
