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

# Use utility functions
from kpk_kitchens.utils import fetch_data_with_retries

data = fetch_data_with_retries(
    endpoint=JTConfig.COINGECKO_PRICE_ENDPOINT,
    params={'x_cg_demo_api_key': JTConfig.COINGECKO_API_KEY},
    max_retries=JTConfig.MAX_RETRIES,
    timeout=JTConfig.DEFAULT_TIMEOUT,
    retry_delay=JTConfig.RETRY_DELAY
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

See `models/README.md` for detailed data architecture documentation.

## Troubleshooting

### Common Issues

1. **API Rate Limits**: If you encounter rate limit errors, increase `RETRY_DELAY` in configuration
2. **Google Sheets Access**: Ensure your service account has proper permissions for the workbook
3. **Dune Query Failures**: Check if the query ID is correct and the query is publicly accessible