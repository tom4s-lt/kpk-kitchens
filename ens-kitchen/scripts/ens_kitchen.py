"""
ENS Kitchen - Price Data Collection and Analysis Script

This script fetches historical price data from CoinGecko for assets listed in the jt_kitchen
Google Sheet, calculates returns, and exports the results to a CSV file.

Note: This script is designed to run in Google Colab and requires Google authentication.
"""

# ==============================================
#  Install Required Packages
# ==============================================

# Google authentication libraries
from google.colab import auth
auth.authenticate_user()

import gspread
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)

# Other libraries
import pandas as pd
import requests
import time
from datetime import datetime
from typing import Optional, Dict, Any, List

# ==============================================
# Configuration
# ==============================================

class Config:
    """Configuration settings for the script."""
    COINGECKO_API_KEY = "CG-UGADVf4bJUJBCZV2BgAonsj7"
    COINGECKO_API_ENDPOINT = "https://api.coingecko.com/api/v3/coins/"
    ENS_KITCHEN_SHEET_URL = "https://docs.google.com/spreadsheets/d/1ml4EVLU6N7sv6R0Q102YOTwTPmStG64HlJ10aOkjIhY"
    SHEET_NAME = 'lk_assets'
    OUTPUT_FILE = 'prices.csv'
    # API request parameters
    API_PARAMS = {
        'vs_currency': 'usd',
        'days': '365',
        'interval': 'daily'
    }
    # API request headers
    API_HEADERS = {
        'accept': 'application/json',
        'x-cg-demo-api-key': COINGECKO_API_KEY
    }
    # Retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds

# ==============================================
# Function declaration
# ==============================================

def etl_gen_df_from_gsheet(
    wb_url: str,
    page: str,
    index_col: str = ''
) -> List[Dict[str, Any]]:
    """
    Extract data from a Google Sheet and convert it to a list of dictionaries.

    Args:
        wb_url (str): URL of the Google Spreadsheet to access.
        page (str): Name of the worksheet to read data from.
        index_col (str, optional): Column to use as index. Currently not used but kept for future use.
                                 Defaults to empty string.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing the worksheet data.
                             Each dictionary represents a row with column names as keys.

    Raises:
        ValueError: If wb_url or page is empty or None.
        Exception: For any other unexpected errors.
    """
    if not wb_url or not page:
        raise ValueError("Spreadsheet URL and page name cannot be empty or None")

    try:
        wb = gc.open_by_url(wb_url)
        sheet = wb.worksheet(page)
        return sheet.get_all_records()
    except Exception as e:
        print(f"Error accessing Google Sheet: {str(e)}")
        raise

