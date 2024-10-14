from datetime import datetime
import pandas as pd
import os

def calculate_spread(hl_exchange, ll_exchange, joint_tickers, spread_threshold):

    hi_spread_tokens = []

    hl_tickers = hl_exchange.fetch_tickers()
    ll_tickers = ll_exchange.fetch_tickers()

    now = datetime.now()
    # Initialize data structure to export to csv via pandas
    data_header = ['Time', 'Pair', 'Exchanges', 'HL_Spread', 'LL_Spread', 'Spread_Differential', 'HL_Volume', 'LL_Volume']
    data = []

    for ticker in joint_tickers:

        hl_ask = hl_tickers[ticker]['ask']
        hl_bid = hl_tickers[ticker]['bid']
        ll_ask = ll_tickers[ticker]['ask']
        ll_bid = ll_tickers[ticker]['bid']

        hl_spread = ((hl_ask - hl_bid) / hl_ask) * 100
        ll_spread = ((ll_ask - ll_bid) / ll_ask) * 100

        # Compare size of spread

        if ll_spread - hl_spread > spread_threshold:
            hi_spread_tokens.append(ticker)
            hl_volume = hl_tickers[ticker]['quoteVolume']
            ll_volume = ll_tickers[ticker]['quoteVolume']
            # print(ticker)
            # print(f'Spread on {hl_exchange.name} = {hl_spread}')
            # print(f'Quote volume on {hl_exchange.name} = {hl_volume}')
            # print(f'Quote volume on {hl_exchange.name} = {ll_volume}')
            # print(f'Spread on {ll_exchange.name} = {ll_spread}')

            ticker_data = [now, ticker, ll_exchange.name, hl_spread, ll_spread, (ll_spread - hl_spread), hl_volume, ll_volume]
            data.append(ticker_data)


    # print(hi_spread_tokens)
    print(f'Found {len(hi_spread_tokens)} pairs with a spread differential of over {spread_threshold} on {ll_exchange.name}.')

    df = pd.DataFrame(data, columns=data_header)
    # print(df)
    output_path = 'export.csv'
    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
    print('Exported data to CSV file.')

    return hi_spread_tokens