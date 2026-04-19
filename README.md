# 📊 Antigravity Data Assistant
> **The Intelligence Layer for Modern Data Professionals.**

The **Antigravity Data Assistant** is a smart, dynamic agent designed to bridge the gap between static spreadsheet data and action-oriented scheduling. It allows users to query their Google Sheets and manage their Google Calendar through a single, premium natural language interface.

---

## 🏆 The STAR Approach (Problem & Solution)

### **S — Situation**
Data professionals (Analysts, Engineers, Managers) often suffer from "context-switching fatigue." They have to manually open Google Sheets to find data, write SQL or complex filters to summarize it, and then jump to Google Calendar to schedule follow-ups or reminders. This fragmentation leads to lost time and potential errors.

### **T — Task**
The goal was to build an integrated, AI-first solution that consolidates these workflows into a single interface. The assistant needed to be:
1. **Intelligent**: Understand natural language accurately.
2. **Dynamic**: Fetch live data from Google Sheets in real-time.
3. **Action-Oriented**: Execute scheduling tasks in Google Calendar automatically.
4. **Resilient**: Fully secure, under 1MB, and responsive across all devices.

### **A — Action**
I developed a high-performance **Python/Flask** application integrated with the **Google Gemini 1.5 Flash** model for NLP reasoning.
- **Live Data Pipeline**: Built a `SheetsHandler` to dynamically fetch and clean spreadsheet data.
- **Automated Execution**: Built a `CalendarHandler` to translate user requirements into Calendar events.
- **Premium UI/UX**: Crafted a **Glassmorphic Chat UI** using modern CSS3 (Plus Jakarta Sans) with full **responsive design** for Desktop, Table, and Mobile.
- **Security First**: Implemented environment-based secret management and service account authentication.

### **R — Result**
The final result is a **Top-Tier Data Partner** that:
- **Reduces Context Switching**: Analyzes data and schedules events in one chat window.
- **Zero-Barrier Analytics**: Allows non-technical stakeholders to query complex sheets in plain English.
- **High Efficiency**: The entire repository is **~3.5 KiB**, ensuring lightning-fast performance and total compliance with competition lightweight rules.

---

## 🎯 Chosen Vertical
**Data & Analytics Assistant**
This vertical was chosen to leverage the high-precision reasoning capabilities of Gemini, solving the real-world problem of data accessibility.

---

## 🔗 integrated Google Services
| Service | Purpose |
| :--- | :--- |
| **Google Gemini API** | Intent classification, data reasoning, and NL summary. |
| **Google Sheets API** | Real-time data retrieval from spreadsheets. |
| **Google Calendar API** | Automated scheduling and reminder management. |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
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

## 💡 How It Works (The Logic)
1. **Intent Detection**: Gemini analyzes the user query to detect if it's a data query (`SHEETS`), a scheduling task (`CALENDAR`), or a `GENERAL` question.
2. **Contextual Retrieval**: If the intent is data-related, the `SheetsHandler` dynamically detects the first sheet tab and fetches the content.
3. **Reasoned Response**: Gemini synthesizes the raw data into a friendly, professional insight.
4. **Action Execution**: Scheduling tasks trigger the `CalendarHandler` to create events on the user's primary calendar using the Service Account.

---

## 🧪 Testing & Validation
- **Unit Tests**: Run `pytest` to verify modular logic.
- **Responsiveness**: Tested across Desktop (1920x1080), Tablet (iPad Air), and Mobile (iPhone 14) resolutions.
- **Repo Measurement**: Measured at **~3.5 KiB** using `git count-objects`.

---

## 📌 Assumptions & Security
- The Target Sheet must be shared with the Service Account email.
- The `service_account.json` is gitignored for security (must be provided locally).
- The assistant assumes the most relevant data is on the first sheet tab.

---
**Build for the Google Antigravity Competition 2026**
