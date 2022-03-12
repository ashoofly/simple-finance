#!/usr/bin/env python

import json
import pandas as pd
from pandas_utils import DFBuilder
from plot_utils import DataPlotter


class Vanguard:
    def __init__(self):
        self.csv_file = 'positions/vanguard-all.csv'
        self.df = pd.read_csv(self.csv_file)
        self.additional_title_text = ' - Vanguard'
        with open('positions/ticker_mappings.json') as mappings:
            self.mappings = json.load(mappings)

    def get_holdings(self):
        holdings = [holding['ticker'] for holding in self.mappings if 'vanguard' in holding['brokerages']]
        return holdings

    def convert_to_df(self, sym):
        self.df = DFBuilder(self.df)\
             .filter_rows_by_column_value('Symbol', sym.upper())\
             .choose_relevant_cols_for_df(['Settlement', 'Symbol', 'Quantity', 'Amount'])\
             .convert_to_datetime('Settlement') \
             .convert_to_numeric_or_else_drop('Quantity') \
             .convert_str_to_numeric('Amount') \
             .take_abs_value('Amount') \
             .group_rows_by_month('Settlement') \
             .fill_in_missing_months() \
             .get_total_contrib_shares_columns('Amount', 'Quantity') \
             .get_total_value_column(sym) \
             .build()
        # print(self.df)
        # DataPlotter().draw_single_ticker(self.df, sym.lower(), " - Vanguard")
        return self.df


if __name__ == "__main__":
    v = Vanguard()
    print(v.get_holdings())
    print(v.convert_to_df('vpl'))