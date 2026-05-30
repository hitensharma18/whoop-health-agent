from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_summary(whoop_data, notes):
    prompt = f"""
You are a personal health coach. Analyze this WHOOP health data and write a friendly daily health summary email.

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

Write a friendly summary with sleep analysis, recovery insights, how notes affected data, and 3 recommendations for tomorrow.
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    return response.text