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

Though with a different objective, there are a lot of similarities with regular accounting. What changes is the specifics of the models used, but in general we want to build the "financial statements but for a portfolio" plus additional investing specific metrics.

### data

In order to create a good portfolio report, the following concepts have to be considered:

1. **Accounts**: index of all existing financial accounts (that are derived from the portfolio asset allocation categories) that's used to cateogrize and aggregate individual allocation balances. Usually done using a chart of accounts.
2. **Transactions**: every change in balance (measured in the underlying/base unit for each account) properly linked to an account.
2. **Balances**: expressed in the desired denomination unit (but preferably in terms of the underlying asset).
4. **Prices**: to express data in the desired accounting currency used (and be able to calculate M2M results, etc).

There are two ways in which these building blocks can be used to product a report and properly atrtibute variations and calculate metrics:

1. By having balance snapshots and calculating differences + explanation of variations with transactions.
2. By having transactions be comprehensive and cover every different kind of variation type the portfolio could have, and building balances by aggregating transactions.

## entities

Depending on the reporting design, the entities and models listed below will be different but at a bare minimum, the ideal to be able to construct the building blocks listed above would look something like the following (this is taken from the current ENS DAO reporting data):

### accounts (chart of accounts)

Used to categorize all allocations of the portfolio.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| *Non-vital metadata* |
| `protocol` | int | Name of the protocol |
| `position` | int | Name of the position |
| `symbol` | int | Symbol of the account as explained below |
| `account_allocation` | str | Related to strategies that generate other tokens also - measures which allocation is the account a result of... |
| `is_active` | bool | Whether the account is currently (being used by asset manager) |
| *Vital atributes* |
| `account` | int | [PK] Unique identifier for the account |
| `account_label` | str | Descriptive name for the account |
| `account_description` | str | Description of the account |
| `account_level` | int | Level of the account (how many categories it has above) |
| `account_level_n` | str | Complete for each account until the lower level to signal the hierarchy and be able to aggregate data for reporting |

#### notes

- Clarifications:
    - Each allocation (account) should be drilled down until the symbol (actual token being held) represents only one asset/has single price exposure. this is done in order to assign a single `symbol_level_0` to each of the balances being tracked (and then be able to decompose the portfolio into the base assets). It's also useful to index transactions that creats inflows/outflows from strategies.
    - Unclaimed rewards is a particular allocation - does not respond to general rules and has to be treated invididually.
- Possible improvments:
    - Include option to check wthere it's included in the permissions for that specific client (in order to know the complete universe of investable assets).
- Generalization:
    - Not entirely sure how this would be generalized to more than one client, there are categories that depend on the specific client (GNO token would be GNO for Gnosis DAO but Other token for ENS DAO).

### addresses

Mapping of all addresses that belong to a specific client.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `label` | str | Label from source (can be etherscan or whichever source used to gather address) |
| `name` | str | Name for the address - to show desired name |
| `entity` | str | Owner or controller of the address |
| `sub_entity` | str | Sub category within the entity for more detail |
| `address` | hex | [PK] Blockchain address |
| `blockchain` | hex | blockchain in which the address exists |
| `creation_block` | int | block at which address was created |
| `source` | str | Source from where the address was identified |

#### notes

- Possible improvements:
    - Have to idenfity which are treasury or "trackable" wallets.
- Generalization:
    - Add `client`/`dao`/`company` to differentiate between them

### assets

Mapping of all assets that are tracked in the portfolio/s.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `symbol` | str | asset symbol (not sure where the ultimate source of truth for this is) - has to coincide with tx symbol or contract_address |
| `name` | str | Name of the asset (e.g. COMP -> Compound Finance) |
| `type_level` | int | Signals the type of underlying of the token (explained below) |
| `symbol_level_0` | str | Level 0 symbol of the `symbol` |
| `company` | str | Which company is the asset being mapped for (could be named `client`/`dao`) |
| `allocation` | str | Denotes the market exposure which might not be explicit in the chart of accounts (and asset classes). This allows to show custom asset classes while still being compliant with more accounting-focused asset classes |
| `type_market` | str | Market exposure of the token `cash`/`fixed`/`variable` |
| `type_income` | str | distinction between `rebasing`/`reward-bearing` - mostly important because transactions and balances are shown in the underlying assets so they should be converted using a rate |
| `id_gecko` | str | Coingecko ID for the asset (for price search) |
| `blockchain` | str | blockchain in which the asset lives (same asset in different blockchain is considered different) |
| `contract_address` | hex | Address of the token contract |

#### notes

- Clarifications:
    - `symbol` - right now is the symbol as identified in the data warehouse & ops app - it generally is the higher level representation of the asset (the one that is transfered and held and symbolizes the strategy)
	- `type_level` - property that expreses the type of "underlying" or "wraps" that a token has vs. the original representation (e.g. aEthWETH is level `1` because it contains WETH inside that token, representing only one asset, and an LP token would be level `2` because it contains wrapped tokens and has several underlyings). A base asset would have level `0`.
    - `symbol_level_0` is the underlying base asset mentioned above.
