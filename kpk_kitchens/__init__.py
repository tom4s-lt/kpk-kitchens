"""
KPK Kitchens package for shared functionality across different kitchen notebooks.
"""

__version__ = "0.1.0"

# Import main components for easier access - Config not included
from .utils import (
    # API functions
    etl_gen_df_from_gsheet,
    gecko_get_price_historical,
    spice_query_id,
    # Data processing
    ann_risk_return_252,  # still not used - have to work on it
    ann_risk_return_365,  # still not used - have to work on it
)