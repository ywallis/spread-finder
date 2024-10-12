
def find_joint_tickers(hl_exchange, ll_exchange):

    """This function takes in two CCXT clients, and returns a list of tickers matching my MM criteria."""

    # Loading markets

    hl_exchange.load_markets()
    ll_exchange.load_markets()

    # Fetching tickers

    hl_tickers = hl_exchange.fetch_tickers()
    ll_tickers = ll_exchange.fetch_tickers()

    # Checking if pair is active and has futures on HL exchange

    valid_hl_tickers = []

    for ticker in hl_tickers:
        if hl_exchange.markets[ticker]['active']:
            try:
                if hl_exchange.markets[f'{ticker}:USDT']['active']:
                    valid_hl_tickers.append(ticker)
            except KeyError:
                continue
                # print('No futures')


    print(valid_hl_tickers)
    print(f'Found {len(valid_hl_tickers)} valid pairs on {hl_exchange.name}.')

    # Checking if pair is active on LL exchange

    joint_tickers = []

    for ticker in valid_hl_tickers:
        if ticker in ll_tickers:
            if ll_exchange.markets[ticker]['active']:
                joint_tickers.append(ticker)

    print(joint_tickers)
    print(f'Found a total of {len(joint_tickers)} eligible pairs.')

    return  joint_tickers