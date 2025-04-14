from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import re

TIMEZONE_ALIASES = {
    # Jordan
    "JST": "Asia/Amman",
    "Jordan": "Asia/Amman",

    # Western & Central Europe
    "WET": "Europe/Lisbon",        # Western European Time
    "WEST": "Europe/Lisbon",       # Western European Summer Time
    "CET": "Europe/Paris",         # Central European Time
    "CEST": "Europe/Paris",        # Central European Summer Time
    "MET": "Europe/Paris",         # Middle European Time
    "MEZ": "Europe/Berlin",        # German for CET
    "MESZ": "Europe/Berlin",       # German for CEST

    # United States
    "EST": "America/New_York",
    "EDT": "America/New_York",
    "Eastern": "America/New_York",

    "CST": "America/Chicago",
    "CDT": "America/Chicago",
    "Central": "America/Chicago",

    "MST": "America/Denver",
    "MDT": "America/Denver",
    "Mountain": "America/Denver",

    "PST": "America/Los_Angeles",
    "PDT": "America/Los_Angeles",
    "Pacific": "America/Los_Angeles",

    # General
    "UTC": "UTC",
    "Z": "UTC",
}

def parse_timezone(tz_str):

    if not tz_str:
        return None

    tz_str = tz_str.strip()

    # Manual alias map
    alias = TIMEZONE_ALIASES.get(tz_str.upper())
    if alias:
        return ZoneInfo(alias)

    # Try direct ZoneInfo
    try:
        return ZoneInfo(tz_str)
    except Exception:
        print(f"Unrecognized timezone format: {tz_str}. Defaulting to UTC")
        return None

def parse_date_input(date, tz_input):
    """Parses a date and returns a datetime. Accepts YYYY-MM-DD with or without
    HH:MM:SS. Optional timezone.
    """

    # check if there are 2 parts (time + date)

    date_str = date.strip()

    if " " in date_str:
        date_part, time_part = date_str.split(" ", 1)
    else:
        date_part, time_part = date_str, "00:00:00"

    date_parts = list(map(int, date_part.split("-")))

    time_parts = list(map(int, time_part.split(":")))
    while len(time_parts) < 3:
        time_parts.append(0)

    while len(date_parts) < 3:
        date_parts.append(1)

    if not tz_input or tz_input.upper() == "Z":
        tzinfo = timezone.utc
    else:
        tz_input = tz_input.strip()
        sign = -1 if tz_input.startswith("-") else 1
        offset_str = tz_input[1:]

        if ':' in offset_str:
            hours_str, minutes_str = offset_str.split(":")
        elif len(offset_str) == 4:
            hours_str, minutes_str = offset_str[:2], offset_str[2:]
        else:
            hours_str, minutes_str = offset_str, "0"

        hours = int(hours_str)
        minutes = int(minutes_str)
        delta = timedelta(hours=hours, minutes=minutes)
        tzinfo = timezone(sign * delta)

    return datetime(*date_parts, *time_parts, tzinfo=tzinfo)
