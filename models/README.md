# models

Model description & data architecture.

## overview

In order to produce proper portfolio reporting, the following data is required:
1. **Balances:** expressed in the desired denomination unit (but preferably in terms of the underlying asset).
2. **Transactions:** every change in balances (same balance denomination unit as the balances above) that is undergone by the portfolio.
3. **Prices:** to express data in the desired accounting currency used (and be able to calculate M2M results, etc).

There are two ways the underlying data can be used for performance & other metrics calculation:
1. By having balance snapshots and calculating differences + explanation of variations with transactions.
2. By having transactions be comprehensive and cover every different kind of variation type the portfolio could have, and building balances by aggregating transactions.

## data models

The three pieces of information above have to be organized in a certain way to be able to produce coherent reporting. With some added things.

- **accounts**: index of all existing financial accounts (allocations of the portfolio) that's used to cateogrize and aggregate individual allocation balances. Usually done in a chart of accounts.
- **transactions:** as explained above - desirably would have the following:
    1. **account:** signals the account (identified above) that's impacted in that transaction.
    2. **tx type/action:** identifies the type of transaction that's happening (swaps, fee, yield, m2m, etc).
    3. **directionality:** either using positive/negative amounts or by signalling in/out or whatever other way of doing it.
    4. **asset/underlying:** identifty the asset involved in the transaction.
- **balances:** amount of notional in each account (+ price information -> valuation in that price).
- **prices:** per asset/underlying, depending on the details of the system being used.