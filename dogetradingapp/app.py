from flask import Flask, request
import json
from binance.client import Client
import math
from binance.helpers import round_step_size


app = Flask(__name__)


@app.route("/webhook", methods=['POST'])
def webhook():
    
    def get_tick_size():
        info = client.futures_exchange_info()

        for symbol_info in info['symbols']:
            if symbol_info['symbol'] == "DOGEBUSD":
                for symbol_filter in symbol_info['filters']:
                    if symbol_filter['filterType'] == 'PRICE_FILTER':
                        return float(symbol_filter['tickSize'])


    def get_rounded_price(price):
        return round_step_size(price, get_tick_size(symbol))
    

    def LongPosition(client,lev,price):
        try:
            ExitShortPosition(client)
        except:
            pass
        try:
            ExitLongPosition(client)
        except:
            pass
        
        
        assets = client.futures_account_balance()
        for asset in assets:
          if "BUSD" in asset.values():
            balance = float(asset["balance"])

        markPrice = float(client.futures_mark_price(symbol="DOGEBUSD")["markPrice"])
        price = price = get_rounded_price(price*99.9/100)
        for i in range(99,48,-5):
            
            quot = math.floor((balance/markPrice)*(i/100)*1000*lev)/1000
            
            """
            params = {"symbol":"DOGEBUSD",
                    "type":"MARKET",
                    "side":"BUY",
                    "quantity":int(quot),
                    "reduceOnly":"false"} 
            """
            tick = get_ticksize(cur)
            
            params = {"symbol":"DOGEBUSD",
                      "type":"LIMIT",
                      "side":"BUY",
                      "price":price,
                      "quantity":int(quot),
                      "timeInForce":"GTC"}
           

            LongPos = client.futures_create_order(**params)
            
        """
        client.futures_cancel_all_open_orders(**{"symbol":"DOGEBUSD"})
        eP = float(client.futures_position_information(symbol="DOGEBUSD")[0]["entryPrice"])
        sL = eP*99/100
        params = {"symbol":"DOGEBUSD",
                  "type":"STOP_MARKET",
                  "side":"SELL",
                  "quantity":quot,
                  "stopPrice":sL,
                  "workingType":"MARK_PRICE",
                  "closePosition":"true"}
        stopLoss = client.futures_create_order(**params)
        """
  
            
    def ExitLongPosition(client):
        client.futures_cancel_all_open_orders(**{"symbol":"DOGEBUSD"})
        qty = client.futures_position_information(symbol="DOGEBUSD")[0]["positionAmt"]
        params = {
            "symbol":"DOGEBUSD",
            "side":"SELL",
            "type":'MARKET',
            "quantity":qty,
            "reduceOnly":"true"
            }
        ExitLong = client.futures_create_order(**params)


    def ShortPosition(client,lev,price):
        try:
            ExitLongPosition(client)
        except:
            pass
        try:
            ExitShortPosition(client)
        except:
            pass
        
        
        assets = client.futures_account_balance()
        for asset in assets:
          if "BUSD" in asset.values():
            balance = float(asset["balance"])

        markPrice = float(client.futures_mark_price(symbol="DOGEBUSD")["markPrice"])
        price = price = get_rounded_price(price*100.1/100)
        for i in range(99,48,-5):
        
            quot = math.floor((balance/markPrice)*(i/100)*1000*lev)/1000
            
            """
            params = {"symbol":"DOGEBUSD",
                    "type":"MARKET",
                    "side":"SELL",
                    "quantity":int(quot),
                    "reduceOnly":"false"}
            """
            
            params = {"symbol":"DOGEBUSD",
                "type":"LIMIT",
                "side":"SELL",
                "price":price,
                "quantity":int(quot),
                "timeInForce":"GTC"}
            

            ShortPos = client.futures_create_order(**params)
        
        """
        client.futures_cancel_all_open_orders(**{"symbol":"DOGEBUSD"})
        eP = float(client.futures_position_information(symbol="DOGEBUSD")[0]["entryPrice"])
        sL = eP*101/100
        params = {"symbol":"DOGEBUSD",
                  "type":"STOP_MARKET",
                  "side":"BUY",
                  "quantity":quot,
                  "stopPrice":sL,
                  "workingType":"MARK_PRICE",
                  "closePosition":"true"}
        stopLoss = client.futures_create_order(**params)
        """

    def ExitShortPosition(client):
        client.futures_cancel_all_open_orders(**{"symbol":"DOGEBUSD"})
        qty = -(client.futures_position_information(symbol="DOGEBUSD")[0]["positionAmt"])
        params = {
            "symbol":"DOGEBUSD",
            "side":"BUY",
            "type":'MARKET',
            "quantity":qty,
            "reduceOnly":"true"
            }
        ExitShort = client.futures_create_order(**params)

    
    def LongTehlikesi(client):
        symbolInfo = client.futures_position_information(symbol="DOGEBUSD")[0]
        eP = float(symbolInfo["entryPrice"])
        mP = float(symbolInfo["markPrice"])
        amnt = float(symbolInfo["positionAmt"])

        if mP > eP and amnt>0:
          ExitLongPosition(client)
          client.futures_cancel_all_open_orders(**{"symbol":"DOGEBUSD"})
           

    def ShortTehlikesi(client):
        symbolInfo = client.futures_position_information(symbol="DOGEBUSD")[0]
        eP = float(symbolInfo["entryPrice"])
        mP = float(symbolInfo["markPrice"])
        amnt = float(symbolInfo["positionAmt"])

        if mP < eP and amnt<0:
          ExitShortPosition(client)
          client.futures_cancel_all_open_orders(**{"symbol":"DOGEBUSD"})

    try:
        data = json.loads(request.data)
        order = data["order"]
        lev = data["leverage"]
        price = float(data["price"])
        #fark = float(data["fark"])
        api_key = data["api_key"]
        api_secret = data["api_secret"]
        
        client = Client(api_key, api_secret, testnet=False)
        client.futures_change_leverage(**{"symbol":"DOGEBUSD","leverage":lev})

        if order == "LongPosition":
            LongPosition(client,lev,price)

        elif order == "ExitLongPosition":
            ExitLongPosition(client)
          
        elif order == "ShortPosition":
            ShortPosition(client,lev,price)

        elif order == "ExitShortPosition":
            ExitShortPosition(client)

        elif order == "LongTehlikesi":
            LongTehlikesi(client)

        elif order == "ShortTehlikesi":
            ShortTehlikesi(client)

    except Exception as e:
        print(e)
        pass
    return {
        "code": "success",

    }
