"""
Configuration classes for kitchen notebooks.
"""

from datetime import datetime
from typing import Dict, Any

class BaseConfig:
    """Base configuration class containing shared settings."""
    
    # ==============================================
    #  API Configs
    # ==============================================

    # API Keys
    COINGECKO_API_KEY: str = 'CG-jN5KXD1QFHacbpJb3T7PVJ3P'
    DUNE_API_KEY: str = 'RyXNIYLH4uE5NeEjLWQBZEcrkjTRw2EH'

    # API Endpoints
    COINGECKO_API_BASE_URL: str = "https://api.coingecko.com/api/v3"
        
    # API Request Settings
    MAX_RETRIES: int = 3
    DEFAULT_TIMEOUT: int = 10
    RETRY_DELAY: int = 5

    # ==============================================
    #  Directories
    # ==============================================

    # File Paths and Directories
    DATA_DIR: str = "./data"

    # ==============================================
    # Variables & Constants
    # ==============================================


class JTConfig(BaseConfig):
    """Configuration specific to JT Kitchen."""

    # ==============================================
    #  Directories
    # ==============================================
    
    # jt_kitchen sheet
    WORKBOOK_URL: str = "https://docs.google.com/spreadsheets/d/1mIQTla9L7l3FBh1k8xtpHQwHMN4D7nHl1u5nsdeWdA0/"
    LK_ASSETS: str = 'lk_assets'
    SN_PRICES: str = 'prices.csv'
    
    # ==============================================
    # Variables & Constants
    # ==============================================

    # Important Dates
    TTE_DATE: str = "2024-04-23"
    ETL_NOW: datetime = datetime.now()
    
    # Token Configurations
    PORTFOLIO_TOKENS: Dict[str, Dict[str, Any]] = {
        'coingecko_id': {
            # Stablecoins
            'dai': 'dai',
            'xdai': 'xdai',
            'usdc': 'usd-coin',
            'usdt': 'tether',
            # ETH
            'eth': 'ethereum',
            # SAFE & GNO
            'safe': 'safe',
            'gno': 'gnosis',
            # Other Tokens
            'aura': 'aura-finance',
            'bal': 'balancer'
        },
        'asset_class': {
            'dai': 'stablecoins',
            'xdai': 'stablecoins',
            'usdc': 'stablecoins',
            'usdt': 'stablecoins',
            'eth': 'eth',
            'weth': 'eth',
            'safe': 'safe',
            'gno': 'gno',
            'aura': 'other',
            'bal': 'other'
        },
        'similar_tokens': {  # Coingecko ID for similar tokens (to compare market data)
            'safe': 'safe',
            'gno': 'gnosis',
            'eth': 'ethereum',
            'uni': 'uniswap',
            'link': 'chainlink',
            'grt': 'the-graph'
        },
        'token_class': {  # mapper from token to asset for matching with current price
            'SAFE': 'safe',
            'GNO': 'gno',
            'WETH': 'eth',
            'USDC': 'usdc'
        }
    }
    
    # Token Address Mappings
    TOKEN_ADDRESSES: Dict[str, str] = {
        '0X5AFE3855358E112B5647B952709E6165E1C1EEEE': 'SAFE',  # Ethereum
        '0X4D18815D14FE5C3304E87B3FA18318BAA5C23820': 'SAFE',  # Gnosis
        '0XC02AAA39B223FE8D0A0E5C4F27EAD9083C756CC2': 'ETH',  # Ethereum WETH
        '0X9C58BACC331C9AA871AFD802DB6379A98E80CEDB': 'GNO',  # Gnosis
        '0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48': 'USDC',  # Ethereum
        '0X5AFE3855358E112B5647B952709E6165E1C1EEEE-0XC02AAA39B223FE8D0A0E5C4F27EAD9083C756CC2': 'SAFE-ETH',  # Ethereum
        '0X5AFE3855358E112B5647B952709E6165E1C1EEEE-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48': 'SAFE-USDC',  # Ethereum
        '0X4D18815D14FE5C3304E87B3FA18318BAA5C23820-0X9C58BACC331C9AA871AFD802DB6379A98E80CEDB': 'SAFE-GNO'  # Gnosis
    }

class ENSConfig(BaseConfig):
    """Configuration specific to ENS Kitchen."""

    # ==============================================
    #  Directories
    # ==============================================
    
    # ens_kitchen sheet
    WORKBOOK_URL: str = "https://docs.google.com/spreadsheets/d/1ml4EVLU6N7sv6R0Q102YOTwTPmStG64HlJ10aOkjIhY"
    LK_ASSETS: str = 'lk_assets'
    TR_TT: str = 'tr_tt'

    # Paths
    PRICES_CSV: str = 'prices.csv'