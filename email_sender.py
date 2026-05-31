import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def send_email(summary, whoop_data):
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = os.getenv("EMAIL_RECIPIENT")
    
    today = datetime.now().strftime("%B %d, %Y")
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your WHOOP Health Report - {today}"
    msg["From"] = sender
    msg["To"] = recipient

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; background:#f1f5f9;">
        
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); 
                    color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
            <h1 style="margin:0; font-size: 24px;">WHOOP Health Report</h1>
            <p style="margin:5px 0 0 0; opacity:0.8;">{today}</p>
        </div>

        <table width="100%" cellpadding="0" cellspacing="10" style="margin-bottom: 20px;">
            <tr>
                <td width="33%" style="background: #f0f9ff; border-left: 4px solid #0ea5e9;
                            padding: 20px; border-radius: 8px; text-align:center;">
                    <div style="color:#0ea5e9; font-size:28px; font-weight:bold;">{whoop_data['recovery_score']}%</div>
                    <div style="color:#666; font-size:13px; margin-top:5px;">Recovery</div>
                </td>
                <td width="33%" style="background: #f0fdf4; border-left: 4px solid #22c55e;
                            padding: 20px; border-radius: 8px; text-align:center;">
                    <div style="color:#22c55e; font-size:28px; font-weight:bold;">{whoop_data['sleep_performance']}%</div>
                    <div style="color:#666; font-size:13px; margin-top:5px;">Sleep</div>
                </td>
                <td width="33%" style="background: #fff7ed; border-left: 4px solid #f97316;
                            padding: 20px; border-radius: 8px; text-align:center;">
                    <div style="color:#f97316; font-size:28px; font-weight:bold;">{whoop_data['strain']}</div>
                    <div style="color:#666; font-size:13px; margin-top:5px;">Strain</div>
                </td>
            </tr>
        </table>

        <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: #1e293b; margin-top:0;">📊 Today's Stats</h3>
            <table style="width:100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 10px 8px; color:#666;">HRV</td>
                    <td style="padding: 10px 8px; font-weight:bold;">{whoop_data['hrv']} ms</td>
                    <td style="padding: 10px 8px; color:#666;">Resting HR</td>
                    <td style="padding: 10px 8px; font-weight:bold;">{whoop_data['resting_heart_rate']} bpm</td>
                </tr>
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 10px 8px; color:#666;">Total Sleep</td>
                    <td style="padding: 10px 8px; font-weight:bold;">{whoop_data['total_sleep_hours']} hrs</td>
                    <td style="padding: 10px 8px; color:#666;">REM Sleep</td>
                    <td style="padding: 10px 8px; font-weight:bold;">{whoop_data['rem_hours']} hrs</td>
                </tr>
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 10px 8px; color:#666;">Deep Sleep</td>
                    <td style="padding: 10px 8px; font-weight:bold;">{whoop_data['deep_hours']} hrs</td>
                    <td style="padding: 10px 8px; color:#666;">Calories</td>
                    <td style="padding: 10px 8px; font-weight:bold;">{whoop_data['calories']} kcal</td>
                </tr>
                <tr>
                    <td style="padding: 10px 8px; color:#666;">SpO2</td>
                    <td style="padding: 10px 8px; font-weight:bold;">{whoop_data['spo2']}%</td>
                    <td style="padding: 10px 8px; color:#666;">Respiratory Rate</td>
                    <td style="padding: 10px 8px; font-weight:bold;">{whoop_data['respiratory_rate']} br/min</td>
                </tr>
            </table>
        </div>

        <div style="background: white; padding: 25px; border-radius: 10px; margin-bottom: 20px; border-top: 4px solid #6366f1;">
            <h3 style="color: #1e293b; margin-top:0; font-size:18px;">🤖 AI Health Summary</h3>
            <div style="color: #334155; line-height: 2.0; font-size: 15px; border-left: 3px solid #e2e8f0; padding-left: 15px;">
                {summary.replace(chr(10), '<br>')}
            </div>
        </div>

        <div style="text-align:center; background: linear-gradient(135deg, #1a1a2e, #16213e); 
                    color:white; padding: 15px; border-radius: 10px; font-size:12px; margin-top:20px;">
            Generated by WHOOP Health Intelligence Agent 🏃
        </div>

    </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        print("Email sent successfully!")