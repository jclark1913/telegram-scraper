import os
import pandas as pd
from datetime import datetime, timezone


def init_output(
    type: str = "xlsx",
    output_dir: str = "./output",
    output_filename=None,
    tz=timezone.utc
) -> str:
    """Creates the output directory and initiates output file.

    Args:
        - type (str): Type of output file. Valid types are "json" and "xlsx". Defaults to "xlsx"
        - output_dir (str): Output directory
        - output_filename (str): Output filename. If not specified, will use current date and time.


    Returns:
        - filename of the output file (str)
    """

    valid_types = ["json", "xlsx"]
    if type not in valid_types:
        raise ValueError(f"Invalid output type. Valid types are {valid_types}")

    # Set default output directory if not specified
    if not output_dir:
        output_dir = "./output"

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get current date and time for filename
    if not output_filename:
        file_name = datetime.now().astimezone(tz).strftime("%Y-%m-%d_%H-%M-%S")
    else:
        file_name = output_filename

    # Check if file already exists and prompt user for input
    # NOTE: Needs refactoring to sanitize input for filename
    if os.path.exists(os.path.join(f"{output_dir}", f"{file_name}.{type}")):
        while True:
            response = input(
                "WARNING: Filename already exists!\n\nOverwrite file and continue: r or replace\n\nEnter new filename: n or new\n\nCancel operation: c or cancel\n\n"
            )
            if response.lower() in ["c", "cancel"]:
                raise ValueError("Operation cancelled")
            elif response.lower() in ["r", "replace"]:
                file_name = output_filename
                break
            elif response.lower() in ["n", "new"]:
                new_filename = input("Enter new filename: ")
                if new_filename == file_name:
                    print("New filename cannot be the same as the old filename.")
                    continue
                break

    # Create empty output file and return filename
    with open(os.path.join(f"{output_dir}", f"{file_name}.{type}"), "w") as f:
        pass

    return os.path.join(f"{output_dir}", f"{file_name}.{type}")


def output_to_excel(data: list, output_file: str, tz: timezone) -> None:
    """Writes scraped data to excel file.

    Args:
        - data (list): List of dictionaries with the scraped data
        - output_file (str): Output file to write to
        - tz (timezone): Timezone to convert message to


    Returns:
        - None
    """

    # Create pandas dataframe from data

    writer = pd.ExcelWriter(output_file, engine="xlsxwriter")

    for link in data:
        flattened_data = []
        channel_name = list(link.keys())[0]
        for result in link:
            for message in link[result]:
                flattened_data.append(
                    {
                        "source": message["source"],
                        "link": message["link"],
                        "text": message["text"],
                        "date": message["date"].astimezone(tz).strftime("%Y-%m-%d %H:%M:%S"),
                        "sender": message["sender"],
                        "media": message["media"],
                    }
                )

        sheet_name = channel_name.replace("https://t.me/","").replace("@", "")[:31]
        df = pd.DataFrame(flattened_data)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        workbook  = writer.book
        worksheet = writer.sheets[sheet_name]

        # Format: wrap text + align top
        wrap_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'top'
        })

        # Bold headers
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D7E4BC',
            'border': 1
        })

        # Apply wrap format to all data cells
        worksheet.set_column('A:F', 30, wrap_format)

        # Apply header format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Optional: freeze first row
        worksheet.freeze_panes(1, 0)

    # Output to excel

    writer.close()


def output_to_json(data: list, output_file: str, tz: timezone) -> None:
    """Writes scraped data to json file.

    Args:
        - data (list): List of dictionaries with the scraped data
        - output_file (str): Output file to write to

    Returns:
        - None
    """

    # Create pandas dataframe from data
    flattened_data = []

    for link in data:
        for result in link:
            for message in link[result]:
                flattened_data.append(
                    {
                        "source": message["source"],
                        "link": message["link"],
                        "text": message["text"],
                        "date": message["date"].astimezone(tz).strftime("%Y-%m-%d %H:%M:%S"),
                        "sender": message["sender"],
                        "media": message["media"],
                    }
                )

    df = pd.DataFrame(flattened_data)

    # Output to json
    df.to_json(output_file, orient="records", indent=4)
