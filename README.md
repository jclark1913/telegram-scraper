# Overview

A lightweight command line tool for scraping data from Telegram channels and groups. Requires Telegram number, app id and API hash in order to work properly.

# Quickstart

```console
python -m main -h
```

```console
usage: main.py [-h] [-c CHANNELS [CHANNELS ...]] [-cf CHANNEL_FILE]
               [-s SEARCH_TERM] -from START_TIME -until END_TIME
               [-tz TIMEZONE] [-of OUTPUT_FILENAME] [-ot OUTPUT_TYPE]
               [-od OUTPUT_DIR]

options:
  -h, --help            show this help message and exit
  -c CHANNELS [CHANNELS ...], --channels CHANNELS [CHANNELS ...]
                        Enter a list of telegram links separated by spaces
                        (e.g. --channels https://t.me/telegram_channel_1
                        https://t.me/telegram_channel_2)
  -cf CHANNEL_FILE, --channel-file CHANNEL_FILE
                        Path to file containing list of telegram links.
  -s SEARCH_TERM, --search_term SEARCH_TERM
                        Enter a search term to look for in the messages
  -from START_TIME, --start_time START_TIME
                        Enter a start time to scrape from in the format YYYY-
                        MM-DD
  -until END_TIME, --end_time END_TIME
                        Enter an end time to scrape to in the format YYYY-MM-
                        DD
  -tz TIMEZONE, --timezone TIMEZONE
                        Enter a timezone. If none given defaults to UTC.
  -of OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                        Enter an output file name.
  -ot OUTPUT_TYPE, --output_type OUTPUT_TYPE
                        Enter an output file type. Defaults to excel.
  -od OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Enter an output directory. Defaults to ./output at
                        current directory.
```