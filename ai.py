import anthropic
import os
import re
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_summary(whoop_data, notes):
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%A, %B %d, %Y")

    prompt = f"""You are a personal health coach. Analyze this WHOOP health data from {yesterday} and write a friendly daily health summary email.

PERSON: {whoop_data['name']}

RECOVERY:
- Recovery Score: {whoop_data['recovery_score']}%
- HRV: {whoop_data['hrv']}ms
- Resting HR: {whoop_data['resting_heart_rate']}bpm
- SpO2: {whoop_data['spo2']}%
- Skin Temp: {whoop_data['skin_temp']}C

SLEEP:
- Performance: {whoop_data['sleep_performance']}%
- Efficiency: {whoop_data['sleep_efficiency']}%
- Consistency: {whoop_data['sleep_consistency']}%
- Total Sleep: {whoop_data['total_sleep_hours']}hrs
- REM: {whoop_data['rem_hours']}hrs
- Deep: {whoop_data['deep_hours']}hrs
- Respiratory Rate: {whoop_data['respiratory_rate']}

STRAIN:
- Strain: {whoop_data['strain']}
- Calories: {whoop_data['calories']}kcal
- Avg HR: {whoop_data['avg_heart_rate']}bpm

PERSONAL NOTES:
{notes if notes else "No notes today."}

Write a concise friendly summary in 3-4 short paragraphs max. Start by mentioning this is the health report for {yesterday}. No markdown formatting, some bullet points, plain text only. Cover: overall assessment, sleep analysis, recovery insights,use emoji as well not too much, and 3 quick recommendations for tomorrow. Make it actionable and easy to understand. Use a warm encouraging tone. Avoid technical jargon."""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = message.content[0].text
    text = re.sub(r'#{1,3}\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    return text