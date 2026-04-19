# 📊 DataPulse Assistant

**Your data shouldn't just sit in a spreadsheet. It should talk to you.**

DataPulse is an AI-powered assistant that reads your Google Sheets, answers your questions in plain English, and even schedules follow-up reminders on your Google Calendar — all from a single chat interface.

No more switching tabs. No more building pivot tables. Just ask.

---

## 🤔 The Problem We're Solving

If you've ever worked with business data, you know the drill:

1. Open Google Sheets. Scroll. Filter. Squint at numbers.
2. Try to figure out what's actually going on.
3. Switch to Calendar to schedule a follow-up meeting.
4. Forget what you just found because you lost context.

This cycle — **"Insight Decay"** — is incredibly common. The gap between *finding* something important in your data and *acting* on it is where opportunities get lost.

We built DataPulse to close that gap.

---

## ✅ What DataPulse Actually Does

| Feature | What it means for you |
| :--- | :--- |
| **Ask questions in plain English** | Type "What's our top region?" instead of writing formulas. |
| **Live data, always** | Every answer comes from your actual Google Sheet — not a cached copy. |
| **Data quality checks** | Before answering, it scans for nulls, duplicates, and format issues automatically. |
| **Schedule follow-ups** | Say "Remind me to review Q1 sales" and it creates a real Google Calendar event. |
| **Typo-tolerant** | Misspell your question? No problem. It understands what you meant. |

---

## 🛠️ How We Built It

We kept the architecture simple and modular on purpose — every piece can be swapped or scaled independently.

```
User (Chat UI)
    ↓
Flask Backend (app.py)
    ↓
Gemini AI → Classifies intent (Is this a data question? A calendar request? General chat?)
    ↓
┌─────────────────┐    ┌──────────────────┐
│  Sheets Handler  │    │ Calendar Handler  │
│  (Live data +    │    │ (Creates real     │
│   quality check) │    │  calendar events) │
└─────────────────┘    └──────────────────┘
```

**Tech stack:**
- **Backend**: Python + Flask
- **AI Brain**: Google Gemini 1.5 Flash
- **Data Source**: Google Sheets API (live reads)
- **Action Layer**: Google Calendar API (real event creation)
- **Frontend**: Vanilla HTML/CSS/JS with a responsive "Modern Classic" dark theme

---

## 🔍 Under the Hood (Developer Notes)

Here's what's happening behind the scenes that you *won't* see in the UI — but matters a lot.

### Intent Classification
When a user sends a message, Gemini doesn't just "chat." It first classifies the message into one of three buckets: `SHEETS`, `CALENDAR`, or `GENERAL`. This determines which handler processes the request. It's a simple routing trick, but it keeps the logic clean and predictable.

### Data Integrity Layer
Before the AI ever sees your spreadsheet data, the `SheetsHandler` runs a validation pass. It checks for:
- **Null/empty cells** that could skew analysis
- **Duplicate rows** that could inflate numbers

The AI receives a quality report *alongside* the raw data. This means it can warn you: "Hey, I found 3 duplicate rows — you might want to clean those up before making decisions."

### Credential Handling (Cloud-Ready)
We support two modes:
- **Local development**: Point to a `service_account.json` file via `GOOGLE_CREDENTIALS_PATH`
- **Cloud deployment (Vercel)**: Paste the JSON as a Base64-encoded string in `GOOGLE_SERVICE_ACCOUNT_JSON`

The handler auto-detects which format you're using. No config flags needed.

### Dynamic Sheet Detection
We never hardcode the sheet tab name. The handler queries the spreadsheet metadata and reads from the first available tab. Rename your tabs anytime — nothing breaks.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- A Google Cloud project with **Sheets API** and **Calendar API** enabled
- A **Gemini API key** from [Google AI Studio](https://aistudio.google.com/)
- A **Service Account** with access to your Google Sheet

### Quick Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/Virtual-PromptWars-H2S-001.git
cd Virtual-PromptWars-H2S-001

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your .env file
GEMINI_API_KEY=your_gemini_key_here
SPREADSHEET_ID=your_sheet_id_here
GOOGLE_CREDENTIALS_PATH=service_account.json

# 4. Run it
python app.py
```

Open `http://localhost:5000` and start asking questions.

---

## 🌐 Deploying to Vercel

1. Push your repo to GitHub.
2. Import the project into [Vercel](https://vercel.com).
3. Add these **Environment Variables** in Vercel Settings:
   - `GEMINI_API_KEY` → Your Gemini key
   - `SPREADSHEET_ID` → Your Google Sheet ID
   - `GOOGLE_SERVICE_ACCOUNT_JSON` → Base64-encoded service account JSON
4. Deploy. That's it.

> **Tip**: To get the Base64 string, run this in PowerShell:
> ```powershell
> [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content service_account.json -Raw)))
> ```

---

## 🎯 Why This Matters

Most AI demos show you a chatbot that *talks* about data.

DataPulse is different because it **acts** on data:
- It reads live spreadsheets (not pre-loaded samples).
- It validates data quality before reasoning (so it doesn't make things up).
- It creates real calendar events (so insights don't get forgotten).

**The goal isn't just intelligence — it's accountability.**

---

## 📋 Google Services Used

| Service | Role |
| :--- | :--- |
| Google Gemini API | Natural language understanding and reasoning |
| Google Sheets API | Live data retrieval and validation |
| Google Calendar API | Automated scheduling and reminder creation |

---

*Built for the Virtual: PromptWars*
