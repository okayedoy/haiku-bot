import os
from datetime import datetime

import requests
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# Change these to your own location (search "my city latitude longitude")
LATITUDE = 39.00
LONGITUDE = -84.63

WEATHER_CODES = {
    0: "clear sky", 1: "mostly clear", 2: "partly cloudy", 3: "overcast",
    45: "foggy", 48: "foggy", 51: "light drizzle", 53: "drizzle",
    55: "heavy drizzle", 61: "light rain", 63: "rain", 65: "heavy rain",
    71: "light snow", 73: "snow", 75: "heavy snow", 80: "rain showers",
    81: "rain showers", 82: "violent rain showers", 95: "thunderstorm",
}

SYSTEM_PROMPT = (
    "You are a haiku poet. Write exactly one haiku in a 5-7-5 syllable pattern "
    "inspired by the moment described. Output only the three lines of the poem. "
    "No title, no explanation, no quotation marks."
)

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment


def get_weather():
    """Fetch current weather from Open-Meteo (free, no API key needed)."""
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
        },
        timeout=10,
    )
    response.raise_for_status()
    current = response.json()["current"]
    return {
        "temp": round(current["temperature_2m"]),
        "conditions": WEATHER_CODES.get(current["weather_code"], "unsettled weather"),
        "wind": round(current["wind_speed_10m"]),
    }


def write_haiku(weather, now):
    """Ask the LLM for a haiku about this moment."""
    prompt = (
        f"Date: {now.strftime('%A, %B %d')}\n"
        f"Time of day: {now.strftime('%I:%M %p')}\n"
        f"Weather: {weather['temp']}°F, {weather['conditions']}, "
        f"wind {weather['wind']} mph\n\n"
        "Write the haiku."
    )
    message = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    for block in message.content:
        if block.type == "text":
            return block.text.strip()
    return "(no haiku returned)"


def save_haiku(haiku, now):
    """Append the haiku to a running journal."""
    with open("haiku_log.md", "a", encoding="utf-8") as f:
        f.write(f"### {now.strftime('%Y-%m-%d %H:%M')}\n\n{haiku}\n\n---\n\n")


def main():
    now = datetime.now()
    try:
        weather = get_weather()
    except requests.RequestException as e:
        print(f"Couldn't fetch weather ({e}). Using a generic prompt instead.")
        weather = {"temp": 60, "conditions": "unknown skies", "wind": 5}

    haiku = write_haiku(weather, now)
    print(f"\n{weather['temp']}°F, {weather['conditions']}\n")
    print(haiku + "\n")
    save_haiku(haiku, now)


if __name__ == "__main__":
    main()