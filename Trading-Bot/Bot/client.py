import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

def get_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_SECRET_KEY")
    
    # The requirement specifically mentions https://testnet.binancefuture.com
    # python-binance uses the testnet flag to set the correct URLs
    client = Client(api_key, api_secret, testnet=True)
    
    # Double check base URL if provided in .env, otherwise default to python-binance's testnet defaults
    base_url = os.getenv("BASE_URL")
    if base_url:
        client.FUTURES_URL = base_url
    
    return client