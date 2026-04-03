import typer
from bot.orders import place_order
from bot.logger import setup_logging

# Initialize logging once when app starts
setup_logging()

app = typer.Typer(help="Binance Futures Testnet Trading Bot")

@app.command()
def trade(
    symbol: str = typer.Argument(..., help="Trading pair (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side: BUY or SELL"),
    order_type: str = typer.Argument(..., help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Argument(..., help="Quantity of the asset"),
    price: float = typer.Option(None, help="Price (Required only for LIMIT orders)")
):
    """
    Place an order on Binance Futures Testnet.
    """
    # Basic Validation
    valid_sides = ["BUY", "SELL"]
    valid_types = ["MARKET", "LIMIT"]

    if side.upper() not in valid_sides:
        print(f"Error: Side must be one of {valid_sides}")
        raise typer.Abort()
    
    if order_type.upper() not in valid_types:
        print(f"Error: Type must be one of {valid_types}")
        raise typer.Abort()

    # Execute Order
    result = place_order(symbol, side, order_type, quantity, price)

    # Print Result
    print("\n" + "="*30)
    print("ORDER SUMMARY")
    print("="*30)
    
    # FIX: Check specific status strings instead of looking for 'error' key
    if result['status'] in ['NEW', 'FILLED', 'PARTIALLY_FILLED']:
        print(f"✅ Order Status: {result['status']}")
        print(f"🆔 Order ID: {result['orderId']}")
        print(f"📊 Symbol: {result['symbol']}")
        print(f"📈 Side: {result['side']}")
        print(f"📝 Type: {result['type']}")
        print(f"📦 Executed Qty: {result['executedQty']}")
        print(f"💰 Avg Price: {result['avgPrice']}")
        
        # Handle None values for cleaner print
        cost = result.get('cummulativeQuoteQty')
        

        # --- FIX: Calculate Cost Manually ---
        try:
            avg_price = float(result.get('avgPrice') or 0)
            exec_qty = float(result.get('executedQty') or 0)
            calculated_cost = avg_price * exec_qty
            print(f"💵 Cost (USDT): {calculated_cost:.2f}")
        except ValueError:
            print(f"💵 Cost (USDT): N/A (Calculating...)")

        # ... rest of code ...
        
    else:
        # This handles failed statuses: 'VALIDATION_FAILED', 'API_ERROR', 'ERROR'
        print(f"❌ Order Failed with status: {result.get('status')}")
        print(f"Details: {result.get('message', result.get('error', 'Unknown error'))}")
        
    print("="*30 + "\n")






@app.command()
def balance():
    """
    Check account balance and open positions.
    """
    from bot.client import get_binance_client
    
    client = get_binance_client()
    
    try:
        # Get Account Balance
        account = client.futures_account()
        usdt_balance = next((item for item in account['assets'] if item['asset'] == 'USDT'), None)
        
        print("\n" + "="*30)
        print("ACCOUNT BALANCE")
        print("="*30)
        if usdt_balance:
            print(f"💵 Wallet Balance: {usdt_balance['walletBalance']} USDT")
            print(f"✅ Available Balance: {usdt_balance['availableBalance']} USDT")
        
        # Get Open Positions
        positions = client.futures_position_information()
        open_positions = [p for p in positions if float(p['positionAmt']) != 0]
        
        print("\n" + "-"*30)
        if open_positions:
            print("OPEN POSITIONS:")
            for pos in open_positions:
                print(f"Symbol: {pos['symbol']} | Side: {pos['positionSide']} | Size: {pos['positionAmt']} | Entry Price: {pos['entryPrice']}")
        else:
            print("No open positions.")
        print("="*30 + "\n")

    except Exception as e:
        print(f"Error fetching balance: {e}")

if __name__ == "__main__":
    app()