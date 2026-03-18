from loguru import logger
from binance.exceptions import BinanceAPIException, BinanceOrderException

def place_order(client, symbol, side, order_type, quantity, price=None, stop_price=None):
    """
    Places an order on Binance Futures Testnet.
    Supports MARKET, LIMIT, and STOP_MARKET.
    """
    try:
        logger.info(f"Order Request | Symbol: {symbol} | Side: {side} | Type: {order_type} | Qty: {quantity} | Price: {price} | StopPrice: {stop_price}")

        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }

        if order_type.upper() == "LIMIT":
            if not price:
                raise ValueError("Price is required for LIMIT orders")
            params.update({
                "price": price,
                "timeInForce": "GTC"
            })
            
        elif order_type.upper() == "STOP_MARKET":
            if not stop_price:
                raise ValueError("Stop Price is required for STOP_MARKET orders")
            params.update({
                "stopPrice": stop_price
            })

        # Execute order
        order = client.futures_create_order(**params)

        # Log success response
        logger.info(f"Order Response | ID: {order.get('orderId')} | Status: {order.get('status')} | ExecutedQty: {order.get('executedQty')} | AvgPrice: {order.get('avgPrice', 'N/A')}")
        
        return order

    except (BinanceAPIException, BinanceOrderException) as e:
        logger.error(f"Binance Error: Status={e.status_code}, Code={e.code}, Message={e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}")
        raise