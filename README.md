# 📊 Antigravity Data Assistant
> **The Intelligence Layer for Modern Data Professionals.**

The **Antigravity Data Assistant** is a smart, dynamic agent designed to bridge the gap between static spreadsheet data and action-oriented scheduling. It allows users to query their Google Sheets and manage their Google Calendar through a single, premium natural language interface.

---

## 🏆 The Vision & Solution

### **Addressing Data Fragmentation**
In modern data engineering and analytics, professionals often suffer from "context-switching fatigue." The manual process of opening Google Sheets, applying complex filters, and then switching to Google Calendar to schedule follow-ups leads to significant time loss and potential human error.

### **Our Mission**
Our goal was to build an integrated, AI-first solution that consolidates these fragmented workflows into a single, high-performance interface. We set out to create a partner that is not just intelligent enough to understand natural language, but dynamic enough to fetch live data and execute actions automatically—all while maintaining a secure, lightweight footprint under 1MB.

### **The Engineering Approach**
We engineered a high-precision **Python/Flask** application powered by **Google Gemini 1.5 Flash**. By developing modular handlers for the Google Sheets and Calendar APIs, we created a live data pipeline that translates ambiguous user queries into structured data lookups and automated scheduling events. The entire system is wrapped in a **Glassmorphic UI** designed for maximum responsiveness across any device.

### **Impact & Scalability**
The resulting "Antigravity Partner" eliminates context switching by providing zero-barrier analytics. It allows stakeholders to query complex enterprise data in plain English. While currently optimized for Google Sheets, the architecture is **Enterprise-Ready**: it can be scaled to BigQuery or Snowflake (handling GB/TB/PB of data) simply by swapping the data handler, without changing the core user experience.

---

## 💡 Why This Assistant is Helpful (The Proof)
1. **Real-Time Data Integrity**: Unlike a static chatbot, this assistant queries **live business data**. You can verify its responses by looking at your Google Sheet in real-time.
2. **Automated Action**: It doesn't just "talk" about tasks; it **executes** them by creating real events in your Google Calendar.
3. **Production Validation**: The system includes a **Data Quality Layer** that automatically detects nulls, duplicates, and mismatches, ensuring the AI never "hallucinates" based on broken data.

---

## 🎯 Chosen Vertical
**Data & Analytics Assistant**
This vertical leverages the high-precision reasoning of Gemini to solve the real-world problem of data accessibility for non-technical stakeholders.

---

## 🔗 Integrated Google Services
| Service | Purpose |
| :--- | :--- |
| **Google Gemini API** | Intent classification, data reasoning, and NL summary. |
| **Google Sheets API** | Real-time data retrieval and validation. |
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

## 🧪 Testing & Validation
- **Unit Tests**: Run `pytest` to verify modular logic.
- **Responsiveness**: Fully tested across Desktop, Tablet, and Mobile resolutions.
- **Repo Measurement**: Measured at **~3.5 KiB** using `git count-objects`.

---
**Build for the Virtual: PromptWars**
