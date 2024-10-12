def calculate_spread(hl_exchange, ll_exchange, joint_tickers, spread_threshold):

    hi_spread_tokens = []

    hl_tickers = hl_exchange.fetch_tickers()
    ll_tickers = ll_exchange.fetch_tickers()

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
            print(ticker)
            print(f'Spread on {hl_exchange.name} = {hl_spread}')
            print(f'Quote volume on {hl_exchange.name} = {hl_tickers[ticker]['quoteVolume']}')
            print(f'Spread on {ll_exchange.name} = {ll_spread}')

    print(hi_spread_tokens)
    print(len(hi_spread_tokens))

    return hi_spread_tokens