import ccxt
import time

from calculate_spread import calculate_spread
from find_joint_tickers import find_joint_tickers


if __name__ == '__main__':

    # Initializing clients

    hl_exchange = ccxt.gate()
    mexc = ccxt.mexc()
    bitget = ccxt.bitget()
    coinex = ccxt.coinex()
    ll_exchanges = [mexc, bitget, coinex]


    # Look at spread

    looping = True

    while looping:

        for exchange in ll_exchanges:

            joint_tickers = find_joint_tickers(hl_exchange, exchange)

            try:
                calculate_spread(hl_exchange, exchange, joint_tickers, 0.2)
            except ccxt.NetworkError:
                print('Core loop network error')
            finally:
                time.sleep(10)

        time.sleep(300)
