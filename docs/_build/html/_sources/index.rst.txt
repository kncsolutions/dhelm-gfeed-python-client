.. DhelmGfeedClient documentation master file, created by
   sphinx-quickstart on Thu Sep 20 11:04:01 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Dhelm-gfeed-python-client's documentation!
============================================

Dhelm-gfeed-python-client is a python client library to access and integrate stock market data from `Global Financial Datafeeds LLP <https://globaldatafeeds.in/>`_ with your  application.To use this library you must subscribe to web socket api with Global Financial Datafeeds LLP and get your API key and web socket endpoint URL.
Programmatic access to data  provides better and unique control over your algorithm. You access the raw data from your data provider, then feed into your own application and do whatever analysis you want in a unique way.


For detailed integration and usage guidelines, please read through the pages.

License
=======
The dhelm-gfeed-python-client is licensed under *Apache License, Version 2.0* license.

Installation
============

The client is tested with python 3.4+.

Install from Sources
--------------------

1. clone the repository:

   git clone https://github.com/kncsolutions/dhelm-gfeed-python-client.git
2. cd to dhelm-gfeed-python-client
3. python setup.py install

Methods and Callbacks
=====================

Initialization:
---------------

Initialize the client in the following way.

.. sourcecode:: python

 from DhelmGfeedClient.gfeedclient import GfeedClient
 client = GfeedClient("<ws_url>","<api_key>")
 # where,
 #<ws_url> : Replace <ws_url> with the web socket url
 #<api_key> : Replace <api_key> with your api key which you have got on subscription.


Members:
---------

**def connect()** 
^^^^^^^^^^^^^^^^^^

 Call this method to connect to the web socket.

On successful authentication **on_authenticated(base_client)** callback is fired.
The **base_client** is the currently initialised WebSocket object.

**def get_exchanges()**
^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get the list of subscribed exchanges.

On successful execution **on_message_get_exchanges(list_exchanges)** callback is fired.
    **list_exchanges** : The list of subscribed exchanges.

**Sample Response:**

 .. sourcecode:: json

  {
   "Result":[
   {"Value":"MCX"},
   {"Value":"NFO"},
   {"Value":"NSE"}],
   "MessageType":"ExchangesResult"
   }

**def get_instruments_on_search(self, exchange, key_word)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get the list of instruments using search key word.

On successful execution **on_message_instruments_on_search(list_instruments)** callback is fired.
**list_instruments** : The list of instruments matching the search word.

**Sample Response:**

.. sourcecode:: json

 {
 "Request":{
 "Exchange":"NFO",
 "Search":"NIF",
 "MessageType":"GetInstrumentsOnSearch"
 },
 "Result":[
 {"Identifier":"OPTIDX_NIFTY_28DEC2017_CE_10000","Name":"OPTIDX","Expiry":"28Dec2017","StrikePrice":10000.0,"Product":"NIFTY","PriceQuotationUnit":"","OptionType":"CE","ProductMonth":"28Dec2017","UnderlyingAsset":"","UnderlyingAssetExpiry":"","IndexName":""}
 {"Identifier":"OPTIDX_NIFTY_28DEC2017_PE_8500","Name":"OPTIDX","Expiry":"28Dec2017","StrikePrice":8500.0,"Product":"NIFTY","PriceQuotationUnit":"","OptionType":"PE","ProductMonth":"28Dec2017","UnderlyingAsset":"","UnderlyingAssetExpiry":"","IndexName":""}
 ],
 "MessageType":"InstrumentsOnSearchResult"
 }


**def get_instruments(self, exchange, instrument_type=None, product=None, expiry=None,option_type=None,strike_price=None)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get the list of instruments from an exchange.

On successful execution **on_message_instruments(list_instruments)** callback is fired.

**list_instruments** : The list of instruments.

**Sample Response:**

