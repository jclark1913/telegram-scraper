from utils import parse_date_input, parse_timezone
from telegram_scraper.output import init_output, output_to_excel, output_to_json
from telegram_scraper.telegram import get_telegram_data
import asyncio
import argparse
from dotenv import load_dotenv

load_dotenv()


async def main(args):
    """Main function. Runs get_telegram_data() with args and writes output to excel"""

    # convert dates to datetime objects, override times to be inclusive of whole day and convert to UTC
    # NOTE: Should add timezone fallback - will need additional arg.

    if args.timezone:
        tz = parse_timezone(args.timezone)
    else:
        tz = None

    start_time = parse_date_input(args.start_time, tz)
    end_time = parse_date_input(args.end_time, tz)

    # raise error if start time is after end time
    if start_time > end_time:
        raise ValueError("Start time cannot be after end time.")

    # Initialize output file + return filename of new file
    final_output_location = init_output(
        type=args.output_type,
        output_dir=args.output_dir,
        output_filename=args.output_filename,
        tz=tz
    )

    channels = args.channels or []

    if args.channel_file:
        try:
            with open(args.channel_file, "r", encoding="utf-8") as f:
                file_channels = [line.strip() for line in f if line.strip()]
                channels.extend(file_channels)
        except FileNotFoundError:
            print(f"File not found: {args.channel_file}")

    if not channels:
        print("Please enter at least one valid Telegram channel.")
        return

    # get data
    results = await get_telegram_data(
        telegram_links=channels,
        search_term=args.search_term,
        start_time=start_time,
        end_time=end_time,
        tz=tz,
    )

    # output data to correct file type
    if args.output_type == "xlsx":
        output_to_excel(data=results, output_file=final_output_location, tz=tz)
    if args.output_type == "json":
        output_to_json(data=results, output_file=final_output_location, tz=tz)

    print("Finished. Output saved to: ", final_output_location)


def setup_args():
    """Setup command line arguments. Returns args for use in main()

    CLI Args:
        --channels: List of telegram channels
        --search_term: Search term to look for in the messages
        --start_time: Start time to scrape from
        --end_time: End time to scrape to

    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--channels",
        nargs="+",
        required=False,
        help="Enter a list of telegram links separated by spaces (e.g. --channels https://t.me/telegram_channel_1 https://t.me/telegram_channel_2)",
    )

    parser.add_argument(
        "-cf",
        "--channel-file",
        required=False,
        help="Path to file containing list of telegram links."
    )

    parser.add_argument(
        "-s",
        "--search_term",
        required=False,
        help="Enter a search term to look for in the messages",
    )

    parser.add_argument(
        "-st",
        "--start_time",
        required=True,
        help="Enter a start time to scrape from in the format YYYY-MM-DD",
    )

    parser.add_argument(
        "-et",
        "--end_time",
        required=True,
        help="Enter an end time to scrape to in the format YYYY-MM-DD",
    )

    parser.add_argument(
        "-tz",
        "--timezone",
        required=False,
        help="""Enter a timezone. If none given defaults to UTC. Timezones should be entered as follows:/n/n

        For EST: "+

        """
    )

    parser.add_argument(
        "-of",
        "--output_filename",
        required=False,
        help="Enter an output file name.",  # TODO: WHAT DEFAULT TO?
    )

    parser.add_argument(
        "-ot",
        "--output_type",
        required=False,
        default="xlsx",
        help="Enter an output file type. Defaults to excel.",
    )

    parser.add_argument(
        "-od",
        "--output_dir",
        required=False,
        default="./output",
        help="Enter an output directory. Defaults to ./output at current directory.",
    )

    return parser.parse_args()


def main_entrypoint():
    """Main entrypoint for script"""
    args = setup_args()
    asyncio.run(main(args))


if __name__ == "__main__":
    main_entrypoint()
