import json

# Read the notebook
with open('ens_ips.ipynb', 'r') as f:
    notebook = json.load(f)

# Find the cell with the ETH prices code
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'eth_prices = pd.read_csv' in source:
            # Add the price shifting logic after the CSV reading
            new_source = []
            for line in cell['source']:
                new_source.append(line)
                if 'btc_prices = pd.read_csv' in line:
                    # Add the price shifting code after reading both CSVs
                    new_source.extend([
                        '\n',
                        '# Convert snapped_at to datetime and set as index\n',
                        "eth_prices['snapped_at'] = pd.to_datetime(eth_prices['snapped_at'])\n",
                        "btc_prices['snapped_at'] = pd.to_datetime(btc_prices['snapped_at'])\n",
                        '\n',
                        '# Shift prices by 1 day to convert from open to close prices\n',
                        '# Each date will now show the closing price from the previous day\n',
                        "eth_prices['price'] = eth_prices['price'].shift(-1)\n",
                        "btc_prices['price'] = btc_prices['price'].shift(-1)\n",
                        '\n',
                        '# Remove the last row which will have NaN values after shifting\n',
                        'eth_prices = eth_prices.dropna()\n',
                        'btc_prices = btc_prices.dropna()\n'
                    ])
            
            cell['source'] = new_source
            break

# Write the modified notebook back
with open('ens_ips.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print("Notebook modified successfully!") 