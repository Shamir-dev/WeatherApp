# from flask import Flask, jsonify, render_template
# import requests
# from datetime import datetime

# app = Flask(__name__)

# # Map weather codes to emojis + text
# WEATHER_MAP = {
#     0: ("☀️", "Sunny"),
#     1: ("☀️", "Mainly Sunny"),
#     2: ("🌤", "Partly Cloudy"),
#     3: ("☁️", "Cloudy"),
#     45: ("☁️", "Fog"),
#     51: ("🌧", "Light Rain"),
#     61: ("🌧", "Rainy"),
#     71: ("❄️", "Snow"),
#     # Custom night fallbacks
#     100: ("🌙", "Clear Night"),
#     101: ("☁️", "Cloudy Night"),
# }
# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/weather")
# def weather():
#     lat, lon = 27.717836, 85.314428
#     url = (
#         f"https://api.open-meteo.com/v1/forecast?"
#         f"latitude={lat}&longitude={lon}"
#         f"&hourly=temperature_2m,weathercode,precipitation_probability"
#         f"&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_probability_max"
#         f"&timezone=auto"
#     )

#     response = requests.get(url).json()

#     # Hourly data
#     hourly_data = []
#     for t, temp, code, prob in zip(
#         response["hourly"]["time"],
#         response["hourly"]["temperature_2m"],
#         response["hourly"]["weathercode"],
#         response["hourly"]["precipitation_probability"]
#     ):
#         dt = datetime.fromisoformat(t)
#         date_str = dt.strftime("%b %d")   # Jul 31
#         time_str = dt.strftime("%I %p")   # 11 AM

#         emoji, status = WEATHER_MAP.get(code, (None, None))
#         if not emoji:
#          hour = dt.hour
#          if 6 <= hour < 18:  # daytime
#              if prob >= 50:
#                  emoji, status = ("☁️", "Cloudy")
#              else:
#                  emoji, status = ("☀️", "Sunny")
#          else:  # nighttime
#             if prob >= 50:
#                  emoji, status = ("☁️", "Cloudy Night")
#             else:
#                emoji, status = ("🌙", "Clear Night")


#         hourly_data.append({
#             "date": date_str,
#             "time": time_str,
#             "temperature": temp,
#             "status": status,
#             "emoji": emoji,
#             "probability": prob
#         })

#     # Daily data with summary logic
#     daily_data = []
#     for idx, d in enumerate(response["daily"]["time"]):
#         dt = datetime.fromisoformat(d)
#         date_str = dt.strftime("%a %d %b")

#         tmax = response["daily"]["temperature_2m_max"][idx]
#         tmin = response["daily"]["temperature_2m_min"][idx]

#         # Extract hourly slice for this day
#         day_hours = []
#         for h_idx, ht in enumerate(response["hourly"]["time"]):
#             if ht.startswith(d):  # same date
#                 hdt = datetime.fromisoformat(ht)
#                 day_hours.append({
#                     "date": hdt.strftime("%b %d"),
#                     "time": hdt.strftime("%I %p"),
#                     "temp": response["hourly"]["temperature_2m"][h_idx],
#                     "prob": response["hourly"]["precipitation_probability"][h_idx],
#                     "emoji": WEATHER_MAP.get(response["hourly"]["weathercode"][h_idx], ("☀️","Sunny"))[0],
#                     "status": WEATHER_MAP.get(response["hourly"]["weathercode"][h_idx], ("☀️","Sunny"))[1]
#                 })

#         # Summary rule: 6am–8pm, ≥2 consecutive rainy hours
#         summary_status = "Sunny"
#         summary_emoji = "☀️"
#         for i in range(len(day_hours) - 1):
#             hour_dt = datetime.strptime(day_hours[i]["time"], "%I %p")
#             if 6 <= hour_dt.hour <= 20:
#                 if (day_hours[i]["prob"] >= 70 and day_hours[i+1]["prob"] >= 70):
#                     summary_status = "Rainy"
#                     summary_emoji = "🌧"
#                     break

#         # fallback if majority cloudy
#         cloudy_count = sum(1 for h in day_hours if h["status"] == "Cloudy")
#         if summary_status == "Sunny" and cloudy_count > len(day_hours) // 2:
#             summary_status = "Cloudy"
#             summary_emoji = "☁️"

#         daily_data.append({
#             "date": date_str,
#             "status": summary_status,
#             "emoji": summary_emoji,
#             "temp_min": tmin,
#             "temp_max": tmax,
#             "hourly": day_hours
#         })

#     return jsonify({
#         "hourly": hourly_data,
#         "daily": daily_data
#     })

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, jsonify, render_template
import requests
from datetime import datetime
import os

app = Flask(__name__)

mylocation = "Lainchaur/Thamel"

