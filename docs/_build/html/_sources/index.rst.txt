.. DhelmGfeedClient documentation master file, created by
   sphinx-quickstart on Thu Sep 20 11:04:01 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Dhelm-gfeed-python-client's documentation!
============================================

Dhelm-gfeed-python-client is a python client library to access and integrate stock market data from `Global Financial Datafeeds LLP <https://globaldatafeeds.in/>`_ with your  application.To use this library you must subscribe to web socket api with Global Financial Datafeeds LLP and get your API key and web socket endpoint URL.
Programmatic access to data  provides better and unique control over your algorithm. You access the raw data from your data provider, then feed into your own application and do whatever analysis you want in a unique way.


For detailed integration and usage guidelines, please read through the pages.

Installation
============

The client is tested with python 3.4+.

Install from Sources
--------------------
To install

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

1. ``def connect()`` : Call this method to connect to the web socket.

On successful authentication ``on_authenticated(base_client)`` callback is fired.
The ``base_client`` is the currently initialised WebSocket object.

2. ``def get_exchanges()`` : Call this method to get the list of subscribed exchanges.

 On successful execution ``on_message_get_exchanges(list_exchanges)`` callback is fired.
       ``list_exchanges`` : The list of subscribed exchanges.

Sample Response:

 .. sourcecode:: json

  {
   "Result":[
   {"Value":"MCX"},
   {"Value":"NFO"},
   {"Value":"NSE"}],
   "MessageType":"ExchangesResult"
   s}


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

 #Connect to the web socket. You have to use the predefined callbacks to receive and process data.
 client.connect()


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
