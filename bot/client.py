import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_binance_client():
    """Initialize and return a Binance Client connected to Testnet."""
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError("API Key or Secret not found in environment variables.")

    # testnet=True is crucial for this assignment
    client = Client(api_key, api_secret, testnet=True)
    
    return client