import ccxt
import time

from calculate_spread import calculate_spread
from find_joint_tickers import find_joint_tickers


if __name__ == '__main__':

    # Initializing clients

    hl_exchange = ccxt.gate()
    ll_exchange = ccxt.mexc()

    joint_tickers = find_joint_tickers(hl_exchange, ll_exchange)

    # Look at spread

    looping = True

    while looping:

        calculate_spread(hl_exchange, ll_exchange, joint_tickers, 0.2)
        time.sleep(300)


