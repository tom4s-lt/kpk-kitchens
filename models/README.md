# models

Model description & data architecture.

## overview

In order to produce proper portfolio reporting, the following data is required:
1. **Balances:** expressed in the desired denomination unit (but preferably in terms of the underlying asset).
2. **Transactions:** every change in balances that is undergone by the portfolio.
3. **Prices:** to express data in the desired accounting currency used (and be able to calculate M2M results, etc).

There are two ways the underlying data can be used for performance & other metrics calculation:
1. By having balance snapshots and calculating differences + explanation of variations with transactions.
2. By having transactions be comprehensive and cover every different kind of variation type the portfolio could have, and building balances by aggregating transactions.

## data models

The three pieces of information above have to be organized in a certain way to be able to produce coherent reporting.

### accounts (chart of accounts)

An index of all existing financial accounts (allocations of the portfolio) that's used to cateogrize and aggregate individual allocation balances.

### balances

...

### transactions

...

### prices

...

# references

...