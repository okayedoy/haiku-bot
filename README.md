# Haiku Bot

Generates a haiku based on today's date and the current weather.

## Example

```
74°F, clear sky

Warm October night
a gentle breeze combs the dark,
make a wish, stars wait
```

## Setup
1. `python -m venv venv`
2. `.\venv\Scripts\Activate.ps1` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your Anthropic API key
5. Set `LATITUDE` and `LONGITUDE` in `haiku.py`
6. `python haiku.py`

## How it works
Fetches weather from Open-Meteo (free, no key needed), builds a prompt
from the date, time, and conditions, then asks an LLM for a 5-7-5 haiku
and logs it to `haiku_log.md`.

## Ideas for next
- Syllable checker with auto-retry
- `--style` flag (pirate, melancholy, cheerful)
- Daily GitHub Action