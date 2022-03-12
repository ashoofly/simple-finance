#!/usr/bin/env python
import pandas as pd
from pandas_utils import DFBuilder


class FidelityRetirementFund:
    def __init__(self):
        self.csv_file = 'positions/fidelity_retirement.csv'
        self.df = pd.read_csv(self.csv_file)
        self.additional_title_text = ' - 401(k)'

    def convert_to_df(self, ticker='fskax'):
        self.df = DFBuilder(self.df)\
            .convert_to_datetime('Date')\
            .convert_str_to_numeric('Amount')\
            .group_rows_by_month('Date')\
            .fill_in_missing_months()\
            .get_total_contrib_shares_columns('Amount', 'Shares/Unit')\
            .get_total_value_column(ticker)\
            .build()
        return self.df
