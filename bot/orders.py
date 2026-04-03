import logging
import time # Import time module for the delay
from binance.exceptions import BinanceAPIException
from bot.client import get_binance_client
from bot import validators 

logger = logging.getLogger(__name__)

def place_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """
    Places an order on Binance Futures Testnet with validation and status polling.
    """
    client = get_binance_client()
    
    symbol = symbol.upper()
    side = side.upper()
    order_type = order_type.upper()

    logger.info(f"--- Placing Order Request ---")
    
    try:
        # 1. Validate and Format Quantity
        quantity = validators.validate_and_format_quantity(client, symbol, quantity)
        price = validators.validate_price(symbol, price)

        logger.info(f"Symbol: {symbol}, Side: {side}, Type: {order_type}, Qty: {quantity}, Price: {price}")

        # Parameter preparation
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }

        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params['price'] = price
            params['timeInForce'] = 'GTC'

        # Execute Order
        result = client.futures_create_order(**params)
        logger.info("Order Request Accepted by Exchange.")

        # --- NEW: POLLING LOGIC ---
        # Since Testnet is slow, we wait 1 second and check the final status
        # This ensures we get the average price and filled qty for Market orders.
        time.sleep(1) 
        
        # Fetch the updated order status from the server
        final_order_status = client.futures_get_order(symbol=symbol, orderId=result['orderId'])
        logger.info(f"Final Status Retrieved: {final_order_status.get('status')}")
        
        # Use the updated data for the output
        output = {
            "status": final_order_status.get('status'),
            "orderId": final_order_status.get('orderId'),
            "symbol": final_order_status.get('symbol'),
            "side": final_order_status.get('side'),
            "type": final_order_status.get('type'),
            "executedQty": final_order_status.get('executedQty'),
            #"cummulativeQuoteQty": final_order_status.get('cumQty'),
            "cummulativeQuoteQty": final_order_status.get('cummulativeQuoteQty'), 
            "avgPrice": final_order_status.get('avgPrice'),
            "transactTime": final_order_status.get('updateTime')
        }
        
        return output

    except ValueError as e:
        logger.error(f"Validation Error: {e}")
        return {"status": "VALIDATION_FAILED", "error": str(e)}
    except BinanceAPIException as e:
        logger.error(f"Binance API Error: {e.message}")
        return {"status": "API_ERROR", "error": e.message}
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}")
        return {"status": "ERROR", "error": str(e)}