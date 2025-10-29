from abc import ABC, abstractmethod

class Broker(ABC):
    """
    Abstract base class for a generic broker interface.
    """

    @abstractmethod
    def get_cash_balance(self):
        """
        Returns the current cash balance in the account.
        """
        pass

    @abstractmethod
    def get_position(self, symbol: str):
        """
        Returns the current position for a given symbol.
        """
        pass

    @abstractmethod
    def place_order(self, symbol: str, quantity: int, side: str, price: float):
        """
        Places an order for a given symbol at a given price.

        Args:
            symbol (str): The symbol to trade.
            quantity (int): The number of shares to trade.
            side (str): 'buy' or 'sell'.
            price (float): The price at which to execute the trade.
        """
        pass


class MockBroker(Broker):
    """
    A mock broker for paper trading and testing.
    """

    def __init__(self, initial_cash: float = 10000.0):
        self._cash = initial_cash
        self._positions = {}  # E.g., {'GOOG': 10}

    def get_cash_balance(self) -> float:
        return self._cash

    def get_position(self, symbol: str) -> int:
        return self._positions.get(symbol, 0)

    def place_order(self, symbol: str, quantity: int, side: str, price: float):
        if side not in ('buy', 'sell'):
            raise ValueError("side must be 'buy' or 'sell'")
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        cost = quantity * price

        if side == 'buy':
            if self._cash < cost:
                raise ValueError("Insufficient funds to place buy order")
            self._cash -= cost
            self._positions[symbol] = self.get_position(symbol) + quantity
            print(f"BOUGHT: {quantity} {symbol} @ {price}")

        elif side == 'sell':
            current_position = self.get_position(symbol)
            if current_position < quantity:
                raise ValueError(f"Cannot sell {quantity} shares of {symbol}; only hold {current_position}")
            self._cash += cost
            self._positions[symbol] -= quantity
            if self._positions[symbol] == 0:
                del self._positions[symbol]
            print(f"SOLD: {quantity} {symbol} @ {price}")
