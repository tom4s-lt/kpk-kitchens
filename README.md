# KPK Kitchens

Shared utilities and configuration for KPK kitchen notebooks.

## Overview

KPK Kitchens is a Python package that provides shared utilities and configuration for financial data analysis and portfolio management across different "kitchens" (workspaces). It includes:

- **Configuration Management**: Centralized settings for API keys, endpoints, and project-specific configurations
- **Data Utilities**: Functions for fetching data from CoinGecko, Dune Analytics, and Google Sheets
- **ETL Tools**: Data processing and transformation utilities
- **Portfolio Management**: Tools for handling balances, transactions, and price data

## Installation

### Local Installation

```bash
# Clone the repository
git clone <repository-url>
cd kpk-kitchens

# Install the package
pip install -e .
```

### Google Colab Installation

Add this to the first cell of your notebook:

```python
# Install the package from GitHub
GITHUB_TOKEN = "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"
BRANCH = "main"
! pip install git+https://{GITHUB_TOKEN}@github.com/tom4s-lt/kpk-kitchens.git@{BRANCH}

# Import the configuration and utilities
from kpk_kitchens.config import JTConfig  # or ENSConfig
from kpk_kitchens.utils import fetch_data_with_retries, etl_gen_df_from_gsheet, process_coingecko_price_data
```

## Configuration

The package provides two main configuration classes:

### JTConfig (Joint Treasury Kitchen)
```python
from kpk_kitchens.config import JTConfig

config = JTConfig()

# Access configuration values
print(config.COINGECKO_API_KEY)
print(config.WORKBOOK_URL)
print(config.PORTFOLIO_TOKENS)
```

### ENSConfig (ENS Kitchen)
```python
from kpk_kitchens.config import ENSConfig

config = ENSConfig()

# Access ENS-specific configuration
print(config.DUNE_ID_SF_EXTRACT_ENS_FINANCIALS)
print(config.LK_ADDRESSES)
```

## Usage

The package provides shared configuration and utility functions that can be used across different kitchen notebooks:

```python
# Import the configuration for your kitchen
from kpk_kitchens.config import JTConfig  # or ENSConfig

# Use the configuration
config = JTConfig()
config.setup_plot_style()

# Use utility functions
from kpk_kitchens.utils import fetch_data_with_retries

data = fetch_data_with_retries(
    endpoint=config.COINGECKO_PRICE_ENDPOINT,
    params={'x_cg_demo_api_key': config.COINGECKO_API_KEY},
    max_retries=config.MAX_RETRIES,
    timeout=config.DEFAULT_TIMEOUT,
    retry_delay=config.RETRY_DELAY
)
```

### Google Sheets Integration

```python
from kpk_kitchens.utils import etl_gen_df_from_gsheet
import gspread
from google.oauth2.service_account import Credentials

# Setup Google Sheets client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('path/to/credentials.json', scopes=scope)
gc = gspread.authorize(creds)

# Fetch data from Google Sheets
df = etl_gen_df_from_gsheet(
    gc=gc,
    wb_url=config.WORKBOOK_URL,
    page=config.LK_ASSETS,
    output_type='df'
)
```

### CoinGecko API Integration

```python
from kpk_kitchens.utils import gecko_get_price_historical

# Fetch historical price data
price_data = gecko_get_price_historical(
    base_url=config.COINGECKO_API_BASE_URL,
    asset_id='ethereum',
    api_key=config.COINGECKO_API_KEY,
    params={
        'vs_currency': 'usd',
        'days': '30',
        'interval': 'daily'
    }
)
```

### Dune Analytics Integration

```python
from kpk_kitchens.utils import spice_query_id

# Query Dune Analytics
df = spice_query_id(
    query_id=config.DUNE_ID_SF_EXTRACT_ENS_FINANCIALS,
    api_key=config.DUNE_API_KEY,
    refresh=True
)
```

## API Reference

### Configuration Classes

#### BaseConfig
Base configuration class containing shared settings:
- `COINGECKO_API_KEY`: CoinGecko API key
- `DUNE_API_KEY`: Dune Analytics API key
- `MAX_RETRIES`: Maximum retry attempts for API calls
- `DEFAULT_TIMEOUT`: Default timeout for requests
- `RETRY_DELAY`: Delay between retries

#### JTConfig
Joint Treasury specific configuration:
- `WORKBOOK_URL`: Google Sheets workbook URL
- `PORTFOLIO_TOKENS`: Token configuration mappings
- `TOKEN_ADDRESSES`: Token address mappings
- `TTE_DATE`: Important date reference

#### ENSConfig
ENS specific configuration:
- `WORKBOOK_URL`: ENS Google Sheets workbook URL
- `DUNE_ID_SF_EXTRACT_ENS_FINANCIALS`: Dune query ID for ENS financials
- `DUNE_ID_EXTRACT_ENS_DAO_HOLDINGS`: Dune query ID for ENS holdings

### Utility Functions

#### `etl_gen_df_from_gsheet(gc, wb_url, page, output_type='json', index_col='')`
Generates DataFrame from Google Sheets table.

#### `gecko_get_price_historical(base_url, asset_id, api_key, ...)`
Fetches historical price data from CoinGecko API.

#### `spice_query_id(query_id, api_key, refresh=True, parameters=None)`
Queries Dune Analytics using Spice library.

## Project Structure

```
kpk-kitchens/
├── kpk_kitchens/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration classes
│   └── utils.py             # Utility functions
├── models/
│   └── README.md            # Data model documentation
├── files/
│   ├── jt-kitchen/          # Joint Treasury kitchen files
│   └── ens-kitchen/         # ENS kitchen files
├── setup.py                 # Package installation
└── README.md                # This file
```

### Kitchens

- **jt-kitchen/**: Joint Treasury kitchen - handles portfolio management for joint treasury operations
- **ens-kitchen/**: ENS kitchen - manages ENS DAO financial data and reporting

## Data Models

The package follows a structured data model for portfolio reporting:

1. **Balances**: Asset balances in underlying denomination units
2. **Transactions**: All balance changes with proper categorization
3. **Prices**: Asset pricing data for valuation calculations
4. **Accounts**: Chart of accounts for portfolio allocation categorization

See `models/README.md` for detailed data architecture documentation.

## Troubleshooting

### Common Issues

1. **API Rate Limits**: If you encounter rate limit errors, increase `RETRY_DELAY` in configuration
2. **Google Sheets Access**: Ensure your service account has proper permissions for the workbook
3. **Dune Query Failures**: Check if the query ID is correct and the query is publicly accessible

### Debug Mode

Enable debug logging by setting environment variables:
```bash
export KPK_DEBUG=1
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.