- Possible improvements:
    - Eventually assets can have a related position to double-check that in the case of transactions that involve them (but they might not coincide with the actual transaction)
    - Would eventually need more properties to work as a dimension table.
- Generalization:
    - No need to add anything else since already the assets and thus the allocation which they represent will be dependent on the `company` identified.

### transactions

Every transfer that involves an address related to the treasury. Right now this doesn't reflect the ideal scenario but rather the current setup using Ops App export through Looker Studio.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `company` | str | company name |
| `address` | str/hex | address label or address of the treasury being tracked |
| `blockchain` | str | name of the blockchain |
| `datetime` | timestamp | date & time in which the tx happened |
| `tx hash` | str | tx hash of the transaction |
| `address_from` | hex | sender |
| `address_to` | hex | receiver |
| `token_symbol` | str | token symbol |
| `token_address` | hex | token address |
| `token_amount` | float | amount of tokens transfered |
| `tx type` | str | type of transaction that creates transfer (this is relevant to build attribution of the portfolio variability) |
| `protocol_from_name` | str | protocol from which the token being transferred is sourced |
| `pos_from_name` | str | position (inside the protocol) from which the token being transferred is sourced |
| `protocol_to_name` | str | protocol to which the token being transferred is going |
| `pos_to_name` | str | position (inside the protocol) to which the token being transferred is going |
| `comments` | str | ad hoc comments on the transaction |
| *Additional attributes* to match transactions to accounts and build balances |
| `dir` | int | either `1` for inflows or `-1` for outflows |
| `4_null` | bool | Returns True if the record has 4 nulls (meaning no position attached) - that means only two of them should be included based on the direction of transaction in the custom `protocol_from`/`to` & `position_from`/`to` explained below |
| `protocol_from` | str | This and the 3 below are just to organize so that the to/from attributes make sense to link txs to accounts |
| `position_from` | str | idem |
| `protocol_to` | str | idem |
| `position_to` | str | idem |
| `type_income` | str | link to the `assets`-`type_income` property to signal if it has to be decomposed into the underlying amount |
| `rate` | float | conversion rate to the underlying (this is the most "heavy" part meaning it has to be fetched manually for each date for each asset that is reward bearing) |
| `amount_level_0` | str | notional amount of the underlying asset (for reward-bearing tokens or lp tokens it's the amount of underlying they represent) |

#### notes

- Clarifications:
    - Transactions have to be useful to link all transfers to a specific account denominated in their base asset (i.e. `symbol_level_0`).
    - If the `accounts`, `assets`, `addresses` and `transactions` models are coherent to each other, there's no need to add some of the properties added here (and in the other models as well).
- Improvements:
    - Since the tx export not always asigns transaction to and from (e.g. entering/exiting stETH position through a SWAP and not a DEPOSIT) - you have to manually add Position To/From as if it were done in the ops app
    -  Also for Endowment funding (taken into account in the capital account) & for kpk fees & other particular txs
    - the protocol names have to be the same as the allocation names - once we have everything mapped in a chart of accounts that has standard names we can do a lot more
    - Types of transactions correspond to particular ledgers/variability sources with a correct mapping

### prices

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `date` | str | date (daily prices) |
| `symbol` | str | token symbol (remember we're only pricing `level_0` assets because everything is expressed in those units) |
| `price` | float | expressed in the unit of account - the `base currency` |

#### notes

- Improvements:
    - Add `blockchain` and `token_address`/`contract_address` to the token
    - Eventually fetch prices of tokens that aren't `level_0` for completeness
    - Add `source` used for price
- Generalization:
    - Have to add `blockchain` to the table
    - Maybe other client-specific workings

### balances

Balances are the result of the combination of accounts (asset specific) & transactions (address specific). They map the `specific amount` (of notional of the `symbol_level_0`) of an asset in a `specific address` at a `specific point in time`. The result from the combination of:
- `addresses`
- `accounts`
- `assets`
- `prices` - if you want them denominated in the unit of account.

There are two dimensions that have to be udnerstood:
- Way in which the balance is obtained (already explained [above](#data))
- Way in which transactions are linked into accounts: there needs to be an `accounts<>transactions` adapter or interface which is used to create this coherency between both and create the proper indexing.
    - There are two ways this can be done:
        - That data is included in the `accounts` model
        - The data is included in a specific model which contains the interface between both.
    - No matter which way is chosen, the logic take several different forms:
        - Map the symbols and then when the treasury interact with symbols that are linked to specific accounts the link is formed.
        - Not all accounts involve holding a specific symbol (example DAI in DSR Manager that returns no token) - so the combination of `symbol` & `address` involved in the transfer can be used to create the link with transactions.

# refs

- https://api-docs.octav.fi/api-models/transaction
- https://api-docs.octav.fi/additional-informations/transaction-type
- [ENS Accounting (SF)](https://docs.google.com/document/d/1xS4nXx1G0QCjFS-VdG5yVmVoMa5t1q9_dFZ9N4wGSJ8/edit?usp=sharing)
- https://aave.tokenlogic.xyz/treasury
- https://dune.com/steakhouse/ens-steakhouse