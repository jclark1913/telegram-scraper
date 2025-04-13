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
    """Parses a date and returns a datetime even if incomplete.

    Examples:
        - "2011-02-01" -> "2011-02-01 00:00:00+00:00"
        - "2011" -> "2011-01-01 00:00:00+00:00"
        - "2011-02-01 01:30:00" -> "2011-02-01 01:30:00+00:00"

    Also supports an optional timezone argument. If not provided defaults to
    UTC.
    """

    date = date.strip()
    tzinfo = timezone.utc  # default

    # Determine if timezone is embedded in the string
    tz_pattern = re.compile(r'(Z|[+-]\d{2}(?::?\d{2})?)$')
    tz_match = tz_pattern.search(date)

    if tz_match:
        tz_str = tz_match.group()
        date = date[:tz_match.start()].strip()
    elif tz_input:
        tz_str = tz_input.strip()
    else:
        tz_str = "Z"

    # Parse timezone
    if tz_str == "Z":
        tzinfo = timezone.utc
    else:
        sign = -1 if tz_str.startswith("-") else 1
        offset_str = tz_str[1:]

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

    # Split date and time
    if ' ' in date:
        date_str, time_str = date.split(' ', 1)
    else:
        date_str, time_str = date, ""

    date_parts = list(map(int, date_str.split('-')))
    while len(date_parts) < 3:
        date_parts.append(1)  # Fill missing parts with 1

    time_fields = [0, 0, 0]
    if time_str:
        time_parts = list(map(int, time_str.split(':')))
        for i in range(min(len(time_parts), 3)):
            time_fields[i] = time_parts[i]

    return datetime(*date_parts, *time_fields, tzinfo=tzinfo)
