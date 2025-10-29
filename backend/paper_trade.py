import pandas as pd
from backtesting.test import GOOG
from backend.broker import MockBroker

def run_paper_trading_simulation():
    """
    Simulates the SmaCross strategy using the MockBroker.
    """
    print("--- Starting Paper Trading Simulation ---")

    # 1. Initialize broker and data
    broker = MockBroker(initial_cash=10000.0)
    data = GOOG.copy()
    symbol = "GOOG"

    # 2. Calculate indicators (SMAs)
    n1 = 10
    n2 = 20
    data[f'SMA{n1}'] = data['Close'].rolling(n1).mean()
    data[f'SMA{n2}'] = data['Close'].rolling(n2).mean()

    # Drop NA rows created by rolling means
    data.dropna(inplace=True)
    # Reset index to ensure clean iteration
    data.reset_index(drop=True, inplace=True)

    print(f"Initial Cash: ${broker.get_cash_balance():.2f}")

    # 3. Iterate through data and apply strategy logic
    for i in range(1, len(data)):
        # Check for crossover signals
        prev_sma1 = data.loc[i-1, f'SMA{n1}']
        prev_sma2 = data.loc[i-1, f'SMA{n2}']
        curr_sma1 = data.loc[i, f'SMA{n1}']
        curr_sma2 = data.loc[i, f'SMA{n2}']

        current_price = data.loc[i, 'Close']

        # Buy signal: short SMA crosses above long SMA
        if prev_sma1 <= prev_sma2 and curr_sma1 > curr_sma2:
            quantity_to_buy = 10
            cost = quantity_to_buy * current_price
            if broker.get_cash_balance() >= cost:
                try:
                    broker.place_order(symbol, quantity=quantity_to_buy, side='buy', price=current_price)
                except ValueError as e:
                    print(f"ERROR placing buy order: {e}")

        # Sell signal: short SMA crosses below long SMA
        elif prev_sma1 >= prev_sma2 and curr_sma1 < curr_sma2:
            current_position = broker.get_position(symbol)
            if current_position > 0:
                try:
                    broker.place_order(symbol, quantity=current_position, side='sell', price=current_price)
                except ValueError as e:
                    print(f"ERROR placing sell order: {e}")

    # 4. Report final results
    print("\n--- Simulation Complete ---")
    final_cash = broker.get_cash_balance()
    final_position = broker.get_position(symbol)

    print(f"Final Cash: ${final_cash:.2f}")
    if final_position > 0:
        last_price = data.loc[len(data)-1, 'Close']
        portfolio_value = final_position * last_price
        print(f"Final Position: {final_position} {symbol} (Value: ${portfolio_value:.2f})")
        total_value = final_cash + portfolio_value
    else:
        print("Final Position: None")
        total_value = final_cash

    print(f"Total Portfolio Value: ${total_value:.2f}")
    profit_or_loss = total_value - 10000.0
    print(f"Net Profit/Loss: ${profit_or_loss:.2f}")


if __name__ == "__main__":
    run_paper_trading_simulation()
