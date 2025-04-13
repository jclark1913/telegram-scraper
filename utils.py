from datetime import datetime, timezone, timedelta
import re


def parse_date_input(date):
    """Parses a date and returns a datetime even if incomplete.

    Examples:
        - "2011-02-01" -> "2011-02-01 00:00:00+00:00"
        - "2011" -> "2011-01-01 00:00:00+00:00"
        - "2011-02-01 01:30:00" -> "2011-02-01 01:30:00+00:00"

    """


    date = date.strip()

    tz_pattern = re.compile(r'(Z|[+-]\d{2}(:?\d{2})?|[+-]\d{2}:\d{2})$')
    tz_match = tz_pattern.search(date)

    tzinfo = timezone.utc  # default to utc if no timezone

    if tz_match:
        tz_str = tz_match.group()
        date = date[:tz_match.start()].strip()

        if tz_str == "Z":
            tzinfo = timezone.utc
        else:
            if ":" in tz_str:
                hours, minutes = map(int, tz_str[1:].split(":"))
            elif len(tz_str) == 3:
                hours, minutes = int(tz_str[1:]), 0
            elif len(tz_str) == 5:  # +0200
                hours, minutes = int(tz_str[1:3]), int(tz_str[3:])
            else:
                print(f"Unrecognized timezone format: {tz_str}")
                tzinfo = timezone.utc

            delta = timedelta(hours=hours, minutes=minutes)
            if tz_str.startswith('-'):
                delta = -delta
            tzinfo = timezone(delta)

    if ' ' in date:
        date_str, time_str = date.split(' ', 1)
    else:
        date_str, time_str = date, ""

    date_parts = list(map(int, date_str.split('-')))
    while len(date_parts) < 3:
        date_parts.append(1)

    time_fields = [0, 0, 0]

    if time_str:
        time_parts = list(map(int, time_str.split(':')))
        for i in range(min(len(time_parts), 3)):
            time_fields[i] = time_parts[i]

    return datetime(*date_parts, *time_fields, tzinfo=tzinfo)