# Steps

## Pre-Reqs to get up-to-date data
1. Check `positions/fidelity_brokerage.json` is updated with latest transactions. (This was created manually b/c Fidelity doesn't even have a CSV download option.)
2. Need to download the latest csv from Vanguard, clean format, and save in `positions/vanguard_brokerage.json`.
3. Download your 401k transaction history in CSV format from the Fidelity site: https://workplaceservices.fidelity.com/mybenefits/savings2/navigation/dc/History. You can specify the time range you want.
4. Ally should be OK b/c we will be pulling live from API. 

## API keys needed

1. Sign up for Tiingo account and get an API key: https://api.tiingo.com/documentation/end-of-day.
2. Ally API key.

## Logging 
I'm logging all Tiingo API calls since I'm on the free version and there are these limits:

Unique Symbols per Month 500
Max Requests Per Hour 50
Max Requests Per Day 1000
Max Bandwidth Per Month 1 GB

## TODO
* Add schema for
  * fidelity.json
  * ticker_mappings.json
  * fidelity_retirement.csv
  * vanguard.csv
* Blur out y-axis of charts and post examples

## Next
1. Ally climate
2. Vanguard climate
3. Add all climate funds together
4. Index funds
5. Tesla
6. Zoom
8. Each individual fund
9. All funds together
10. 