# Complete WMO Weather Interpretation Codes (WW)
WEATHER_MAP = {
    0: {"day": ("☀️", "Sunny"), "night": ("🌙", "Clear Night")},
    1: {"day": ("🌤️", "Mainly Sunny"), "night": ("🌙", "Mainly Clear")},
    2: {"day": ("⛅", "Partly Cloudy"), "night": ("☁️", "Partly Cloudy")},
    3: {"day": ("☁️", "Cloudy"), "night": ("☁️", "Cloudy Night")},
    45: {"day": ("🌫️", "Fog"), "night": ("🌫️", "Fog")},
    51: {"day": ("🌧️", "Drizzle"), "night": ("🌧️", "Drizzle")},
    61: {"day": ("🌧️", "Light Rain"), "night": ("🌧️", "Light Rain")},
    63: {"day": ("🌧️", "Strong Rain"), "night": ("🌧️", "Strong Rain")},
    71: {"day": ("❄️", "Snow"), "night": ("❄️", "Snow")},
    80: {"day": ("🌧️", "Rain Showers"), "night": ("🌧️", "Rain Showers")},
    95: {"day": ("⛈️", "Thunderstorm"), "night": ("⛈️", "Thunderstorm")},
    96: {"day": ("⛈️", "Severe Thunderstorm"), "night": ("⛈️", "Severe Thunderstorm")},
}
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather")
def weather():
    lat, lon = 27.717836, 85.314428
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,weather_code,precipitation_probability,is_day"
        f"&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch weather data", "details": str(e)}), 500

    hourly_data = []
    for t, temp, code, prob, is_day_flag in zip(
        data["hourly"]["time"],
        data["hourly"]["temperature_2m"],
        data["hourly"]["weather_code"],
        data["hourly"]["precipitation_probability"],
        data["hourly"]["is_day"]
    ):
        dt = datetime.fromisoformat(t)
        time_type = "day" if is_day_flag else "night"
        
        weather_info = WEATHER_MAP.get(code, {"day": ("☀️", "Clear"), "night": ("🌙", "Clear Night")})
        emoji, status = weather_info[time_type]

        if code >= 51:
            if prob > 85:
                status = "Certainly rain"
                emoji = "⛈️"
            elif 70 <= prob <= 85:
                status = "High chances of rain"
                emoji = "🌧️"
            elif 50 <= prob < 70:
                status = "Moderate chances of rain"
                emoji = "🌦️"
            elif 30 <= prob < 50:
                status = "Low chances of rain"
                emoji = "🌦️"
            else:
                status = "Very Low chances of rain"
                emoji = "⛅"

        # Providing dual key names to preserve compatibility with existing JS templates
        hourly_data.append({
            "date": dt.strftime("%b %d"),
            "time": dt.strftime("%I %p"),
            "hour": dt.hour,
            "temp": temp,
            "temperature": temp,
            "prob": prob,
            "probability": prob,
            "status": status,
            "emoji": emoji,
            "code": code
        })

    daily_data = []
    for idx, d in enumerate(data["daily"]["time"]):
        dt = datetime.fromisoformat(d)
        date_formatted = dt.strftime("%b %d")
        
        # Extract hourly slice for the day
        day_hours = [h for h in hourly_data if h["date"] == date_formatted]

        # Focus daily status calculation on daytime hours (6 AM to 8 PM)
        daytime_hours = [h for h in day_hours if 6 <= h["hour"] <= 20]
        eval_hours = daytime_hours if daytime_hours else day_hours

        max_prob = max((h["prob"] for h in eval_hours), default=0)
        has_storm = any(h["code"] in [95, 96, 99] for h in eval_hours)
        has_heavy_rain = any(h["code"] in [63, 65, 82] or h["prob"] >= 80 for h in eval_hours)
        has_light_rain = any(h["prob"] >= 40 or h["code"] in [51, 53, 55, 61, 80] for h in eval_hours)

        # Granular summary priority logic
       # Check if any hourly WMO code during the day indicates precipitation (51+)
        has_rain_code = any(h["code"] >= 51 for h in eval_hours)

        # Granular summary priority logic based on maximum daily probability
        if has_rain_code:
            if max_prob > 85:
                summary_emoji, summary_status = "🌧️", "Certainly rain"
            elif 70 <= max_prob <= 85:
                summary_emoji, summary_status = "🌧️", "High chances of rain"
            elif 50 <= max_prob < 70:
                summary_emoji, summary_status = "🌧️", "Moderate chances of rain"
            elif 30 <= max_prob < 50:
                summary_emoji, summary_status = "⛅", "Low chances of rain"
            else:
                summary_emoji, summary_status = "⛅", "Very Low chances of rain"
        else:
            # Fallback to cloud coverage if no precipitation codes are detected
            cloudy_cnt = sum(1 for h in eval_hours if h["code"] in [2, 3, 45, 48])
            if cloudy_cnt > len(eval_hours) // 2:
                summary_emoji, summary_status = "☁️", "Mostly Cloudy"
            else:
                summary_emoji, summary_status = "☀️", "Mostly Sunny"
        # Sanitize internal helper keys before sending to client
        cleaned_day_hours = [{k: v for k, v in h.items() if k != "hour"} for h in day_hours]

        daily_data.append({
            "date": dt.strftime("%a %d %b"),
            "status": summary_status,
            "emoji": summary_emoji,
            "temp_min": data["daily"]["temperature_2m_min"][idx],
            "temp_max": data["daily"]["temperature_2m_max"][idx],
            "max_prob": data["daily"]["precipitation_probability_max"][idx],
            "hourly": cleaned_day_hours
        })

    return jsonify({
        "hourly": hourly_data,
        "daily": daily_data
    })

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "False").lower() == "true")