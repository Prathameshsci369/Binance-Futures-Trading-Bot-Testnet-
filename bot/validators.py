import logging
import math
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)

def get_symbol_info(client, symbol):
    """Fetch exchange info for a specific symbol."""
    try:
        info = client.futures_exchange_info()
        for s in info['symbols']:
            if s['symbol'] == symbol:
                return s
        raise ValueError(f"Symbol {symbol} not found.")
    except Exception as e:
        logger.error(f"Error fetching symbol info: {e}")
        raise

def validate_and_format_quantity(client, symbol, quantity):
    """
    Validates quantity against Binance LOT_SIZE filter.
    Ensures the quantity has the correct number of decimal places.
    """
    symbol_info = get_symbol_info(client, symbol)
    
    # Find the LOT_SIZE filter
    lot_size_filter = next((f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'), None)
    
    if not lot_size_filter:
        return quantity 

    step_size_str = lot_size_filter['stepSize']
    min_qty = float(lot_size_filter['minQty'])
    max_qty = float(lot_size_filter['maxQty'])

    # 1. Check Minimum Quantity
    if quantity < min_qty:
        logger.warning(f"Quantity {quantity} is below Min Notional/Min Qty ({min_qty}). Order might fail.")
    
    # 2. Check Maximum Quantity
    if quantity > max_qty:
        raise ValueError(f"Quantity {quantity} is too large. Max qty: {max_qty}")

    # 3. Calculate Precision (The Fix)
    # We count how many decimals are in the step_size string.
    # e.g., "0.001" -> 3 decimals. "1" -> 0 decimals.
    if 'e-' in step_size_str:
        # Handle scientific notation like "1e-05"
        precision = int(step_size_str.split('e-')[1])
    elif '.' in step_size_str:
        precision = len(step_size_str.split('.')[1].rstrip('0'))
    else:
        precision = 0

    # 4. Format the quantity
    # math.floor is used to ensure we don't accidentally round up (which causes precision errors)
    formatted_qty = math.floor(quantity * (10 ** precision)) / (10 ** precision)
    
    # Edge case: if rounding makes it 0, but it was > 0, the input was too small for the precision.
    if formatted_qty == 0 and quantity > 0:
         raise ValueError(f"Quantity {quantity} is too small for this precision. Min step: {step_size_str}")

    logger.info(f"Quantity formatted from {quantity} to {formatted_qty} (Step: {step_size_str})")
    return formatted_qty

def validate_price(symbol, price):
    """Basic price validation."""
    if price is not None and price <= 0:
        raise ValueError("Price must be positive.")
    return price