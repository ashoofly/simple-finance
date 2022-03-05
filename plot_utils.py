import matplotlib.dates as dates
import matplotlib.pyplot as plt
import json

class DataPlotter:
    def __init__(self):
        with open('positions/ticker_mappings.json') as mappings:
            self.mappings = json.load(mappings)

    def _get_next_bar_loc(self, orig_x):
        bar_width = 5
        return [x + bar_width for x in dates.date2num(orig_x)]

    def _get_title(self, ticker, additional_text):
        full_name = [fund for fund in self.mappings if fund['ticker'] == ticker][0]['name']
        return f'{full_name} ({ticker.upper()}) {additional_text}'

    def draw(self, df, ticker, additional_text=""):
        # set up chart
        fig, ax = plt.subplots()
        plt.title(self._get_title(ticker, additional_text))
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (US$)")

        # format x-axis
        ax.xaxis_date()
        ax.xaxis.set_major_locator(dates.MonthLocator())
        month_format = dates.DateFormatter('%b %y')
        ax.xaxis.set_major_formatter(month_format)

        # plot data
        values_x_loc = self._get_next_bar_loc(df.index)
        contributions = ax.bar(df.index, df['Total Contrib'], 5, color="blue", label="Total Contribution", linewidth=0)
        value = ax.bar(values_x_loc, df['Total Value'], 5, color="orange", label="Total Value", linewidth=0)

        ax.legend()

        # show plot
        fig.autofmt_xdate()
        plt.show()