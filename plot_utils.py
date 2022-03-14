import matplotlib.dates as dates
import matplotlib.pyplot as plt
import json
from functools import reduce
from pandas_utils import DFBuilder
import locale

bar_colors = [
    "blue",
    "orange",
    "purple",
    "green",
    "#DC148A"
]

class DataPlotter:
    def __init__(self):
        with open('positions/ticker_mappings.json') as mappings:
            self.mappings = json.load(mappings)
        self.fig, self.ax = plt.subplots()
        locale.setlocale(locale.LC_ALL, 'en_US')


    def _get_next_bar_loc(self, orig_x):
        bar_width = 5
        return [x + bar_width for x in dates.date2num(orig_x)]

    def _get_single_ticker_title(self, ticker, additional_text):
        full_name = [fund for fund in self.mappings if fund['ticker'] == ticker][0]['name']
        return f'{full_name} ({ticker.upper()}) {additional_text}'

    def _get_contrib_label(self, ticker):
        if ticker == 'ping':
            return 'Vested RSU'
        else:
            return 'Total Contribution'

    def _setup_chart(self, is_single=False, main_text='', subtext='', xlabel='Month', ylabel='Amount (US$)'):
        # set up chart
        if is_single:
            plt.title(self._get_single_ticker_title(main_text, subtext))
        else:
            plt.title(main_text)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        # format x-axis
        self.ax.xaxis_date()
        self.ax.xaxis.set_major_locator(dates.MonthLocator())
        month_format = dates.DateFormatter('%b %y')
        self.ax.xaxis.set_major_formatter(month_format)

    def _show_plot(self):
        self.ax.legend()

        # show plot
        self.fig.autofmt_xdate()
        plt.show()

    def draw_single_ticker(self, df, ticker, additional_text=""):
        self._setup_chart(True, ticker, additional_text)

        # plot data
        values_x_loc = self._get_next_bar_loc(df.index)
        contributions = self.ax.bar(df.index, df['Total Contrib'], 5, color="blue", label=self._get_contrib_label(ticker), linewidth=0)
        value = self.ax.bar(values_x_loc, df['Total Value'], 5, color="orange", label="Total Value", linewidth=0)

        self._show_plot()

    def draw_multiple_tickers(self, dataframes, title):
        self._setup_chart(False, title)
        start_month = min(reduce(lambda a, b: a + b, [list(df.index) for ticker, df in dataframes.items()]))
        final_dfs = {}
        for ticker, df in dataframes.items():
            final_dfs[ticker] = DFBuilder(df).fill_in_missing_months(start_month).build()
        i = 0
        contribs = []
        values = []
        for ticker, df in final_dfs.items():
            values_x_loc = self._get_next_bar_loc(df.index)
            if i == 0:
                self.ax.bar(df.index, df['Total Contrib'], 5, color='blue',
                                            label=ticker, linewidth=0, edgecolor='black')
                self.ax.bar(values_x_loc, df['Total Value'], 5, color='orange', linewidth=0, edgecolor='black')
            elif i == 1:
                self.ax.bar(df.index, df['Total Contrib'], 5, color='blue',
                            label=ticker, linewidth=0, edgecolor='black', bottom=contribs[0])
                self.ax.bar(values_x_loc, df['Total Value'], 5, color='orange',
                            linewidth=0, edgecolor='black', bottom=values[0])
            else:
                self.ax.bar(df.index, df['Total Contrib'], 5, color='blue',
                            label=ticker, linewidth=0, edgecolor='black', bottom=[sum(y) for y in zip(*contribs)])
                self.ax.bar(values_x_loc, df['Total Value'], 5, color='orange',
                            linewidth=0, edgecolor='black', bottom=[sum(y) for y in zip(*values)])
            contribs.append(df['Total Contrib'].tolist())
            values.append(df['Total Value'].tolist())
            i += 1
        self._show_plot()
        current_total_value = [sum(y) for y in zip(*values)][-1]
        return current_total_value

    def draw_all_tickers(self, dataframes, title):
        self._setup_chart(False, title)
        start_month = min(reduce(lambda a, b: a + b, [list(df.index) for ticker, df in dataframes.items()]))
        final_dfs = {}
        for ticker, df in dataframes.items():
            final_dfs[ticker] = DFBuilder(df).fill_in_missing_months(start_month).build()
        i = 0
        contribs = []
        values = []
        for ticker, df in final_dfs.items():
            values_x_loc = self._get_next_bar_loc(df.index)
            if i == 0:
                self.ax.bar(df.index, df['Total Contrib'], 5, color='blue',
                                            linewidth=0, edgecolor='black')
                self.ax.bar(values_x_loc, df['Total Value'], 5, color='orange', linewidth=0, edgecolor='black')
            elif i == 1:
                self.ax.bar(df.index, df['Total Contrib'], 5, color='blue',
                            linewidth=0, edgecolor='black', bottom=contribs[0])
                self.ax.bar(values_x_loc, df['Total Value'], 5, color='orange',
                            linewidth=0, edgecolor='black', bottom=values[0])
            else:
                self.ax.bar(df.index, df['Total Contrib'], 5, color='blue',
                            linewidth=0, edgecolor='black', bottom=[sum(y) for y in zip(*contribs)])
                self.ax.bar(values_x_loc, df['Total Value'], 5, color='orange',
                            linewidth=0, edgecolor='black', bottom=[sum(y) for y in zip(*values)])
            contribs.append(df['Total Contrib'].tolist())
            values.append(df['Total Value'].tolist())
            i += 1
        # List statistics
        current_total_contrib = [sum(y) for y in zip(*contribs)][-1]
        current_total_value = [sum(y) for y in zip(*values)][-1]
        current_net_gain = current_total_value - current_total_contrib
        percent_net_gain = current_net_gain / current_total_contrib
        print(f'Current Total Contributions: {locale.currency(current_total_contrib, grouping=True)}')
        print(f'Current Total Value: {locale.currency(current_total_value, grouping=True)}')
        print(f'Total Current Gain: {locale.currency(current_net_gain, grouping=True)}')
        print(f'Total Percent Gain: {"{:.0%}".format(percent_net_gain)}')
        self._show_plot()

    def compare_tags(self, dataframes, title):
        self._setup_chart(False, title, ylabel='Percent Gain')
        i = 0
        for tag, df in dataframes.items():
            values_x_loc = self._get_next_bar_loc(df.index)
            if i == 0:
                self.ax.bar(df.index, df['Percent Gain'], 5, color=bar_colors[i], label=tag)
            else:
                self.ax.bar(values_x_loc, df['Percent Gain'], 5, color=bar_colors[i], label=tag)
            i += 1
        self._show_plot()