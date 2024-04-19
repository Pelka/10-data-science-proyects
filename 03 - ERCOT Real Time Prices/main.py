import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from selectolax.parser import HTMLParser


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_data(url: str):
    """
    Retrieves HTML content from the given URL using GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        HTMLParser: Parsed HTML content.
    """

    res = requests.request("GET", url)
    return HTMLParser(res.text)


def parse_data(parser: HTMLParser):
    """
    Parses HTML table data.

    Args:
        parser (HTMLParser): Parsed HTML content.

    Returns:
        list: List of rows extracted from the table.
    """
    data = []
    table = parser.css_first(".tableStyle")
    for row in table.css("tr"):
        row_data = []
        for cell in row.css("th, td"):
            row_data.append(cell.text(strip=True))
        data.append(row_data)

    return data


def _create_ts(row: pd.Series):
    """
    Creates a timestamp from the given row.

    Args:
        row (pd.Series): A row of the DataFrame.

    Returns:
        str: The formatted timestamp.
    """
    date_parts = row["Oper Day"].split("/")
    year, month, day = map(int, [date_parts[2], date_parts[0], date_parts[1]])
    hour, minute = int(row["Interval Ending"][:2]), int(row["Interval Ending"][2:])
    hour = 0 if hour > 23 else hour
    return datetime(year, month, day, hour, minute).strftime(DATE_FORMAT)


def format_data(data: list[list]):
    """
    Formats parsed data into a DataFrame.

    Args:
        data (list[list]): Parsed data in the form of a list of lists.

    Returns:
        pd.DataFrame: Formatted DataFrame.
    """
    df = pd.DataFrame(data[1:], columns=data[0])
    df["ts"] = df.apply(_create_ts, axis=1)
    df["Creation_Date"] = datetime.now().strftime(DATE_FORMAT)
    df["Update_Date"] = None
    return df


def save_data(df: pd.DataFrame):
    """
    Saves DataFrame to a CSV file without duplicated records.

    Args:
        df (pd.DataFrame): DataFrame to be saved.
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_path, "result.csv")

    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path)
        old_df = old_df.drop(columns=["Update_Date"])
        new_df = pd.concat([old_df, df]).drop_duplicates(
            subset=["Oper Day", "Interval Ending"], keep="last"
        )
        new_df["Update_Date"] = datetime.now().strftime(DATE_FORMAT)
    else:
        new_df = df.copy()
    new_df.to_csv(file_path, index=False)


def start_taks(past_days: int = 1):
    """
    Initiates the data retrieval and saving process.

    Args:
        past_days (int): Number of past days to retrieve data for.
    """
    actual_day = datetime.now()
    for day in range(past_days):
        target_day = actual_day - timedelta(days=day)
        target_day = target_day.strftime("%Y%m%d")
        url = f"https://www.ercot.com/content/cdr/html/{target_day}_real_time_spp.html"
        parser = get_data(url)
        parsed_data = parse_data(parser)
        formated_data = format_data(parsed_data)
        save_data(formated_data)


if __name__ == "__main__":
    start_taks(2)