.. sourcecode:: json

 {
 "Request":{
 "Exchange":"NFO",
 "MessageType":"GetInstruments"
 },
 "Result":[
 {"Identifier":"OPTIDX_NIFTY_28DEC2017_CE_10000","Name":"OPTIDX","Expiry":"28Dec2017","StrikePrice":10000.0,"Product":"NIFTY","PriceQuotationUnit":"","OptionType":"CE","ProductMonth":"28Dec2017","UnderlyingAsset":"","UnderlyingAssetExpiry":"","IndexName":""}
 {"Identifier":"OPTIDX_NIFTY_28DEC2017_PE_8500","Name":"OPTIDX","Expiry":"28Dec2017","StrikePrice":8500.0,"Product":"NIFTY","PriceQuotationUnit":"","OptionType":"PE","ProductMonth":"28Dec2017","UnderlyingAsset":"","UnderlyingAssetExpiry":"","IndexName":""}
 ..........................
 ...........................
 ],
 "MessageType":"InstrumentsResult"
 }


**def get_last_quote(self, exchange, instrument_identifier)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get the last quote of an instrument.

On successful execution **on_message_last_quote(l_quote)** callback is fired.

**l_quote** : The last quote of the given instrument.

**Sample Response:**

.. sourcecode:: json

 {
 "Exchange":"NSE",
 "InstrumentIdentifier":"SBIN",
 "LastTradeTime":1508320899,
 "ServerTime":1508320899,
 "AverageTradedPrice":243.81,
 "BuyPrice":243.2,
 "BuyQty":36000,
 "Close":244.75,
 "High":244.6,
 "Low":243.0,
 "LastTradePrice":243.2,
 "LastTradeQty":0,
 "Open":244.35,
 "OpenInterest":50052000,
 "SellPrice":243.3,
 "SellQty":24000,
 "TotalQtyTraded":12864000,
 "Value":563571840.0,
 "PreOpen":false,
 "MessageType":"LastQuoteResult"
 }

**def get_last_quote_array(self, exchange, instrument_identifiers)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get the last quotes of given instruments.

On successful execution **on_message_last_quote_array(l_quote_array)** callback is fired.

**l_quote_array** : The last quotes of the given instruments.

**Sample Response:**

