import pandas as pd
from tiingo_client import TiingoClient


class DFBuilder:
    def __init__(self, df):
        self.df = df

    def build(self):
        return self.df

    def convert_to_datetime(self, column):
        self.df[column] = pd.to_datetime(self.df[column])
        return self

    def group_rows_by_month(self, date_column):
        self.df = self.df.groupby(pd.Grouper(key=date_column, freq='M')).sum()
        return self

    def convert_str_to_numeric(self, column):
        self.df[column] = pd.to_numeric(self.df[column].str.replace(',',''))
        return self

    def fill_in_missing_months(self):
        self.df = self.df.reindex(pd.date_range(self.df.index[0], pd.to_datetime('now'), freq='M'), fill_value=0.0)
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
