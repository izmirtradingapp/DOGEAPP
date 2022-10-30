from flask import Flask, request
import json
from binance.client import Client
import math 


app = Flask(__name__)


@app.route("/webhook", methods=['POST'])
def webhook():

    def LongPosition(client,lev,price,fark):
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
          if "USDT" in asset.values():
            balance = float(asset["balance"])

        markPrice = float(client.futures_mark_price(symbol="DOGEUSDT")["markPrice"])
        
        for i in range(4):
            
            if i == 0:
                quot = math.floor((balance/markPrice)*(90/100)*1000*lev)/1000
            
            if i == 1:
                quot = math.floor((balance/markPrice)*(80/100)*1000*lev)/1000
                
            if i == 2:
                quot = math.floor((balance/markPrice)*(70/100)*1000*lev)/1000
                
            if i == 3:
                quot = math.floor((balance/markPrice)*(60/100)*1000*lev)/1000
            
            if i == 4:
                quot = math.floor((balance/markPrice)*(50/100)*1000*lev)/1000
            
            """
            params = {"symbol":"DOGEUSDT",
                    "type":"MARKET",
                    "side":"BUY",
                    "quantity":int(quot),
                    "reduceOnly":"false"} 
            """
            params = {"symbol":"DOGEUSDT",
                      "type":"LIMIT",
                      "side":"BUY",
                      "price":price-fark,
                      "quantity":quot,
                      "timeInForce":"GTC"}

            LongPos = client.futures_create_order(**params)
            
        """
        client.futures_cancel_all_open_orders(**{"symbol":"DOGEUSDT"})
        eP = float(client.futures_position_information(symbol="DOGEUSDT")[0]["entryPrice"])
        sL = eP*99/100
        params = {"symbol":"DOGEUSDT",
                  "type":"STOP_MARKET",
                  "side":"SELL",
                  "quantity":quot,
                  "stopPrice":sL,
                  "workingType":"MARK_PRICE",
                  "closePosition":"true"}
        stopLoss = client.futures_create_order(**params)
        """
  
            
    def ExitLongPosition(client):
        client.futures_cancel_all_open_orders(**{"symbol":"DOGEUSDT"})
        qty = client.futures_position_information(symbol="DOGEUSDT")[0]["positionAmt"]
        params = {
            "symbol":"DOGEUSDT",
            "side":"SELL",
            "type":'MARKET',
            "quantity":qty,
            "reduceOnly":"true"
            }
        ExitLong = client.futures_create_order(**params)


    def ShortPosition(client,lev,price,fark):
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
          if "USDT" in asset.values():
            balance = float(asset["balance"])

        markPrice = float(client.futures_mark_price(symbol="DOGEUSDT")["markPrice"])
        
        for i in range(4):
        
            if i == 0:
                quot = math.floor((balance/markPrice)*(90/100)*1000*lev)/1000
            
            if i == 1:
                quot = math.floor((balance/markPrice)*(80/100)*1000*lev)/1000
                
            if i == 2:
                quot = math.floor((balance/markPrice)*(70/100)*1000*lev)/1000
                
            if i == 3:
                quot = math.floor((balance/markPrice)*(60/100)*1000*lev)/1000
                
            if i == 4:
                quot = math.floor((balance/markPrice)*(50/100)*1000*lev)/1000
            
            
            """"
            params = {"symbol":"DOGEUSDT",
                    "type":"MARKET",
                    "side":"SELL",
                    "quantity":int(quot),
                    "reduceOnly":"false"}
            """"
            params = {"symbol":"DOGEUSDT",
                "type":"LIMIT",
                "side":"SELL",
                "price":price+fark,
                "quantity":quot,
                "timeInForce":"GTC"}

            ShortPos = client.futures_create_order(**params)
        
        """
        client.futures_cancel_all_open_orders(**{"symbol":"DOGEUSDT"})
        eP = float(client.futures_position_information(symbol="DOGEUSDT")[0]["entryPrice"])
        sL = eP*101/100
        params = {"symbol":"DOGEUSDT",
                  "type":"STOP_MARKET",
                  "side":"BUY",
                  "quantity":quot,
                  "stopPrice":sL,
                  "workingType":"MARK_PRICE",
                  "closePosition":"true"}
        stopLoss = client.futures_create_order(**params)
        """

    def ExitShortPosition(client):
        client.futures_cancel_all_open_orders(**{"symbol":"DOGEUSDT"})
        qty = -(client.futures_position_information(symbol="DOGEUSDT")[0]["positionAmt"])
        params = {
            "symbol":"DOGEUSDT",
            "side":"BUY",
            "type":'MARKET',
            "quantity":qty,
            "reduceOnly":"true"
            }
        ExitShort = client.futures_create_order(**params)

    
    def LongTehlikesi(client):
        symbolInfo = client.futures_position_information(symbol="DOGEUSDT")[0]
        eP = float(symbolInfo["entryPrice"])
        mP = float(symbolInfo["markPrice"])
        amnt = float(symbolInfo["positionAmt"])

        if mP > eP and amnt>0:
          ExitLongPosition(client)
          client.futures_cancel_all_open_orders(**{"symbol":"DOGEUSDT"})
           

    def ShortTehlikesi(client):
        symbolInfo = client.futures_position_information(symbol="DOGEUSDT")[0]
        eP = float(symbolInfo["entryPrice"])
        mP = float(symbolInfo["markPrice"])
        amnt = float(symbolInfo["positionAmt"])

        if mP < eP and amnt<0:
          ExitShortPosition(client)
          client.futures_cancel_all_open_orders(**{"symbol":"DOGEUSDT"})

    try:
        data = json.loads(request.data)
        order = data["order"]
        lev = data["leverage"]
        price = float(data["price"])
        fark = float(data["fark"])
        api_key = data["api_key"]
        api_secret = data["api_secret"]
        
        client = Client(api_key, api_secret, testnet=False)
        client.futures_change_leverage(**{"symbol":"DOGEUSDT","leverage":lev})

        if order == "LongPosition":
            LongPosition(client,lev,price,fark)

        elif order == "ExitLongPosition":
            ExitLongPosition(client)
          
        elif order == "ShortPosition":
            ShortPosition(client,lev,price,fark)

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
