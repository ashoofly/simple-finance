import json
import pandas as pd
from pandas_utils import DFBuilder


class Fidelity:
    def __init__(self):
        self.name = 'fidelity'
        self.additional_title_text = ' - Fidelity'
        with open('positions/fidelity.json') as positions:
            self.positions = json.load(positions)

    def convert_to_df(self, ticker):
        ticker_positions = [position['transactions'] for position in self.positions if position['ticker'] == ticker.upper()][0]
        df = pd.DataFrame(ticker_positions)
        df = DFBuilder(df)\
            .convert_to_datetime('date')\
            .group_rows_by_month('date')\
            .fill_in_missing_months()\
            .get_total_contrib_shares_columns('cost_basis', 'shares')\
            .get_total_value_column(ticker)\
            .build()
        print(df)
        return df
