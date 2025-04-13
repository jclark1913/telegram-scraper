import asyncio
import argparse
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

from telegram_scraper.telegram import get_telegram_data
from telegram_scraper.output import init_output, output_to_excel, output_to_json

from utils import parse_date_input


async def main(args):
    """Main function. Runs get_telegram_data() with args and writes output to excel"""

    # convert dates to datetime objects, override times to be inclusive of whole day and convert to UTC
    # NOTE: Should add timezone fallback - will need additional arg.


    # start_time = datetime.strptime(args.start_time, "%Y-%m-%dT%H:%M:%SZ").replace(
    #     tzinfo=timezone.utc
    # )
    # end_time = datetime.strptime(args.end_time, "%Y-%m-%dT%H:%M:%SZ").replace(
    #     tzinfo=timezone.utc
    # )

    start_time = parse_date_input(args.start_time)
    end_time = parse_date_input(args.end_time)

    # raise error if start time is after end time
    if start_time > end_time:
        raise ValueError("Start time cannot be after end time.")

    # Initialize output file + return filename of new file
    final_output_location = init_output(
        type=args.output_type,
        output_dir=args.output_dir,
        output_filename=args.output_filename,
    )

    # get data
    results = await get_telegram_data(
        telegram_links=args.channels,
        search_term=args.search_term,
        start_time=start_time,
        end_time=end_time,
    )

    # output data to correct file type
    if args.output_type == "xlsx":
        output_to_excel(data=results, output_file=final_output_location)
    if args.output_type == "json":
        output_to_json(data=results, output_file=final_output_location)

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
        required=True,
        help="Enter a list of telegram links separated by spaces (e.g. --channels https://t.me/telegram_channel_1 https://t.me/telegram_channel_2)",
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
        "-of",
        "--output_filename",
        required=False,
        help="Enter an output file name. WHAT DEFAULT TO?",
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
