from flask import Flask, request
import json
from binance.client import Client
import math
from binance.helpers import round_step_size


app = Flask(__name__)


@app.route("/webhook", methods=['POST'])
def webhook():
    
    def get_tick_size(symbol):
        info = client.futures_exchange_info()

        for symbol_info in info['symbols']:
            if symbol_info['symbol'] == symbol:
                for symbol_filter in symbol_info['filters']:
                    if symbol_filter['filterType'] == 'PRICE_FILTER':
                        return float(symbol_filter['tickSize'])


    def get_rounded_price(price,symbol):
        return round_step_size(price, get_tick_size(symbol))
    

    def LongPosition(client,lev,symbol):
        try:
            ExitShortPosition(client,symbol)
        except:
            pass
        try:
            ExitLongPosition(client,symbol)
        except:
            pass
        
        
        assets = client.futures_account_balance()
        for asset in assets:
          if "BUSD" in asset.values():
            balance = float(asset["balance"])

        markPrice = float(client.futures_mark_price(symbol=symbol)["markPrice"])
        #price = get_rounded_price(price*99.9/100,symbol)
       
            
        quot = int(math.floor((balance/markPrice)*(80/100)*1000*lev)/1000)

        
        params = {"symbol":symbol,
                "type":"MARKET",
                "side":"BUY",
                "quantity":quot,
                "reduceOnly":"false"} 
        """
        params = {"symbol":symbol,
                  "type":"LIMIT",
                  "side":"BUY",
                  "price":price,
                  "quantity":float(quot),
                  "timeInForce":"GTC"}
        """

        LongPos = client.futures_create_order(**params)
            
        """
        client.futures_cancel_all_open_orders(**{"symbol":symbol})
        eP = float(client.futures_position_information(symbol=symbol)[0]["entryPrice"])
        sL = eP*99/100
        params = {"symbol":symbol,
                  "type":"STOP_MARKET",
                  "side":"SELL",
                  "quantity":quot,
                  "stopPrice":sL,
                  "workingType":"MARK_PRICE",
                  "closePosition":"true"}
        stopLoss = client.futures_create_order(**params)
        """
  
            
    def ExitLongPosition(client,symbol):
        client.futures_cancel_all_open_orders(**{"symbol":symbol})
        qty = int(client.futures_position_information(symbol=symbol)[0]["positionAmt"])
        params = {
            "symbol":symbol,
            "side":"SELL",
            "type":'MARKET',
            "quantity":qty,
            "reduceOnly":"true"
            }
        ExitLong = client.futures_create_order(**params)


    def ShortPosition(client,lev,symbol):
        try:
            ExitLongPosition(client,symbol)
        except:
            pass
        try:
            ExitShortPosition(client,symbol)
        except:
            pass
        
        
        assets = client.futures_account_balance()
        for asset in assets:
          if "BUSD" in asset.values():
            balance = float(asset["balance"])

        markPrice = float(client.futures_mark_price(symbol=symbol)["markPrice"])
        #price = price = get_rounded_price(price*100.1/100,symbol)

        
        quot = int(math.floor((balance/markPrice)*(80/100)*1000*lev)/1000)

        
        params = {"symbol":symbol,
                "type":"MARKET",
                "side":"SELL",
                "quantity":quot,
                "reduceOnly":"false"}
        """
        params = {"symbol":symbol,
            "type":"LIMIT",
            "side":"SELL",
            "price":price,
            "quantity":float(quot),
            "timeInForce":"GTC"}
        """

        ShortPos = client.futures_create_order(**params)
        
        """
        client.futures_cancel_all_open_orders(**{"symbol":symbol})
        eP = float(client.futures_position_information(symbol=symbol)[0]["entryPrice"])
        sL = eP*101/100
        params = {"symbol":symbol,
                  "type":"STOP_MARKET",
                  "side":"BUY",
                  "quantity":quot,
                  "stopPrice":sL,
                  "workingType":"MARK_PRICE",
                  "closePosition":"true"}
        stopLoss = client.futures_create_order(**params)
        """

    def ExitShortPosition(client,symbol):
        client.futures_cancel_all_open_orders(**{"symbol":symbol})
        qty = -(int(client.futures_position_information(symbol=symbol)[0]["positionAmt"]))
        params = {
            "symbol":symbol,
            "side":"BUY",
            "type":'MARKET',
            "quantity":qty,
            "reduceOnly":"true"
            }
        ExitShort = client.futures_create_order(**params)
    

    try:
        data = json.loads(request.data)
        symbol = data["symbol"]
        order = data["order"]
        lev = data["leverage"]
        #price = float(data["price"])
        #fark = float(data["fark"])
        api_key = data["api_key"]
        api_secret = data["api_secret"]
        
        client = Client(api_key, api_secret, testnet=False)
        client.futures_change_leverage(**{"symbol":symbol,"leverage":lev})

        if order == "LongPosition":
            LongPosition(client,lev,symbol)

        elif order == "ExitLongPosition":
            ExitLongPosition(client,symbol)
          
        elif order == "ShortPosition":
            ShortPosition(client,lev,symbol)

        elif order == "ExitShortPosition":
            ExitShortPosition(client,symbol)


    except Exception as e:
        print(e)
        pass
    return {
        "code": "success",

    }
