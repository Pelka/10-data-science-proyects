import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from selectolax.parser import HTMLParser


def get_data(url: str):
    """
    Retrieves HTML content from the given URL using GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        HTMLParser: Parsed HTML content.
    """

    # headers = {
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    #     "accept-language": "en-US,en;q=0.5",
    #     "cache-control": "max-age=0",
    #     "cookie": "visid_incap_1217363=40YplimcQJeeAN8TPac9sSr5H2YAAAAAQUIPAAAAAACHlq0JfMNpNLkcEXNtje7K; incap_ses_1605_1217363=ZHt7C5zUpEzJF0S6AxtGFir5H2YAAAAA8MZKhCy+M5FtdUAq/+5KKA==; JSESSIONID=97945DC485C4D1A60EFE7C240A14CCBB.w_prblwbc0093b",
    #     "if-modified-since": "Wed, 17 Apr 2024 16:32:36 GMT",
    #     "if-none-match": "97e4-6164d66fd93e7",
    #     "referer": "https://www.ercot.com/content/cdr/html/20240412_real_time_spp.html",
    #     "sec-ch-ua": '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": '"Linux"',
    #     "sec-fetch-dest": "document",
    #     "sec-fetch-mode": "navigate",
    #     "sec-fetch-site": "same-origin",
    #     "sec-fetch-user": "?1",
    #     "sec-gpc": "1",
    #     "upgrade-insecure-requests": "1",
    #     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    # }

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


def format_data(data: list[list]):
    """
    Formats parsed data into a DataFrame.

    Args:
        data (list[list]): Parsed data in the form of a list of lists.

    Returns:
        pd.DataFrame: Formatted DataFrame.
    """

    def create_ts(row: any):
        splited_date = list(map(int, row["Oper Day"].split("/")))
        hour = int(row["Interval Ending"][:2])
        hour = 0 if hour > 23 else hour
        minute = int(row["Interval Ending"][2:])
        second = 0
        return datetime(
            splited_date[2], splited_date[0], splited_date[1], hour, minute, second
        ).strftime("%Y-%m-%d %H:%M:%S")

    df = pd.DataFrame(data[1:], columns=data[0])
    df["ts"] = df.apply(create_ts, axis=1)
    df["Creation_Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df


def save_data(df: pd.DataFrame):
    """
    Saves DataFrame to a CSV file without duplicated records.

    Args:
        df (pd.DataFrame): DataFrame to be saved.
    """
    current_path = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(current_path + "/result.csv"):
        df["Update_Date"] = None
        df.to_csv(current_path + "/result.csv", index=False)
    else:
        old_df = pd.read_csv(f"{current_path}/result.csv")
        old_df = old_df.drop(columns=["Update_Date"])
        new_df = pd.concat([old_df, df]).drop_duplicates(
            subset=["Oper Day", "Interval Ending"]
        )
        new_df["Update_Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_df.to_csv(current_path + "/result.csv", index=False)


def start_taks(past_days: int):
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
    start_taks(3)
