"""
Setup file for kpk-kitchens package.
"""

from setuptools import setup, find_packages

setup(
    name="kpk_kitchens",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "matplotlib",
        "seaborn",
        "gspread",
        "dune_client",
        "dune_spice",
        "polars",
    ],
    author="Tomas Galizia",
    description="Shared utilities for KPK kitchen notebooks",
    python_requires=">=3.7",
)