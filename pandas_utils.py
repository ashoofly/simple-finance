import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from tiingo_client import TiingoClient


class DFBuilder:
    def __init__(self, df):
        self.df = df

    def build(self):
        return self.df

    def filter_rows_by_column_value(self, col_name, col_value):
        self.df = self.df[self.df[col_name] == col_value]
        return self

    def filter_rows_by_condition(self):
        self.df = self.df[pd.to_numeric(self.df['Quantity'], errors='coerce')]
        return self

    def choose_relevant_cols_for_df(self, col_names):
        self.df = self.df[col_names]
        return self

    def convert_to_datetime(self, column):
        self.df[column] = pd.to_datetime(self.df[column])
        return self

    def convert_to_numeric_or_else_drop(self, column):
        self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
        self.df = self.df.dropna()
        return self

    def group_rows_by_month(self, date_column):
        self.df = self.df.groupby(pd.Grouper(key=date_column, freq='M')).sum()
        return self

    def convert_str_to_numeric(self, column):
        self.df[column] = self.df[column].str.replace(',','')
        self.df[column] = self.df[column].str.replace('$','')
        self.df[column] = pd.to_numeric(self.df[column])
        return self

    def take_abs_value(self, column):
        self.df[column] = abs(self.df[column])
        return self

    def fill_in_missing_months(self, start_month=''):
        if not start_month:
            start_month = self.df.index[0]
        self.df = self.df.reindex(pd.date_range(start_month, pd.to_datetime('now'), freq='M'), fill_value=0.0)
        return self

    def get_total_contrib_shares_columns(self, contrib, shares):
        self.df['Total Contrib'] = self.df[contrib].cumsum()
        self.df['Total Shares'] = self.df[shares].cumsum()
        self.df = self.df[["Total Contrib", "Total Shares"]]
        return self

    def get_total_value_column(self, ticker):
        tiingo_client = TiingoClient(ticker)
        total_value_by_month = []
        for index, row in self.df.iterrows():
            close_date = index.date().strftime("%Y-%m-%d")
            total_shares = row["Total Shares"]
            closing_price = tiingo_client.get_closing_price(close_date)
            total_value = total_shares * closing_price
            total_value_by_month.append(total_value)
        self.df['Total Value'] = total_value_by_month
        return self

    def set_index_name(self, name):
        self.df.index.name = name
        return self