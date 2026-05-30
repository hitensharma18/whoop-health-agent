import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_whoop_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    base_v1 = "https://api.prod.whoop.com/developer/v1"
    base_v2 = "https://api.prod.whoop.com/developer/v2"

    # Get cycle data (strain)
    cycle_res = requests.get(f"{base_v1}/cycle?limit=1", headers=headers)
    cycle = cycle_res.json()["records"][0]
    cycle_id = cycle["id"]

    # Get recovery data
    recovery_res = requests.get(f"{base_v2}/cycle/{cycle_id}/recovery", headers=headers)
    recovery = recovery_res.json()
    sleep_id = recovery["sleep_id"]

    # Get sleep data
    sleep_res = requests.get(f"{base_v2}/activity/sleep/{sleep_id}", headers=headers)
    sleep = sleep_res.json()

    # Get profile
    profile_res = requests.get(f"{base_v1}/user/profile/basic", headers=headers)
    profile = profile_res.json()

    return {
        "name": profile["first_name"],
        "strain": round(cycle["score"]["strain"], 2),
        "avg_heart_rate": cycle["score"]["average_heart_rate"],
        "max_heart_rate": cycle["score"]["max_heart_rate"],
        "calories": round(cycle["score"]["kilojoule"] * 0.239006),
        "recovery_score": recovery["score"]["recovery_score"],
        "resting_heart_rate": recovery["score"]["resting_heart_rate"],
        "hrv": round(recovery["score"]["hrv_rmssd_milli"], 2),
        "spo2": recovery["score"]["spo2_percentage"],
        "skin_temp": recovery["score"]["skin_temp_celsius"],
        "sleep_performance": sleep["score"]["sleep_performance_percentage"],
        "sleep_efficiency": round(sleep["score"]["sleep_efficiency_percentage"], 2),
        "sleep_consistency": sleep["score"]["sleep_consistency_percentage"],
        "total_sleep_hours": round(sleep["score"]["stage_summary"]["total_in_bed_time_milli"] / 3600000, 2),
        "rem_hours": round(sleep["score"]["stage_summary"]["total_rem_sleep_time_milli"] / 3600000, 2),
        "deep_hours": round(sleep["score"]["stage_summary"]["total_slow_wave_sleep_time_milli"] / 3600000, 2),
        "light_hours": round(sleep["score"]["stage_summary"]["total_light_sleep_time_milli"] / 3600000, 2),
        "respiratory_rate": round(sleep["score"]["respiratory_rate"], 2),
    }