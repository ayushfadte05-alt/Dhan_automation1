import unittest
from backend.broker import MockBroker

class TestMockBroker(unittest.TestCase):

    def setUp(self):
        """Set up a new MockBroker instance before each test."""
        self.broker = MockBroker(initial_cash=10000.0)

    def test_initial_state(self):
        """Test the initial state of the broker."""
        self.assertEqual(self.broker.get_cash_balance(), 10000.0)
        self.assertEqual(self.broker.get_position("AAPL"), 0)
        self.assertEqual(self.broker._positions, {})

    def test_buy_order_success(self):
        """Test a successful buy order."""
        self.broker.place_order("AAPL", 10, "buy", price=150.0)
        self.assertEqual(self.broker.get_cash_balance(), 10000.0 - (10 * 150.0))
        self.assertEqual(self.broker.get_position("AAPL"), 10)

    def test_buy_order_insufficient_funds(self):
        """Test a buy order that fails due to insufficient funds."""
        with self.assertRaises(ValueError):
            self.broker.place_order("AAPL", 100, "buy", price=150.0)
        # Ensure state has not changed
        self.assertEqual(self.broker.get_cash_balance(), 10000.0)
        self.assertEqual(self.broker.get_position("AAPL"), 0)

    def test_sell_order_success(self):
        """Test a successful sell order."""
        # First, buy some shares to have a position
        self.broker.place_order("MSFT", 20, "buy", price=300.0)
        self.assertEqual(self.broker.get_cash_balance(), 4000.0)
        self.assertEqual(self.broker.get_position("MSFT"), 20)

        # Now, sell some of them
        self.broker.place_order("MSFT", 5, "sell", price=310.0)
        self.assertEqual(self.broker.get_cash_balance(), 4000.0 + (5 * 310.0))
        self.assertEqual(self.broker.get_position("MSFT"), 15)

    def test_sell_all_shares(self):
        """Test selling all shares of a position."""
        self.broker.place_order("GOOG", 5, "buy", price=500.0)
        self.broker.place_order("GOOG", 5, "sell", price=520.0)
        self.assertEqual(self.broker.get_cash_balance(), 10000.0 - (5 * 500) + (5 * 520))
        self.assertEqual(self.broker.get_position("GOOG"), 0)
        self.assertNotIn("GOOG", self.broker._positions) # Ensure symbol is removed

    def test_sell_order_insufficient_position(self):
        """Test selling more shares than are held."""
        self.broker.place_order("TSLA", 5, "buy", price=200.0)
        with self.assertRaises(ValueError):
            self.broker.place_order("TSLA", 10, "sell", price=210.0)
        # Ensure state has not changed
        self.assertEqual(self.broker.get_cash_balance(), 9000.0)
        self.assertEqual(self.broker.get_position("TSLA"), 5)

    def test_invalid_order_side(self):
        """Test placing an order with an invalid side."""
        with self.assertRaises(ValueError):
            self.broker.place_order("NVDA", 10, "hold", price=400.0)

    def test_zero_or_negative_quantity(self):
        """Test placing an order with zero or negative quantity."""
        with self.assertRaises(ValueError):
            self.broker.place_order("AMD", 0, "buy", price=100.0)
        with self.assertRaises(ValueError):
            self.broker.place_order("AMD", -5, "sell", price=100.0)

if __name__ == "__main__":
    unittest.main()
