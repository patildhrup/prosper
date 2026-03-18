from typing import Optional

def validate_side(side: str):
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be either BUY or SELL")

def validate_order_type(order_type: str):
    if order_type.upper() not in ["MARKET", "LIMIT", "STOP_MARKET"]:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_MARKET")

def validate_price(order_type: str, price: Optional[float]):
    if order_type.upper() == "LIMIT" and not price:
        raise ValueError("Price is required for LIMIT orders")

def validate_stop_price(order_type: str, stop_price: Optional[float]):
    if order_type.upper() == "STOP_MARKET" and not stop_price:
        raise ValueError("Stop Price is required for STOP_MARKET orders")