.. sourcecode:: json

 {
 "Result":[
 {"Exchange":"NSE","InstrumentIdentifier":"SBIN","LastTradeTime":15363
 16145,"ServerTime":1536316145,"AverageTradedPrice":291.74,"BuyPrice":0.0,"BuyQty
 ":0,"Close":291.65,"High":295.9,"Low":289.45,"LastTradePrice":291.65,"LastTradeQ
 ty":0,"Open":295.9,"OpenInterest":0,"QuotationLot":1.0,"SellPrice":291.65,"SellQ
 ty":30531,"TotalQtyTraded":23716678,"Value":6919103639.72,"PreOpen":false,"Messa
 geType":"LastQuoteResult"},

 {"Exchange":"NSE","InstrumentIdentifier":"INFY","Last
 TradeTime":1536316142,"ServerTime":1536316142,"AverageTradedPrice":730.95,"BuyPr
 ice":732.8,"BuyQty":3128,"Close":732.8,"High":735.15,"Low":723.8,"LastTradePrice
 ":732.8,"LastTradeQty":0,"Open":734.35,"OpenInterest":0,"QuotationLot":1.0,"Sell
 Price":0.0,"SellQty":0,"TotalQtyTraded":6510605,"Value":4758926724.75,"PreOpen":
 false,"MessageType":"LastQuoteResult"},

 {"Exchange":"NSE","InstrumentIdentifier":
 "BEPL","LastTradeTime":1536315602,"ServerTime":1536315601,"AverageTradedPrice":1
 25.92,"BuyPrice":0.0,"BuyQty":0,"Close":126.35,"High":127.4,"Low":124.6,"LastTra
 dePrice":126.35,"LastTradeQty":0,"Open":127.0,"OpenInterest":0,"QuotationLot":1.
 0,"SellPrice":126.35,"SellQty":9,"TotalQtyTraded":242004,"Value":30473143.68,"Pr
 eOpen":false,"MessageType":"LastQuoteResult"}],

 "MessageType":"LastQuoteArrayResult"
 }

**def get_snapshot(self, exchange, instrument_identifiers, periodicity=Constants.MINUTE, period=1)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get the snapshot quotes of given instruments.

On successful execution **on_message_snapshot_data(s_data)** callback is fired.

**l_data** : The snapshot quotes of the given instruments.

**Sample Response:**

.. sourcecode:: json

 {
 "Result":[
 {"InstrumentIdentifier":"BEPL","Exchange":"NSE","LastTradeTime":15363
 09000,"TradedQty":46846,"OpenInterest":0,"Open":125.65,"High":126.9,"Low":125.5,
 "Close":126.4},

 {"InstrumentIdentifier":"SBIN","Exchange":"NSE","LastTradeTime":1
 536309000,"TradedQty":5417972,"OpenInterest":0,"Open":291.1,"High":292.8,"Low":2
 89.5,"Close":292.4},

 {"InstrumentIdentifier":"INFY","Exchange":"NSE","LastTradeTi
 me":1536309000,"TradedQty":651205,"OpenInterest":0,"Open":732.25,"High":733.65,"
 Low":730.55,"Close":731.45}],

 "MessageType":"SnapshotResult"
 }

**def get_historical_tick_data(self,  exchange, instrument_identifier,max_no=0, from_timestamp=None, to_timestamp=None)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get historical tick data of the given instruments.

On successful execution **on_message_historical_tick_data(h_t_d)** callback is fired.

**h_t_d** : The historical tick data  of the given instrument.

**Sample Response:**

.. sourcecode:: json

 {
 "Result":[
 ......................................
 {"LastTradeTime":1536205500,"LastTradePrice":298.0,"QuotationLot":1,"TradedQty":0,"OpenInterest":0,"BuyPrice":298.1,"BuyQty
 ":2980,"SellPrice":298.45,"SellQty":1835},

 {"LastTradeTime":1536205500,"LastTradePrice":299.0,"QuotationLot":1,"TradedQty":0,"OpenInterest":0,"BuyPrice":298.1,"B
 uyQty":2980,"SellPrice":298.45,"SellQty":1835},

 {"LastTradeTime":1536205500,"LastTradePrice":298.1,"QuotationLot":1,"TradedQty":0,"OpenInterest":0,"BuyPrice":298
 .1,"BuyQty":2980,"SellPrice":298.45,"SellQty":1835},

 {"LastTradeTime":1536205500,"LastTradePrice":298.0,"QuotationLot":1,"TradedQty":34510,"OpenInterest":0,"BuyP
 rice":298.1,"BuyQty":2980,"SellPrice":298.45,"SellQty":1835}],

 "MessageType":"HistoryTickResult"}

**get_historical_ohlc_data(self, exchange, instrument_identifier, periodicity,from_timestamp, to_timestamp, max_no=0)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get historical ohlc data of the given instruments.

On successful execution **on_message_historical_ohlc_data(h_ohlc_d)** callback is fired.

**h_ohlc_d** : The historical tick data  of the given instrument.

**Sample Response:**

.. sourcecode:: json

 {"Request":{"Exchange":"NSE","InstrumentIdentifier":"SBIN","From":1536019200,"To
 ":1536477902,"Max":0,"Periodicity":"DAY","Period":0,"MessageType":"GetHistory"},
 "Result":[
 {"LastTradeTime":1536280200,"QuotationLot":1,"TradedQty":23716678,"Ope
 nInterest":0,"Open":295.9,"High":295.9,"Low":289.45,"Close":291.65},

 {"LastTradeTime":1536193800,"QuotationLot":1,"TradedQty":18001336,"OpenInterest":0,"Open":29
 8.0,"High":299.85,"Low":294.5,"Close":296.45},

 {"LastTradeTime":1536107400,"Quota
 tionLot":1,"TradedQty":22922686,"OpenInterest":0,"Open":296.5,"High":298.85,"Low
 ":290.4,"Close":296.55},

 {"LastTradeTime":1536021000,"QuotationLot":1,"TradedQty"
 :42859084,"OpenInterest":0,"Open":306.8,"High":307.45,"Low":295.45,"Close":296.4
 }],

 "MessageType":"HistoryOHLCResult"}

**def get_instrument_types(self, exchange)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Call this method to get the list of instrument types available for an exchange.

On successful execution **on_message_instrument_types(i_types)** callback is fired.

**i_types** : The list of instrument types.

**Sample Response:**

.. sourcecode:: json

 {"Request":{"Exchange":"NFO","MessageType":"GetInstrumentTypes"},
 "Result":[
 {"Value":"FUTIDX"},
 {"Value":"FUTIVX"},
 {"Value":"FUTSTK"},
 {"Value":"OPTIDX"},
 {"Value":"OPTSTK"}],
 "MessageType":"InstrumentTypesResult"}

**def get_products(self, exchange, instrument_type=None)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Call this method to get the list of products available for an exchange.

On successful execution **on_message_product(p)** callback is fired.

**p** : The list of products.

**Sample Response:**

.. sourcecode:: json

 {"Request":{"Exchange":"NFO","MessageType":"GetProducts"},
 "Result":[
 {"Value":"BANKNIFTY"},{"Value":"FTSE100"},{"Value":"NIFTYCPSE"},{"Value":"NIFTYINFRA"},{"Val
 ue":"NIFTYIT"},{"Value":"NIFTYMID50"},{"Value":"NIFTYPSE"},{"Value":"NIFTY"},{"V
 alue":"INDIAVIX"},{"Value":"ACC"},
 ................................
 ],
 "MessageType":"ProductsResult"}

**def get_expiry_dates(self, exchange, instrument_type=None, product=None)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Call this method to get the list of expiry dates of different contracts for an exchange.

On successful execution **on_message_expiry_dates(e_dates)** callback is fired.

**e_dates** : The list of expiry dates.

**Sample Response:**

.. sourcecode:: json

 {"Request":{"Exchange":"NFO","InstrumentType":"FUTIDX","Product":"BANKNIFTY","Me
 ssageType":"GetExpiryDates"},
 "Result":[{"Value":"25OCT2018"},{"Value":"27SEP2018
 "},{"Value":"29NOV2018"}],"MessageType":"ExpiryDatesResult"}

**def get_option_types(self, exchange, instrument_type=None, product=None , expiry=None)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Call this method to get the list of option types available for different contracts for an exchange.

On successful execution **on_message_option_types(o_types)** callback is fired.

**o_types** : The list of option types.

**Sample Response:**

.. sourcecode:: json

 {"Request":{"Exchange":"NFO","InstrumentType":"FUTIDX","Product":"BANKNIFTY","Ex
 piry":"25OCT2018","MessageType":"GetOptionTypes"},"Result":[{"Value":"FF"},{"Val
 ue":"XX"}],"MessageType":"OptionTypesResult"}

**def get_strike_prices(self, exchange, instrument_type=None, product=None, expiry=None, option_type=None)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Call this method to get the list of strike prices for different contracts for an exchange.

On successful execution **on_message_strike_prices(s_prices)** callback is fired.

**s_prices** : The list of strike prices.

**Sample Response:**

.. sourcecode:: json

 {"Request":{"Exchange":"NFO","MessageType":"GetStrikePrices"},"Result":[{"Value"
 :"0"},{"Value":"25800"},{"Value":"25900"},{"Value":"26000"},{"Value":"26100"},{"
 Value":"26200"},{"Value":"26300"},{"Value":"26400"},{"Value":"26500"},
 ............................
 ],
 "MessageType":"StrikePricesResult"}

**def get_limitations(self)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get your account details and limitations.

On successful execution **on_message_account_limitations(a_limit)** callback is fired.

**a_limit** : Account details and limitations.

**Sample Response:**

.. sourcecode:: json

 {"GeneralParams":{"AllowedBandwidthPerHour":-1.0,"AllowedCallsPerHour":7200,"All
 owedCallsPerMonth":5356800,"AllowedBandwidthPerMonth":-1.0,"ExpirationDate":1538
 159399,"Enabled":true},
 "AllowedExchanges":[{"AllowedInstruments":200,"DataDelay"
 :0,"ExchangeName":"CDS"},{"AllowedInstruments":200,"DataDelay":0,"ExchangeName":
 "MCX"},{"AllowedInstruments":200,"DataDelay":0,"ExchangeName":"NFO"},{"AllowedIn
 struments":160,"DataDelay":0,"ExchangeName":"NSE"},{"AllowedInstruments":40,"Dat
 aDelay":0,"ExchangeName":"NSE_IDX"}],
 "AllowedFunctions":[{"FunctionName":"GetExchangeMessages","IsEnabled":false},
 {"FunctionName":"GetHistory","IsEnabled":true}
 ,{"FunctionName":"GetLastQuote","IsEnabled":false},{"FunctionName":"GetLastQuote
 Array","IsEnabled":false},{"FunctionName":"GetLastQuoteArrayShort","IsEnabled":f
 alse},{"FunctionName":"GetLastQuoteShort","IsEnabled":false},{"FunctionName":"Ge
 tMarketMessages","IsEnabled":false},{"FunctionName":"GetSnapshot","IsEnabled":tr
 ue},{"FunctionName":"SubscribeRealtime","IsEnabled":false},{"FunctionName":"Subs
 cribeSnapshot","IsEnabled":false}],
 "HistoryLimitation":{"TickEnabled":true,"DayE
 nabled":true,"WeekEnabled":true,"MonthEnabled":true,"MaxEOD":100000,"MaxIntraday
 ":44,"Hour_1Enabled":true,"Hour_2Enabled":true,"Hour_3Enabled":true,"Hour_4Enabl
 ed":true,"Hour_6Enabled":true,"Hour_8Enabled":true,"Hour_12Enabled":true,"Minute
 _1Enabled":true,"Minute_2Enabled":true,"Minute_3Enabled":true,"Minute_4Enabled":
 true,"Minute_5Enabled":true,"Minute_6Enabled":true,"Minute_10Enabled":true,"Minu
 te_12Enabled":true,"Minute_15Enabled":true,"Minute_20Enabled":true,"Minute_30Ena
 bled":true,"MaxTicks":2},
 "MessageType":"LimitationResult"}

**def get_market_message(self, exchange)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get the market message for the given exchange.

On successful execution **on_message_market_message(m_m)** callback is fired.

**m_m** : The market message.

**Sample Response:**

.. sourcecode:: json

 {"Request":{"Exchange":"NFO","MessageType":"GetMarketMessages"},
 "Result":[{"ServerTime":1536314399,"SessionID":0,"MarketType":"Normal Market Close","MessageType
 ":"MarketMessagesItemResult"}],
 "MessageType":"MarketMessagesResult"}

**def get_exchange_message(self, exchange)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to get the exchange message for the given exchange.

On successful execution **on_message_exchange_message(e_m)** callback is fired.

**e_m** : The exchange message.

**Sample Response:**

.. sourcecode:: json

 {
 "Request":{
 "Exchange":"NFO",
 "MessageType":"GetExchangeMessages"
 },
 "Result":[
 {"ServerTime":1391822398,"Identifier":"Market","Message":"Members are requested to note that  ...","MessageType":"ExchangeMessagesItemResult"},
 {"ServerTime":1391822399,"Identifier":"Market","Message":"2013 shall be levied subsequently.","MessageType":"ExchangeMessagesItemResult"}
 ],
 "MessageType":"ExchangeMessagesResult"
 }

**def subscribe_realtime(self, exchange, instrument_identifier, unsubscribe=False)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to subscribe to real time data for the given exchange and given instrument.

On successful execution **on_message_realtime_data(r_r)** callback is fired.

**r_r** : The real time data.

**Sample Response:**

.. sourcecode:: json

 {"Exchange":"NSE","InstrumentIdentifier":"SBIN","LastTradeTime":1536558991,"Serv
 erTime":1536558991,"AverageTradedPrice":291.31,"BuyPrice":290.15,"BuyQty":5441,"
 Close":291.65,"High":293.25,"Low":289.15,"LastTradePrice":290.2,"LastTradeQty":3
 23,"Open":290.65,"OpenInterest":0,"QuotationLot":0.0,"SellPrice":290.3,"SellQty"
 :551,"TotalQtyTraded":7422459,"Value":2162236531.29,"PreOpen":false,"MessageType
 ":"RealtimeResult"}

 ..............................

**subscribe_realtime_snapshot(self, exchange, instrument_identifier, periodicity, unsubscribe=False)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to subscribe to real time snapshot data for the given exchange, given instrument and given periodicity.

On successful execution **on_message_realtime_snapshot_data(r_r)** callback is fired.

**r_r** : The real time snapshot data.

**Sample Response:**

.. sourcecode:: json

 {"Exchange":"NSE","InstrumentIdentifier":"SBIN","Periodicity":"MINUTE","LastTrad
 eTime":1536559380,"TradedQty":58767,"OpenInterest":0,"Open":290.4,"High":290.4,"
 Low":289.95,"Close":290.15,"MessageType":"RealtimeSnapshotResult"}

 ..............................

**def disconnect(self)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Call this method to disconnect the client.

On disconnection **on_close(base_client, code, reason)** callback is fired.

**Others**
^^^^^^^^^^^^^^
The client will automatically try to reconnect  to the server. On reconnection the **on_reconnect(self, attempts_count)**
will be fired.

If maximum number of reconnection attempts have been exhausted the **on_reconnection_max_tries()** callback will be fired. 

To get more details about the methods and their parameters visit `here <DhelmGfeedClient.html#module-DhelmGfeedClient.gfeedclient>`_

Example usage
=============

.. sourcecode:: python

 from DhelmGfeedClient.gfeedclient import GfeedClient
 from DhelmGfeedClient.constants import Constants
 import json
 import time
 import datetime

 #<ws_url> : Replace <ws_url> with the web socket url
 #<api_key> : Replace <api_key> with your api key which you have got on subscription.
 client = GfeedClient("<ws_url>","<api_key>")

 #Sample implementation of callback on successful authentication. Inside this method you have to call the relevant method to
 #retrive data from web socket.
 def on_authenticated(base_client):
    #Retrieve the list of subscribed exchanges. On successful data retrieval the callback `on_message_get_exchanges`(in this sample example)
    #will be called.
    base_client.get_exchanges()
    #Retrieve the list of instruments using search key "SBIN" from exchange "NSE".
    #Respective callback in example : on_message_instruments_on_search
    base_client.get_instruments_on_search("NSE", "SBIN")
    #Retrieve the list of all instruments from exchange "NSE".
    #Respective callback in example : on_message_instruments
    base_client.get_instruments("NSE")
    #Retrieve the last quote of "SBIN" from exchange "NSE".
    #Respective callback in example : on_message_last_quote_array
    base_client.get_last_quote("NSE", "SBIN")
    #Retrieve the last quotes of "SBIN","BEPL" and "INFY" in one call from exchange "NSE".
    #Respective callback in example : on_message_last_quote_array
    base_client.get_last_quotes_array("NSE", ["SBIN", "BEPL", "INFY"])
    #Retrieve the snapshot quote of "SBIN", "BEPL" and "INFY" from exchange "NSE".
    #Respective callback in example :  on_message_snapshot_data
    base_client.get_snapshot("NSE", ["SBIN", "BEPL", "INFY"])
    #Retrieve the types of instruments available from exchange "NFO".
    #Respective callback in example : on_message_instrument_types
    base_client.get_instrument_types("NFO")
    #Retrieve the type of products of  from exchange "NFO" where instrument type is "FUTIDX".
    #Respective callback in example : on_message_products
    base_client.get_products("NFO", "FUTIDX")
    #Retrieve the expiry dates of contracts  from exchange "NFO" where instrument type is "FUTIDX" and product is "NIFTY".
    #Respective callback in example : on_message_expiry_dates
    base_client.get_expiry_dates("NFO", "FUTIDX", "NIFTY")
    #Retrieve the option types from exchange "NFO" where instrument type is "FUTIDX", product is "NIFTY" and expiry date is "25OCT2018".
    #Respective callback in example : on_message_option_types
    base_client.get_option_types("NFO", "FUTIDX", "NIFTY", "25OCT2018")
    #Retrieve the strike prices from exchange "NFO" where instrument type is "FUTIDX", product is "NIFTY" and expiry date is "25OCT2018"
    #Respective callback in example : on_message_strike_prices
    base_client.get_strike_prices("NFO", "FUTIDX", "NIFTY", "25OCT2018")
    #Retrieve your account details and limitations.
    #Respective callback in example : on_message_account_limitations
    base_client.get_limitations()
    #Retrieve the market message for exchange "NSE"
    #Respective callback in example : on_message_market_message
    base_client.get_market_message("NSE")
    #Retrieve the exchange message for exchange "NSE"
    #Respective callback in example : on_message_exchange_message
    base_client.get_exchange_message("NSE")
    #Retrieve the real time data for "SBIN" for exchange "NSE"
    #Respective callback in example : on_message_realtime_data
    base_client.subscribe_realtime("NSE", "SBIN")
    #Retrieve the real  time snapshot data for "SBIN" for exchange "NSE"
    #Respective callback in example : on_message_realtime_snapshot_data
    base_client.subscribe_realtime_snapshot("NSE", "SBIN", Constants.MINUTE)
    #Retrieve the last 10 historical tick data for "SBIN" for exchange "NSE"
    #Respective callback in example : on_message_historical_tick_data
    base_client.get_historical_tick_data("NSE", "SBIN", 10)
    #Retrieve the historical ohlc data for "SBIN" for exchange "NSE" from 13th September 2018 until now.
    #Respective callback in example : on_message_historical_ohlc_data
    base_client.get_historical_ohlc_data("NSE", "SBIN", Constants.HOUR,
                                int(time.mktime((datetime.datetime(2018, 9, 13)).timetuple())),
                                int(time.mktime((datetime.datetime.now()).timetuple())), 10)


 def on_message_get_exchanges(list_exchanages):
    print("\n*********LIST OF EXCHANGES*************\n")
    response = (json.loads(list_exchanages))
    print(response)
    print("\n")
    print(response['Result'])


 def on_message_instruments_on_search(list_instruments):
    print("\n*********LIST OF INSTRUMENTS*************\n")
    print(list_instruments)


 def on_message_instruments(list_instruments):
    print("\n*********LIST OF INSTRUMENTS*************\n")
    print(list_instruments)


 def on_message_last_quote(last_quote):
    print("\n*********LAST QUOTE*************\n")
    print(last_quote)


 def on_message_last_quote_array(last_quote_array):
    print("\n*********LAST QUOTE ARRAY*************\n")
    print(last_quote_array)


 def on_message_snapshot_data(snapshot_data):
    print("\n*********SNAPSHOT DATA*************\n")
    print(snapshot_data)


 def on_message_instrument_types(instrument_types):
    print("\n*********INSTRUMENT TYPES*************\n")
    print(instrument_types)


 def on_message_products(products):
    print("\n*********PRODUCTS*************\n")
    print(products)


 def on_message_expiry_dates(expiry_dates):
    print("\n*********EXPIRY DATES*************\n")
    print(expiry_dates)


 def on_message_option_types(option_types):
    print("\n*********OPTION TYPES*************\n")
    print(option_types)


 def on_message_strike_prices(strike_prices):
    print("\n*********STRIKE PRICES*************\n")
    print(strike_prices)


 def on_message_account_limitations(account_limitations):
    print("\n*********ACCOUNT LIMITATIONS*************\n")
    print(account_limitations)


 def on_message_market_message(market_message):
    print("\n*********MARKET MESSAGE*************\n")
    print(market_message)


 def on_message_exchange_message(exchange_message):
    print("\n*********EXCHANGE MESSAGE*************\n")
    print(exchange_message)


 def on_message_realtime_data(realtime_data):
    print("\n*********REALTIME DATA*************\n")
    print(realtime_data)


 def on_message_realtime_snapshot_data(realtime_snapshot_data):
    print("\n*********REALTIME SNAPSHOT DATA*************\n")
    print(realtime_snapshot_data)


 def on_message_historical_tick_data(historical_tick_data):
    print("\n*********HISTORICAL TICK DATA*************\n")
    print(historical_tick_data)


 def on_message_historical_ohlc_data(historical_ohlc_data):
    print("\n*********HISTORICAL OHLC DATA*************\n")
    print(historical_ohlc_data)

 def on_reconnect(count):
    print("\n+++++++Reconnected+++++++++\n")
    
 def on_reconnection_max_tries():
    print("+++MAX RECONNECT ATTEMPTS MADE++++")

 def on_close(base_client, code, reason):
    print("\n+++++++SUCCESFULLY DISCONNCTED+++++++++\n")

 #Assign your callbacks. Every callback has some specific functions.
 #This callback will be called when user will be authenticated after successful connection.
 #Once the user is authenticated then only other predefined methods to access data from web socket can be called from inside this callback.
 client.on_authenticated = on_authenticated

 #Callback to receive the list of subscribed exchanges.
 client.on_message_get_exchanges = on_message_get_exchanges

 #Callback to receive the list of instruments using search key.
 client.on_message_instruments_on_search = on_message_instruments_on_search

 #Callback to receive the list of instruments for a given exchange exchanges.
 client.on_message_instruments = on_message_instruments

 #Callback to receive the last quote of a given instrument
 client.on_message_last_quote = on_message_last_quote

 #Callback to receive the last quotes of a list of instruments.
 client.on_message_last_quote_array = on_message_last_quote_array

 #Callback to receive snapshot data of given instruments.
 client.on_message_snapshot_data = on_message_snapshot_data

 #Callback to receive the historical tick data of the given instruments
 client.on_message_historical_tick_data = on_message_historical_tick_data

 #Callback to receive the historical ohlc data of the given instruments
 client.on_message_historical_ohlc_data = on_message_historical_ohlc_data

 #Callback to receive the types of instruments available for an exchange.
 client.on_message_instrument_types = on_message_instrument_types

 #Callback to receive the list of products.
 client.on_message_product = on_message_products

 #Callback to receive the expiry dates.
 client.on_message_expiry_dates = on_message_expiry_dates

 #Callback to receive the option types.
 client.on_message_option_types = on_message_option_types

 #Callback to receive the strike prices.
 client.on_message_strike_prices = on_message_strike_prices

 #Callback to receive the account information.
 client.on_message_account_limitations = on_message_account_limitations

 #Callback to receive the market message.
 client.on_message_market_message = on_message_market_message

 #Callback to receive the exchange message.
 client.on_message_exchange_message = on_message_exchange_message

 #Callback to receive the real time data for the given instrument.
 client.on_message_realtime_data = on_message_realtime_data

 #Callback to receive the real time snapshot data for the given instrument.
 client.on_message_realtime_snapshot_data = on_message_realtime_snapshot_data

 #Callback on disconnection.
 client.on_close = on_close

 #Callback on reconnection.
 client.on_reconnect = on_reconnect

 #Callback on maximum retries for reconnection have been exhausted
 client.on_reconnection_max_tries = on_reconnection_max_tries

 #Connect to the web socket. You have to use the predefined callbacks to receive and process data.
 client.connect()


Notice
======
Dhelm® is a trademark of the KNC Solutions Private Limited.

Conclusion
==========

If you have any query feel free to email us at developer@kncsolutions.in.
Or you can raise an issue `here <https://github.com/kncsolutions/dhelm-gfeed-python-client/issues>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
