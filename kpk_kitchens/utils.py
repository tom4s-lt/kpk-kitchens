"""
Utility functions for kitchen notebooks.
"""

from typing import Dict, List, Optional, Any, Union
import pandas as pd
import requests
import time
from datetime import datetime

def fetch_data_with_retries(
    endpoint: str,
    params: Dict[str, Any],
    max_retries: int = 3,
    timeout: int = 10,
    retry_delay: int = 5
) -> Optional[Dict[str, Any]]:
    """
    Fetch data from an API endpoint with retry logic.

    Args:
        endpoint: The API endpoint URL
        params: Parameters for the API request
        max_retries: Maximum number of retry attempts
        timeout: Request timeout in seconds
        retry_delay: Delay between retries in seconds

    Returns:
        JSON response data if successful, None otherwise
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(
                endpoint,
                params=params,
                timeout=timeout
            )
            if response.status_code == 200:
                return response.json()
            print(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")

        print(f"Retrying {attempt + 1}/{max_retries}...")
        time.sleep(retry_delay)

    print("Failed to fetch data after multiple attempts.")
    return None

def etl_gen_df_from_gsheet(
    gc,
    wb_url: str,
    page: str,
    output_type: str = 'json',
    index_col: str = ''
) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """
    Generates dataframe from a table stored in google sheets.
    str dtype is forced for conversion to decimal.Decimal type with all decimals.

    Args:
        gc: Google Sheets client instance
        wb_url: URL of the spreadsheet
        page: Name of the page that has to be accessed
        output_type: Type of output desired (json/df)
        index_col: Column label to be used as string

    Returns:
        DataFrame or list of records containing information from the page
    """
    wb = gc.open_by_url(wb_url)
    sheet = wb.worksheet(page)
    records = sheet.get_all_records()

    if output_type == 'df':
        df = pd.DataFrame(records, dtype=str)
        if index_col:
            df.set_index(index_col, drop=True, inplace=True)
        return df
    
    return records

def process_coingecko_price_data(
    data: Dict[str, Any],
    token_configs: Dict[str, Dict[str, str]],
    etl_now: datetime
) -> pd.DataFrame:
    """
    Process price data from CoinGecko API response.

    Args:
        data: Raw data from CoinGecko API
        token_configs: Token configuration dictionary with coingecko_id and asset_class mappings
        etl_now: Current timestamp for ETL process

    Returns:
        DataFrame with processed price data
    """
    df = pd.DataFrame(data)

    # Mapping from coingecko ids to asset
    inv_map = {v: k for k, v in token_configs['coingecko_id'].items()}

    # Rename the columns from coingecko_id to symbol
    df = df.rename(columns=inv_map).T
    df.columns = ['price']

    # Add the asset class for each asset
    df['asset_class'] = df.index.map(token_configs['asset_class'])

    # Add specific cases listed in the dictionary in the setup index
    df.loc['weth', :] = df.loc['eth', :]

    # Add datetime + etl_dt
    df['datetime'] = etl_now
    df['datetime'] = df['datetime'].dt.floor('s')
    df['etl_dt'] = df['datetime']

    return df 