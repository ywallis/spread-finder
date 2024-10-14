import ccxt
import time

from calculate_spread import calculate_spread
from find_joint_tickers import find_joint_tickers


if __name__ == '__main__':

    # Initializing clients

    hl_exchange = ccxt.gate()
    mexc = ccxt.mexc()
    bitget = ccxt.bitget()
    bitmart = ccxt.bitmart()
    htx = ccxt.htx()
    kraken = ccxt.kraken()
    cdc = ccxt.cryptocom()

    # Tuple is a quick and dirty way to represent fees.

    ll_exchanges = [(mexc, 0.2), (bitget, 0.3), (bitmart, 0.4), (htx, 0.3), (kraken, 0.4), (cdc, 0.3)]



    # Look at spread

    looping = True

    while looping:

        for exchange in ll_exchanges:

            joint_tickers = find_joint_tickers(hl_exchange, exchange[0])

            try:
                calculate_spread(hl_exchange, exchange[0], joint_tickers, exchange[1])
            except ccxt.NetworkError:
                print('Core loop network error')
            finally:
                time.sleep(10)

        time.sleep(300)
