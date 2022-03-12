#!/usr/bin/env python
import argparse
import sys
import json
from fidelity import Fidelity
from pandas_utils import DFBuilder
from vanguard import Vanguard
from ally import Ally
from plot_utils import DataPlotter
from retirement import FidelityRetirementFund
import pandas as pd
from pandas_utils import DFBuilder


class Finance():
    def __init__(self):
        with open('positions/ticker_mappings.json') as mappings:
            self.mappings = json.load(mappings)
        self.brokerages = [Fidelity(), Ally(), Vanguard()]
        self.retirement = FidelityRetirementFund()

    def choose_brokerage(self, brokerage):
        if brokerage == 'fidelity':
            return Fidelity()
        elif brokerage == 'vanguard':
            return Vanguard()
        elif brokerage == 'ally':
            return Ally()
        elif brokerage == 'fidelity_retirement':
            return FidelityRetirementFund()
        else:
            # TODO: Add error handling
            return None

    def plot_retirement_fund(self):
        df = self.retirement.convert_to_df()
        DataPlotter().draw_single_ticker(df, self.retirement.ticker, self.retirement.additional_title_text)

    def list_funds_with_tag(self, tag):
        print([ticker['ticker'] for ticker in self.mappings if tag in ticker['tags']])
        print([ticker['brokerages'] for ticker in self.mappings if tag in ticker['tags']])

    def get_dataframe_for(self, ticker):
        brokerage_info = [ticker_info for ticker_info in self.mappings if ticker_info['ticker'] == ticker][0][
            'brokerages']
        frames = []
        for brokerage in brokerage_info:
            brokerage_analyzer = self.choose_brokerage(brokerage)
            df = brokerage_analyzer.convert_to_df(ticker)
            frames.append(df)
        if len(frames) > 1:
            result = pd.concat(frames)
            result.index.name = 'Date'
            result = result.groupby('Date')['Total Contrib', 'Total Shares'].sum()
            final_result = DFBuilder(result).get_total_value_column(ticker).build()
            additional_text = brokerage_info
        else:
            final_result = frames[0]
            additional_text = brokerage_info[0]
        return final_result, additional_text

    def plot_historical_performance(self, ticker='', tag=''):
        if ticker:
            dataframe, additional_text = self.get_dataframe_for(ticker)
            DataPlotter().draw_single_ticker(dataframe, ticker, f' - {additional_text}')
        elif tag:
            tickers = [ticker['ticker'] for ticker in self.mappings if tag in ticker['tags']]
            dataframes = {}
            for ticker in tickers:
                dataframe, additional_text = self.get_dataframe_for(ticker)
                dataframes[ticker] = dataframe
            DataPlotter().draw_multiple_tickers(dataframes, f'{tag.capitalize()} Funds')
        else:
            tickers = [ticker['ticker'] for ticker in self.mappings]
            dataframes = {}
            for ticker in tickers:
                dataframe, additional_text = self.get_dataframe_for(ticker)
                dataframes[ticker] = dataframe
            DataPlotter().draw_all_tickers(dataframes, f'All Funds')


if __name__ == '__main__':
    help_description = """
Usage: 
./finance.py list ticker      Lists all available ticker symbols
./finance.py list tags        Lists all available tags
./finance.py list [tag]       Lists all ticker symbols with this tag  

./finance.py [ticker]         Displays progress chart for that ticker
./finance.py                  Defaults to `./finance.py --all`
./finance.py --climate        Displays progress chart for all fossil-free funds  
./finance.py --index          Displays progress chart for all index funds
./finance.py --retirement     Displays progress chart for retirement fund
./finance.py --ss             Displays progress chart for all single stocks
./finance.py --rsu            Displays progress chart for RSUs
"""
    parser = argparse.ArgumentParser(description=help_description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-t', '--ticker', type=str, help='ticker symbol', required=False)
    parser.add_argument('--climate', action='store_true', help='Displays progress chart for all fossil-free funds')
    parser.add_argument('--retirement', action='store_true', help='Displays progress chart for 401(k)')

    if any(option in sys.argv for option in ['-h', '--help']):
        parser.print_help()
        exit(0)

    # TODO: Add error handling
    args = parser.parse_args()
    print(args)

    f = Finance()
    if args.ticker:
        f.plot_historical_performance(ticker=args.ticker)
    if args.climate:
        f.list_funds_with_tag('climate')
        f.plot_historical_performance(tag='climate')
    if args.retirement:
        f.plot_retirement_fund()
    else:
        f.plot_historical_performance()

