# KPK Kitchens

Shared utilities and configuration for KPK kitchen notebooks.

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
!pip install git+https://github.com/your-username/kpk-kitchens.git

# Import the configuration and utilities
from kpk_kitchens.config import JTConfig  # or ENSConfig
from kpk_kitchens.utils import fetch_data_with_retries, etl_gen_df_from_gsheet, process_coingecko_price_data
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

## Project Structure

```
kpk-kitchens/
├── kpk_kitchens/
│   ├── __init__.py
│   ├── config.py      # Configuration classes
│   └── utils.py       # Utility functions
├── setup.py           # Package installation
└── README.md         # This file
```

## Kitchens

- `jt-kitchen/`: Joint Treasury kitchen
- `ens-kitchen/`: ENS kitchen