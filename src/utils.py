import logging
import os
from .config import (
    LOGS_DIR,
    PRODUCT,
    TOP_RESULTS
)
from googlesearch import search
import json
import pandas as pd

os.makedirs(LOGS_DIR, exist_ok=True)
log_file_path = os.path.join(LOGS_DIR, 'logs.log')
logging.basicConfig(
    force=True,
    level=logging.INFO if PRODUCT else logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
    ] if PRODUCT else [
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

def search_websites(keywords, num_results=TOP_RESULTS):
    """
    Perform Google searches for a list of keywords and return a list of websites.

    Args:
        keywords (list): A list of keywords to search for.
        num_results (int): Number of results to fetch for each keyword. Default is 10.

    Returns:
        list: A list of websites (URLs) from the search results.
    """
    websites = []
    for keyword in keywords:
        try:
            logging.info(f"Searching for keyword: {keyword}")
            results = search(keyword, num_results=num_results)
            websites.extend(results)
        except Exception as e:
            logging.error(f"Error occurred while searching for '{keyword}': {e}")
    return websites

def load_jsonl_to_list(file_path):
    """
    Load a JSONL (JSON Lines) file into a list of dictionaries.

    Args:
        file_path (str): The path to the JSONL file.

    Returns:
        list: A list of dictionaries loaded from the JSONL file.
    """
    try:
        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
        logging.info(f"JSONL file successfully loaded from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error occurred while loading JSONL file '{file_path}': {e}")
        return []
    
def dump_list_to_jsonl(data, file_path):
    """
    Dump a list of dictionaries to a JSONL (JSON Lines) file.

    Args:
        data (list): A list of dictionaries to write to the JSONL file.
        file_path (str): The path to the JSONL file where the data will be written.
    """
    try:
        with open(file_path, 'w') as file:
            for item in data:
                file.write(json.dumps(item) + '\n')
        logging.info(f"Data successfully dumped to JSONL file at {file_path}")
    except Exception as e:
        logging.error(f"Error occurred while dumping data to JSONL file '{file_path}': {e}")

def list_to_dataframe(data):
    """
    Convert a list of dictionaries to a pandas DataFrame. If a dictionary contains a value
    that is a list of strings, split it into multiple rows with the same other values.

    Args:
        data (list): A list of dictionaries.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the list of dictionaries,
                          with list values split into multiple rows.
    """
    try:
        # Normalize the data by expanding lists into multiple rows
        normalized_data = []
        for item in data:
            for key, value in item.items():
                if isinstance(value, list):
                    for sub_value in value:
                        new_item = item.copy()
                        new_item[key] = sub_value
                        normalized_data.append(new_item)
                    break
            else:
                normalized_data.append(item)

        df = pd.DataFrame(normalized_data)
        logging.info("List of dictionaries successfully converted to DataFrame with expanded rows for list values")
        return df
    except Exception as e:
        logging.error(f"Error occurred while converting list of dictionaries to DataFrame: {e}")
        return pd.DataFrame()

def load_csv_to_dataframe(file_path:str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"CSV file successfully loaded into DataFrame from {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error occurred while loading CSV file '{file_path}': {e}")
        return pd.DataFrame()