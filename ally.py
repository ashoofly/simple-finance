#!/usr/bin/env python

import json
import pandas as pd
from pandas_utils import DFBuilder
from plot_utils import DataPlotter

class Ally:
    def __init__(self):
        with open('positions/ally_holdings.json') as holdings:
            self.holdings = json.load(holdings)
        with open('positions/ally_history.json') as history:
            self.history = json.load(history)

    def get_holdings(self):
        holdings = [holding['instrument']['sym'] for holding in self.holdings['response']['accountholdings']['holding']]
        return holdings

    def get_history(self, sym):
        transactions = [entry for entry in
                self.history['response']['transactions']['transaction']
                if entry['transaction']['security']['sym'] == sym]
        print(len(transactions))
        return transactions

    def convert_to_df(self, sym):
        transactions = a.get_history(sym)
        relevant_data = [(transaction['date'][:10], abs(float(transaction['amount'])), float(transaction['transaction']['quantity'])) for transaction in transactions]
        df = pd.DataFrame(relevant_data, columns=['Date', 'Cost Basis', 'Shares'])
        print(df)
        df = DFBuilder(df)\
            .convert_to_datetime('Date')\
            .group_rows_by_month('Date')\
            .fill_in_missing_months()\
            .get_total_contrib_shares_columns('Cost Basis', 'Shares')\
            .get_total_value_column(sym)\
            .build()
        print(df)
        DataPlotter().draw(df, sym.lower(), " - Ally")


if __name__ == "__main__":
    a = Ally()
    print(a.get_holdings())
    #print(json.dumps(a.get_history('GOOG'), indent=2))
    #print(json.dumps(a.get_history('QCLN'), indent=2))
    print(a.convert_to_df('TSLA'))
    #print(json.dumps(a.get_history('TSLA'), indent=2))
    #print(json.dumps(a.get_history('ZM'), indent=2))