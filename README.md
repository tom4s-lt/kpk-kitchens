# kpk-kitchens

Repo to contain kpk related helper directories that require code for own projects.

Most scripts are intended to be executable locally & in Google Colab so this means:
1. Scripts are written into Jupyter Notebook files and are self-contained
2. At the top of each ipynb file:
    1. A data directory is created for storing any data (can manage both types of execution)
    2. Required packages are installed by running pip-cmd-style commands at the top of each script inside
    3. Environment variables such as API keys and other sensitive data is included in the in the Config class defined at the top