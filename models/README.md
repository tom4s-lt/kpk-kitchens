# models

Model description & data architecture in order to build a report that looks like the [ENS Endowment Weekly Report](https://lookerstudio.google.com/reporting/455e7884-3a66-4dff-97cf-74cb9c1de98a)

## building blocks

### policies

There are certain rules that will be enforced for reporting and need to be identified first:

1. **Accounting period**: refering to the minimum time granularity of the data being recorded.
2. **Base currency**: currency in which reporting will be denominated.
3. **Special rules for asset treatment**: 
    1. **Base asset equivalence**: e.g. how to treat stablecoins (if price fixed at $1, if equal to each other, etc)
    2. **Non-base asset pricing**: pricing time & price source - and discrepancies that non-continuous pricing could create.
    3. **Special asset treatment**: e.g. own stock/token or any other specific things.
    4. **Any other topics worth mentioning**

Though with a different objective, there are a lot of similarities between how regular accounting. What changes is the specifics of the models used, but in general we want to build the "financial statements but for a portfolio" plus additional investing specific metrics.

### data

In order to create a good portfolio report, the following concepts have to be considered:

1. **Accounts**: index of all existing financial accounts (that are derived from the portfolio asset allocation categories) that's used to cateogrize and aggregate individual allocation balances. Usually done using a chart of accounts.
2. **Transactions**: every change in balance (measured in the underlying/base unit for each account) properly linked to an account.
2. **Balances**: expressed in the desired denomination unit (but preferably in terms of the underlying asset).
4. **Prices**: to express data in the desired accounting currency used (and be able to calculate M2M results, etc).

There are two ways in which these building blocks can be used to product a report and properly atrtibute variations & calculate metrics:

1. By having balance snapshots and calculating differences + explanation of variations with transactions.
2. By having transactions be comprehensive and cover every different kind of variation type the portfolio could have, and building balances by aggregating transactions.

## entities

Depending on the reporting design, the entities and models listed below will be different but at a bare minimum, the ideal to be able to construct the building blocks listed above would look something like the following:

### accounts (chart of accounts)

Used to categorize all allocations of the portfolio.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `account` | int | [PK] Unique identifier for the account |
| `account_label` | str | Descriptive name for the account |
| `account_description` | str | Description of the account |
| `account_level` | int | Level of the account (how many categories it has above) |
| `is_active` | bool | Whether the account is currently (being used by asset manager) |
| `account_allocation` | str | Related to strategies that generate other tokens also - measures which allocation is the account a result of... |
| `account_level_n` | str | Complete for each account until the lower level to signal the hierarchy and be able to aggregate data for reporting |

#### notes

- Possible improvments:
    - Include option to check wthere it's included in the permissions for that specific client (in order to know the complete universe of investable assets).
- Generalization:
    - Not entirely sure how this would be generalized to more than one client, there are categories that depend on the specific client (GNO token would be GNO for Gnosis DAO but Other token for ENS DAO).

### addresses

Mapping of all addresses that belong to a specific client.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `label` | str | Label from source (can be etherscan or whichever source used to gather address) |
| `name` | str | Name for the address - to show desired name |
| `entity` | str | Owner or controller of the address |
| `sub_entity` | str | Sub category within the entity for more detail |
| `address` | hex | [PK] Blockchain address |
| `source` | str | Source from where the address was identified |

#### notes

- Possible improvements:
    - Add blockchain (right now it doesn't have it because it's ENS DAO only).
    - Have to idenfity which are treasury or "trackable" wallets.
- Generalization:
    - Add two attributes: `client/dao` & `blockchain` in order to include every possible address.

### assets

Mapping of all assets that are tracked in the portfolio/s.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `symbol` | str | asset symbol (not sure where the ultimate source of truth for this is) - has to coincide with tx symbol or contract_address |
| `name` | str | Name of the asset (e.g. COMP -> Compound Finance) |
| `type_level` | int | Signals the asset level, the underlying type of the token (explained below) |
| `symbol_level_0` | str | Level 0 symbol of the `symbol` |
| `company` | str | Which company is the asset being mapped for (could be named `client`/`dao`) |
| `symbol_level_0` | str | Level 0 symbol of the `symbol` |
| `allocation` | str | Denotes the market exposure which might not be explicit in the chart of accounts (and asset classes). This allows to show custom asset classes while still being compliant with more accounting-focused asset classes |
| `type_market` | str | Market exposure of the token `cash`/`fixed`/`variable` |
| `type_income` | str | distinction between `rebasing`/`reward-bearing` - mostly important because transactions and balances are shown in the underlying assets so they should be converted using a rate |
| `id_gecko` | str | Coingecko ID for the asset (for price search) |
| `blockchain` | str | blockchain in which the asset lives (same asset in different blockchain is considered different) |
| `contract_address` | hex | Address of the token contract |

#### notes

- `type_level` and `symbol_level_0` explained:
    - `type_level` is a property that expresses the amount of "underlyings" and "wraps" and asset has vs. the original representation of the underlying (e.g. aEthWETH is level `1` because it contains WETH inside that token, and an LP token would be level `2` because it contains wrapped tokens and has several underlyings). A base asset would have level `0`.
    - `symbol_level_0` is the underlying asset mentioned above.
- Possible improvements:
    - Eventually assets can have a related position to double-check that in the case of transactions that involve them (but they might not coincide with the actual transaction)
- Generalization:
    - No need to add anything else since already the assets and thus the allocation which they represent will be dependent on the `company` identified.

___

To do from here

___


### balances

- **balances:** amount of notional in each account (+ price information -> valuation in that price).

### prices

- **prices:** per asset/underlying, depending on the details of the system being used.

### transactions

address
blockchain
company

- **transactions:** as explained above - desirably would have the following:
    1. **account:** signals the account (identified above) that's impacted in that transaction.
    2. **tx type/action:** identifies the type of transaction that's happening (swaps, fee, yield, m2m, etc).
    3. **directionality:** either using positive/negative amounts or by signalling in/out or whatever other way of doing it.
    4. **asset/underlying:** identifty the asset involved in the transaction.

### account<>transactions adapter

1. This could take two forms:
    1. Transactions already include they account so that they are automatically linked to an account via chart of accounts id for example
    2. Transactions don’t include the same metadata as the accounts - so you need a way to link them together and build balances and results based on the chart of accounts
        - This is done right now by adding metadata in the ops app + the csv export you get from there

# refs

- https://api-docs.octav.fi/api-models/transaction
- https://api-docs.octav.fi/additional-informations/transaction-type
- [ENS Accounting (SF)](https://docs.google.com/document/d/1xS4nXx1G0QCjFS-VdG5yVmVoMa5t1q9_dFZ9N4wGSJ8/edit?usp=sharing)
- https://aave.tokenlogic.xyz/treasury
- https://dune.com/steakhouse/ens-steakhouse