def fetch_data_gecko_hist(
    asset_id: str,
    endpoint: str = Config.COINGECKO_API_ENDPOINT,
    api_key: str = Config.COINGECKO_API_KEY,
    max_retries: int = Config.MAX_RETRIES,
    retry_delay: int = Config.RETRY_DELAY
) -> Optional[Dict[str, Any]]:
    """
    Fetch historical price data for a given asset from CoinGecko API.

    Args:
        asset_id (str): The CoinGecko ID of the asset (e.g., 'bitcoin', 'ethereum')
        endpoint (str, optional): The CoinGecko API endpoint. Defaults to Config.COINGECKO_API_ENDPOINT.
        api_key (str, optional): The CoinGecko API key. Defaults to Config.COINGECKO_API_KEY.
        max_retries (int, optional): Maximum number of retry attempts. Defaults to Config.MAX_RETRIES.
        retry_delay (int, optional): Delay between retries in seconds. Defaults to Config.RETRY_DELAY.

    Returns:
        Optional[Dict[str, Any]]: JSON response containing historical price data if successful,
                                 None if all retry attempts fail.

    Raises:
        ValueError: If asset_id is empty or None.
    """
    if not asset_id:
        raise ValueError("asset_id cannot be empty or None")

    complete_endpoint = f"{endpoint}/{asset_id}/market_chart"

    for attempt in range(max_retries):
        try:
            response = requests.get(
                complete_endpoint,
                params=Config.API_PARAMS,
                headers=Config.API_HEADERS,
                timeout=30
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

# ==============================================
# Main Execution
# ==============================================

# Fetch assets from Google Sheet
json_assets_ = etl_gen_df_from_gsheet(Config.ENS_KITCHEN_SHEET_URL, Config.SHEET_NAME)

# Separate stablecoins and non-stablecoins
stablecoins = [
    asset for asset in json_assets_
    if asset.get("gecko_id", "") and asset.get("stablecoin", False)
]

non_stablecoins = [
    asset for asset in json_assets_
    if asset.get("gecko_id", "") and not asset.get("stablecoin", False)
]

print(f"Found {len(stablecoins)} stablecoins and {len(non_stablecoins)} non-stablecoins")

# Fetch and process price data for non-stablecoin assets
price_data = []
for asset in non_stablecoins:
    print(f"Fetching data for {asset['symbol']}...")
    gecko_hist_data = fetch_data_gecko_hist(asset['gecko_id'])
    
    if gecko_hist_data:
        # Create DataFrame for current asset
        df = pd.DataFrame(gecko_hist_data['prices'], columns=['ts', 'price'])
        df['gecko_id'] = asset['gecko_id']
        df['symbol'] = asset['symbol']
        price_data.append(df)
        print(f"Successfully fetched data for {asset['symbol']}")
    
    time.sleep(3)  # Rate limiting

print("\nPrice data collection complete")

# Process price data
print("\nProcessing price data...")
df_prices = pd.concat(price_data)
df_prices['date'] = pd.to_datetime(df_prices['ts'], unit='ms')

# Resample to daily frequency and calculate mean prices
df_prices = (df_prices
    .groupby(['symbol', 'gecko_id'])
    .resample('D', on='date')
    .mean()
    .reset_index()
    [['date', 'symbol', 'gecko_id', 'price']]  # Drop ts
    .sort_values('date', ascending=False)
)

# Add stablecoin data with price=1
if stablecoins:
    print("\nAdding stablecoin data...")
    # Get unique dates from the price data
    dates = df_prices['date'].unique()
    
    # Create stablecoin records
    stablecoin_data = []
    for asset in stablecoins:
        for date in dates:
            stablecoin_data.append({
                'date': date,
                'symbol': asset['symbol'],
                'gecko_id': asset['gecko_id'],
                'price': 1.0
            })
    
    # Convert to DataFrame and append to price data
    df_stablecoins = pd.DataFrame(stablecoin_data)
    df_prices = pd.concat([df_prices, df_stablecoins], ignore_index=True)
    df_prices = df_prices.sort_values('date', ascending=False)

print("Calculating returns...")

# Calculate returns
df_prices_wide = df_prices.pivot(
    index='date',
    columns='symbol',
    values='price'
).sort_index(ascending=True)

# Calculate 7d & 30d returns
df_returns_7d = df_prices_wide.iloc[-8:].div(df_prices_wide.iloc[-8]).mul(100)
df_returns_30d = df_prices_wide.iloc[-31:].div(df_prices_wide.iloc[-31]).mul(100)

# Convert returns to long format
df_returns_7d_long = df_returns_7d.reset_index().melt(
    id_vars='date',
    var_name='symbol',
    value_name='return_7d'
)
df_returns_30d_long = df_returns_30d.reset_index().melt(
    id_vars='date',
    var_name='symbol',
    value_name='return_30d'
)

# Merge all data
df_prices_complete = (df_prices
    .merge(df_returns_7d_long, on=['date', 'symbol'], how='left')
    .merge(df_returns_30d_long, on=['date', 'symbol'], how='left')
)

print("Return calculation complete")

# Export results
print(f"\nExporting results to {Config.OUTPUT_FILE}...")
df_prices_complete.to_csv(Config.OUTPUT_FILE, index=False)
print("Export complete!")