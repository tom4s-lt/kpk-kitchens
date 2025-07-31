"""
Utility functions for kitchen notebooks.
"""

from typing import Dict, List, Optional, Any, Union
import pandas as pd
import requests
import time
from datetime import datetime
import spice

# ==============================================
#  API Request Functions
# ==============================================

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

def gecko_get_price_historical(
    base_url: str,
    asset_id: str,
    api_key: str,
    max_retries: int = 3,
    retry_delay: int = 5,
    timeout: int = 30,
    params: Dict[str, Any] = None,
    headers: Dict[str, Any] = None
) -> Optional[Dict[str, Any]]:
    """
    Fetch historical price data for a given asset from CoinGecko API.

    Args:
        base_url: The base URL of the API
        asset_id: The CoinGecko ID of the asset (e.g., 'bitcoin', 'ethereum')
        api_key: The CoinGecko API key
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        timeout: The timeout for the request in seconds
        params: Additional parameters for the API request
        headers: Additional headers for the API request

    Returns:
        Optional[Dict[str, Any]]: JSON response containing historical price data if successful,
                                 None if all retry attempts fail.
                                 Price included is the opening price of the day, not the closing.

    Raises:
        ValueError: If asset_id is empty or None.
    """
    if not asset_id:
        raise ValueError("asset_id cannot be empty or None")

    # Set default parameters if not provided
    if params is None:
        params = {
            'vs_currency': 'usd',
            'days': '365',
            'interval': 'daily'
        }
    
    # Add API key to params
    params['x_cg_demo_api_key'] = api_key

    if headers is None:
        headers = {
            'accept': 'application/json'
        }

    complete_endpoint = f"{base_url}/coins/{asset_id}/market_chart"

    for attempt in range(max_retries):
        try:
            response = requests.get(
                complete_endpoint,
                params=params,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"Error on attempt {attempt + 1}/{max_retries}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

    print(f"Failed to fetch data for {asset_id} after {max_retries} attempts")
    return None

def spice_query_id(
    query_id: int,
    api_key: str,
    refresh: bool = True,
    parameters: Dict[str, Any] = None,
) -> Optional[Dict[str, Any]]:
    """
    Query dune tables using https://github.com/paradigmxyz/spice
    Can refresh or get the latest execution result by modifying refresh param.

    Args:
        query_id: The Dune query ID
        api_key: The Dune API key
        refresh: Whether to refresh the query results
        parameters: Parameters for the query

    Returns:
        polars DataFrame with the query results
    """
    query = spice.query(
        query_id,
        refresh=refresh,
        api_key=api_key,
        parameters=parameters
    )

    return query.to_pandas()

# ==============================================
#  Data processing functions
# ==============================================

def ann_risk_return_252(returns_df):
    '''Summary statistics for portfolio (based on 252 trading days)

    args:
        returns_df: pandas DataFrame with returns

    returns:
        pandas DataFrame with summary statistics
    '''
    summary = returns_df.agg(["mean", "std"]).T
    summary.columns = ["Return", "Risk"]
    summary.Return = summary.Return * 252
    summary.Risk = summary.Risk * np.sqrt(252)
    return summary

def ann_risk_return_365(returns_df):
    '''
    Summary statistics for portfolio (based on 365 trading days)

    args:
        returns_df: pandas DataFrame with returns

    returns:
        pandas DataFrame with summary statistics
    '''
    summary = returns_df.agg(["mean", "std"]).T
    summary.columns = ["Return", "Risk"]
    summary.Return = summary.Return * 365
    summary.Risk = summary.Risk * np.sqrt(365)
    return summary










# ==============================================
#  Ohther/old
# ==============================================

# def fetch_data_with_retries(
#     endpoint: str,
#     params: Dict[str, Any],
#     max_retries: int = 3,
#     timeout: int = 10,
#     retry_delay: int = 5
# ) -> Optional[Dict[str, Any]]:
#     """
#     Fetch data from an API endpoint with retry logic.

#     Args:
#         endpoint: The API endpoint URL
#         params: Parameters for the API request
#         max_retries: Maximum number of retry attempts
#         timeout: Request timeout in seconds
#         retry_delay: Delay between retries in seconds

#     Returns:
#         JSON response data if successful, None otherwise
#     """
#     for attempt in range(max_retries):
#         try:
#             response = requests.get(
#                 endpoint,
#                 params=params,
#                 timeout=timeout
#             )
#             if response.status_code == 200:
#                 return response.json()
#             print(f"Error {response.status_code}: {response.text}")
#         except requests.exceptions.RequestException as e:
#             print(f"Network error: {e}")

#         print(f"Retrying {attempt + 1}/{max_retries}...")
#         time.sleep(retry_delay)

#     print("Failed to fetch data after multiple attempts.")
#     return None

# def process_coingecko_price_data(
#     data: Dict[str, Any],
#     token_configs: Dict[str, Dict[str, str]],
#     etl_now: datetime
# ) -> pd.DataFrame:
#     """
#     Process price data from CoinGecko API response.

#     Args:
#         data: Raw data from CoinGecko API
#         token_configs: Token configuration dictionary with coingecko_id and asset_class mappings
#         etl_now: Current timestamp for ETL process

#     Returns:
#         DataFrame with processed price data
#     """
#     df = pd.DataFrame(data)

#     # Mapping from coingecko ids to asset
#     inv_map = {v: k for k, v in token_configs['coingecko_id'].items()}

#     # Rename the columns from coingecko_id to symbol
#     df = df.rename(columns=inv_map).T
#     df.columns = ['price']

#     # Add the asset class for each asset
#     df['asset_class'] = df.index.map(token_configs['asset_class'])

#     # Add specific cases listed in the dictionary in the setup index
#     df.loc['weth', :] = df.loc['eth', :]

#     # Add datetime + etl_dt
#     df['datetime'] = etl_now
#     df['datetime'] = df['datetime'].dt.floor('s')
#     df['etl_dt'] = df['datetime']

#     return df 