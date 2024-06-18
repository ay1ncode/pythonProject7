import yfinance as yf
import pandas as pd
from datetime import datetime
import alpaca_trade_api as tradeapi
import os

# Read Alpaca API credentials from environment variables
API_KEY = os.getenv('ALPACA_API_KEY')
API_SECRET = os.getenv('ALPACA_API_SECRET')
BASE_URL = 'https://paper-api.alpaca.markets'  # Use the paper trading URL for testing

# Initialize the Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')


def get_stock_data(ticker, period='1mo', interval='1d'):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist


def moving_average_strategy(ticker, short_window=10, long_window=40):
    data = get_stock_data(ticker)

    if data.empty:
        print(f"No data found for ticker {ticker}")
        return None, data

    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

    print(data.tail())  # Debug: Check the last few rows of the dataframe

    signal = None
    if data['Short_MA'].iloc[-1] > data['Long_MA'].iloc[-1]:
        signal = 'BUY'
    elif data['Short_MA'].iloc[-1] < data['Long_MA'].iloc[-1]:
        signal = 'SELL'
    else:
        signal = 'HOLD'  # New case for equal moving averages

    return signal, data



def execute_trade(signal, ticker):
    # Get current position
    try:
        position = api.get_position(ticker)
        qty = int(position.qty)
    except tradeapi.rest.APIError as e:
        if 'position does not exist' in str(e):
            qty = 0
        else:
            print(f"Error retrieving position for {ticker}: {e}")
            return

    if signal == 'BUY' and qty < 20:
        # Place a buy order
        try:
            api.submit_order(
                symbol=ticker,
                qty=2,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print(f"BUY order placed for {ticker}")
        except Exception as e:
            print(f"Error placing BUY order for {ticker}: {e}")

    elif signal == 'SELL' and qty > 0:
        # Place a sell order
        try:
            api.submit_order(
                symbol=ticker,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print(f"SELL order placed for {ticker}")
        except Exception as e:
            print(f"Error placing SELL order for {ticker}: {e}")


def main():
    ticker = 'PLTR'  # Example ticker, you can change this
    signal, data = moving_average_strategy(ticker)

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{now} - {ticker} - Signal: {signal}")

    with open("trading_log.txt", "a") as f:
        f.write(f"{now} - {ticker} - Signal: {signal}\n")

    if signal == 'BUY' or signal == 'SELL':
        execute_trade(signal, ticker)



if __name__ == "__main__":
    main()
