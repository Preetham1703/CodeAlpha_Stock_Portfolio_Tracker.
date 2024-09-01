import requests

# Constants
ALPHA_VANTAGE_API_KEY = 'your_alpha_vantage_api_key'  # Replace with your API key
ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query'

# Portfolio Class
class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, quantity, purchase_price):
        self.stocks[symbol] = {'quantity': quantity, 'purchase_price': purchase_price}
        print(f"Added {quantity} shares of {symbol} at ${purchase_price:.2f} each.")

    def remove_stock(self, symbol):
        if symbol in self.stocks:
            del self.stocks[symbol]
            print(f"Removed {symbol} from portfolio.")
        else:
            print(f"{symbol} not found in portfolio.")

    def get_stock_price(self, symbol):
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': '1min',
            'apikey': ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        data = response.json()
        if 'Time Series (1min)' in data:
            latest_time = next(iter(data['Time Series (1min)']))
            latest_price = float(data['Time Series (1min)'][latest_time]['1. open'])
            return latest_price
        else:
            print(f"Error fetching data for {symbol}: {data.get('Error Message', 'Unknown error')}")
            return None

    def calculate_portfolio_value(self):
        total_value = 0.0
        for symbol, details in self.stocks.items():
            current_price = self.get_stock_price(symbol)
            if current_price:
                total_value += current_price * details['quantity']
        return total_value

    def display_portfolio(self):
        print("\nCurrent Portfolio:")
        for symbol, details in self.stocks.items():
            current_price = self.get_stock_price(symbol)
            if current_price:
                print(f"{symbol}: {details['quantity']} shares, Purchase Price: ${details['purchase_price']:.2f}, Current Price: ${current_price:.2f}, Value: ${current_price * details['quantity']:.2f}")
            else:
                print(f"{symbol}: Data not available")

# Example usage
def main():
    portfolio = Portfolio()

    # Add stocks
    portfolio.add_stock('AAPL', 10, 150.00)
    portfolio.add_stock('GOOGL', 5, 2500.00)

    # Display portfolio
    portfolio.display_portfolio()

    # Calculate total value
    total_value = portfolio.calculate_portfolio_value()
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")

    # Remove a stock
    portfolio.remove_stock('GOOGL')

    # Display portfolio after removal
    portfolio.display_portfolio()

if __name__ == "__main__":
    main()
