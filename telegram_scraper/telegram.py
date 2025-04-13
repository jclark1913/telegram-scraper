import sys

print(sys.path)
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import Chat, Channel, MessageMediaDocument
from telethon.utils import get_display_name
import asyncio
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta, timezone
from telegram_scraper.output import init_output, output_to_excel

load_dotenv()


api_id = os.environ.get("TELEGRAM_API_ID")
api_hash = os.environ.get("TELEGRAM_API_HASH")
phone_number = os.environ.get("TELEGRAM_PHONE_NUMBER")

end_time = datetime.now(timezone.utc) - timedelta(days=0)
start_time = end_time - timedelta(days=30)


async def get_telegram_data(
    telegram_links: list,
    search_term: str,
    start_time: datetime = start_time,
    end_time: datetime = end_time,
) -> list:
    """Accepts a list of telegram links and a search term and returns a list of dictionaries with the data

    Args:
        telegram_links (list): List of telegram links
        search_term (str): Search term to look for in the messages
        start_time (datetime): Start time to scrape from
        end_time (datetime): End time to scrape to

    Returns:
        list: List of dictionaries with the scraped data

    TODO:
        - Add solid error handling
    """
    async with TelegramClient("Main_client", api_id, api_hash) as client:
        results = []
        for link in telegram_links:
            try:
                print("Processing link: ", link)

                # Initialize results list
                link_results = []

                # Create entity to get display name + check if group
                entity = await client.get_entity(link)
                source_name = get_display_name(entity)
                link_type = is_telegram_group(entity)


                # Iterate through messages
                async for message in client.iter_messages(link):
                    print("TELE MSG TIME: ", message.date)
                    # Check if message w/i time range
                    if message.date > end_time:
                        continue
                    if message.date < start_time:
                        break

                    # Skip if no text or media
                    if not message.text and not message.media:
                        continue

                    # If search term is specified, skip messages that don't contain it
                    if search_term and search_term not in message.text:
                        continue

                    # If message contains media, get media link
                    if message.media:
                        media_link = "View media: " + f"{link}/{message.id}"
                    else:
                        media_link = "N/A"

                    # Get sender username if channel or user_id if group
                    if link_type is False:
                        sender = message.sender.username
                    elif link_type is True:
                        sender = message.from_id.user_id
                    else:
                        sender = "N/A"

                    # Append message details to results list
                    link_results.append(
                        {
                            "source": source_name,
                            "text": message.text,
                            "date": message.date,
                            "sender": sender,
                            "link": f"{link}/{message.id}",
                            "media": media_link,
                        }
                    )

                # Append link results to results list
                results.append({f"{link}": link_results})
            except Exception as e:
                print(f"There was an error processing {link}. Error message: {e}")
                continue

        print(results)
        return results


def is_telegram_group(entity: Chat) -> bool:
    """Returns true if entity is a group, or false if channel.

    Args:
        entity (Chat): Chat entity to check

    Returns:
        bool: True if group, False if channel, None if error

    """

    try:
        if isinstance(entity, Channel):
            return False if entity.broadcast else True
    except Exception as e:
        print("There was an error getting entity type: ", e)
        return None

