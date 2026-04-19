# 📊 DataPulse Assistant

> **Your data shouldn't just sit in a spreadsheet. It should talk to you.**

🔗 **Live Demo**: [virtual-prompt-wars-h2s-001.vercel.app](https://virtual-prompt-wars-h2s-001.vercel.app)
📁 **GitHub**: [github.com/SubhajitSK/Virtual-PromptWars-H2S-001](https://github.com/SubhajitSK/Virtual-PromptWars-H2S-001)
👤 **Built by**: Subhajit | AWS Data Engineer

---

## 🤔 The Problem

Every analyst knows this pain:

You open Google Sheets. You scroll. You filter. You squint at numbers — and by the time you've figured out what's going on, you've already forgotten why you opened the tab in the first place. Then you switch to Google Calendar to schedule a follow-up, and by then you've lost context completely.

This constant **"context-switching"** is where valuable insights go to die. The gap between *finding* something important in your data and *acting* on it is where business opportunities get missed every single day.

---

## 💡 What DataPulse Does About It

DataPulse is a conversational AI assistant that plugs directly into your Google Sheets and Google Calendar. Instead of switching tools and losing context, you just **ask a question in plain English** and get a clear, accurate answer back — instantly.

It bridges the gap between **data insight** and **real action**, in one chat window.

Here's what that looks like in practice:

| What you type | What DataPulse does |
| :--- | :--- |
| *"What is our top-selling region?"* | Reads your live sheet, runs a quality check, and gives you a clear answer with numbers. |
| *"Show me a breakdown of Q1 revenue"* | Generates a clean, sorted table directly in the chat. |
| *"Remind me to review sales data on Friday"* | Creates a real Google Calendar event and sends you the link. |
| *"Whch prodct had the hihgest margins?"* (typos and all) | Understands what you meant and answers correctly — no judgment. |
| *(Upload a CSV or Excel file)* | Instantly analyzes your custom dataset the same way it does with Google Sheets. |

---

## 🏗️ How It Was Built

The architecture is deliberately modular. Every component can be swapped or scaled without touching the rest.

```
You (Chat Interface)
        ↓
  Flask Backend
        ↓
  Gemini AI Brain → Classifies your message (Data? Calendar? General?)
        ↓
  ┌──────────────────┐    ┌────────────────────┐
  │  Sheets Handler  │    │  Calendar Handler  │
  │  • Reads sheet   │    │  • Creates events  │
  │  • Audits data   │    │  • Returns links   │
  └──────────────────┘    └────────────────────┘
```

**Tech Stack:**
- **Backend**: Python + Flask
- **AI**: Google Gemini 1.5 Flash (with Multi-Agent key rotation for resilience)
- **Data**: Google Sheets API (live reads) + Local file uploads (CSV, XLSX, JSON)
- **Actions**: Google Calendar API (real events, not simulations)
- **Frontend**: Vanilla HTML/CSS/JS — dark-themed, fully responsive

---

## 🔍 What's Happening Under the Hood

These are the non-obvious engineering decisions that make DataPulse more than just "a chatbot that reads a spreadsheet."

### Intent Router
Every message is classified *before* it's answered. Gemini first determines: is this a **data question**, a **calendar request**, or a **general question**? This keeps responses accurate and prevents the AI from guessing.

### Data Integrity Auditor
Before the AI ever sees your data, a validation pass runs automatically. It checks for:
- **Empty cells** — so the AI isn't reasoning on incomplete rows
- **Duplicate entries** — so numbers aren't inflated

The AI then receives a quality report *alongside* the data. This means it can proactively flag issues: *"I found 2 duplicate rows in your dataset — your totals may be slightly off."* This is what makes DataPulse trustworthy, not just fast.

### Universal File Analyzer
Users can upload their own `.csv`, `.xlsx`, or `.json` files directly in the chat. The assistant seamlessly switches to analyzing that file — and runs the same audit on it. One click on **Reset** switches it back to the live Google Sheet.

### Multi-Agent API Pool
Instead of relying on a single API key (which can hit rate limits), DataPulse supports a **pool of Gemini API keys** via `GEMINI_API_KEYS`. It rotates through them using a round-robin strategy, and automatically fails over to the next key if one is exhausted. The user never sees an error.

### Cloud-Safe Credential Handling
We support two modes, detected automatically:
- **Local**: Use a `service_account.json` file path via `GOOGLE_CREDENTIALS_PATH`
- **Cloud (Vercel)**: Paste a Base64-encoded version of the JSON in `GOOGLE_SERVICE_ACCOUNT_JSON`

No flags. No config files to change. It just works in both environments.

---

## 🚀 Getting Started Locally

**What you need before you begin:**
- Python 3.10+
- A Google Cloud project with **Sheets API** and **Calendar API** enabled
- A **Gemini API key** from [Google AI Studio](https://aistudio.google.com/)
- A **Service Account** JSON with read access to your Google Sheet

**Steps:**

```bash
# Step 1: Clone the repository
git clone https://github.com/SubhajitSK/Virtual-PromptWars-H2S-001.git
cd Virtual-PromptWars-H2S-001

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Set up your environment variables
# Create a file named .env in the root folder and paste this:
GEMINI_API_KEY=your_gemini_key_here
SPREADSHEET_ID=your_google_sheet_id_here
GOOGLE_CREDENTIALS_PATH=service_account.json

# Step 4: Run the app
python app.py
```

Open your browser and go to `http://localhost:5000`. Start asking questions.

---

## ☁️ Deploying to Vercel

1. Push your code to GitHub.
2. Go to [Vercel](https://vercel.com) and import your repository.
3. In **Settings → Environment Variables**, add the following:

   | Variable Name | What to put there |
   | :--- | :--- |
   | `GEMINI_API_KEY` | Your Gemini API key |
   | `SPREADSHEET_ID` | The ID from your Google Sheet URL |
   | `GOOGLE_SERVICE_ACCOUNT_JSON` | Your service account JSON as a Base64 string |

4. Click **Deploy**.

> **Getting the Base64 string (Windows PowerShell):**
> ```powershell
> [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content service_account.json -Raw)))
> ```
> Copy the output and paste it as the value for `GOOGLE_SERVICE_ACCOUNT_JSON`.

---

## 🌐 Google Services Used

| Service | What it does in DataPulse |
| :--- | :--- |
| **Google Gemini API** | Powers the AI brain — understands questions, classifies intent, generates answers |
| **Google Sheets API** | Fetches live data from your spreadsheet for every query |
| **Google Calendar API** | Creates real calendar reminders from natural language commands |

---

## 📋 About the Project

This project was built for the **Virtual: PromptWars** competition — a challenge to build a useful, production-grade AI assistant powered by Google services.

The goal was simple: build something that a real operations or analytics team could use on Monday morning, not just a demo that works in ideal conditions.

**The core belief behind DataPulse**: AI becomes genuinely useful when it bridges the gap between *insight* and *action*. Seeing data is not enough. Acting on it — immediately, correctly, and without losing context — is what counts.

---

*Built with ☕ by [Subhajit](https://github.com/SubhajitSK) · AWS Data Engineer*
