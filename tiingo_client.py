import logging
import os
import json
import requests
import datetime


logging.basicConfig(filename='./logs/tiingo.log', encoding='utf-8', level=logging.INFO)

class TiingoClient:
    def __init__(self, ticker):
        self.ticker = ticker
        self.json_file = f'./historical/{ticker.lower()}.json'
        self.record = self.load_record()
        self.eod_price_url_template = "https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={end_date}"
        self.auth_header = {'Authorization': f'Token {os.getenv("TIINGO_API_KEY")}'}

    def __del__(self):
        print(f"[TiingoClient] Saving historical record to: {self.json_file}")
        self.save_record()

    def load_record(self):
        try:
            with open(self.json_file) as jsonfile:
                return json.load(jsonfile)
        except Exception as e:
            print(f"No historical record found for {self.ticker}.")
            return {}

    def _get_one_week_before(self, date_str):
        """This is necessary b/c apparently sometimes API is missing some dates."""
        end_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        start_date = end_date - datetime.timedelta(days=7)
        return start_date.strftime('%Y-%m-%d')

    def _format_date_str(self, raw_date):
        raw_datetime = datetime.datetime.strptime(raw_date, '%Y-%m-%dT00:00:00.000Z')
        formatted_date = raw_datetime.strftime('%Y-%m-%d')
        return formatted_date

    def _get_month_historical(self, date):
        month_entry = {key: value for key, value in self.record.items() if key.startswith(date[:7])}
        if len(month_entry.values()) == 1:
            print(f"Found historical EOD record for {date[:7]} in cache, not calling Tiingo API.")
            return list(month_entry.values())[0]
        else:
            return None

    def get_closing_price(self, date):
        # check our cache first
        closing_price = self._get_month_historical(date)
        if not closing_price:
            # make actual API call
            path_params = {'ticker': self.ticker.lower(),
                           'start_date': self._get_one_week_before(date),
                           'end_date': date}
            url = self.eod_price_url_template.format(**path_params)
            logging.info(f"GET {url}")
            response = requests.get(url, headers=self.auth_header)
            if response.status_code == 200:
                last_day = response.json()[-1]
                response_date = self._format_date_str(last_day['date'])
                closing_price = last_day['close']
                self.record[response_date] = closing_price
            else:
                print(f'[{response.status_code}] {response.content}')
        return closing_price

    def save_record(self):
        with open(self.json_file, 'w') as jsonfile:
            json.dump(self.record, jsonfile, indent=2)

