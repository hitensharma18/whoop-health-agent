# WHOOP Health Intelligence Agent 🏃

An agentic AI system that automatically fetches daily WHOOP biometric data, combines it with personal daily notes, generates an AI-powered health summary, and emails it every morning.

## Demo
![WHOOP Health Report](screenshot.png)
*Sample daily health report email with AI-generated summary*

## What It Does
- Fetches real-time sleep, recovery, strain and workout data from WHOOP API
- Reads personal daily notes (food, mood, stress, water intake)
- Uses Google Gemini AI to generate a personalized health summary
- Sends a beautifully formatted HTML email every morning at 10am
- Automatically refreshes OAuth tokens — fully autonomous, no manual login

## Tech Stack
- **Python** — core agent logic
- **WHOOP API** — biometric data (sleep, recovery, strain)
- **Google Gemini AI** — health summary generation
- **OAuth 2.0** — secure WHOOP authentication
- **Gmail SMTP** — automated email delivery
- **Flask** — OAuth callback server
- **Windows Task Scheduler** — daily automation

## Architecture
Daily at 10am (automated)
↓
Fetch WHOOP Data
(sleep + recovery + strain)
↓
Read personal notes.txt
(food, mood, stress, water)
↓
Gemini AI generates
personalized health summary
↓
HTML email sent automatically
↓
notes.txt cleared for next day

## Project Structure
whoop-agent/
├── main.py          # Agent orchestrator + OAuth + scheduler
├── whoop.py         # WHOOP API integration
├── ai.py            # Gemini AI summary generation
├── email_sender.py  # HTML email formatting + sending
├── .env             # API keys (gitignored)
├── tokens.json      # OAuth tokens (gitignored)
└── notes.txt        # Daily personal notes (gitignored)

## Sample Email
The daily email includes:
- Recovery score, HRV, resting heart rate
- Sleep performance, efficiency, consistency
- REM, deep and light sleep breakdown
- Daily strain and calories burned
- AI generated health summary and recommendations

## Setup
1. Clone the repo
2. Install dependencies:
```bash
   pip install requests google-genai python-dotenv schedule flask
```
3. Register app at developer.whoop.com and get Client ID and Secret
4. Get Google Gemini API key at aistudio.google.com
5. Get Gmail app password at myaccount.google.com
6. Create `.env` file:
WHOOP_CLIENT_ID=your_client_id
WHOOP_CLIENT_SECRET=your_client_secret
WHOOP_REDIRECT_URI=http://localhost:5000/callback
GEMINI_API_KEY=your_gemini_key
GMAIL_ADDRESS=your_gmail
GMAIL_APP_PASSWORD=your_app_password
EMAIL_RECIPIENT=your_email
7. Run to authenticate:
```bash
   python main.py
```
8. Schedule with Windows Task Scheduler at desired time

## Skills Demonstrated
- REST API integration with OAuth 2.0 authentication
- Agentic AI design and autonomous task execution
- LLM integration (Google Gemini)
- Automated data pipelines
- HTML email generation
- Scheduled task automation
