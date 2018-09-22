# -*- coding: utf-8 -*-
"""
    **gfeedclient.py**

    - Copyright (c) 2018, KNC Solutions Private Limited.
    - License: 'Apache License, Version 2.0'.
    - version: 1.0.0
"""
from twisted.python import log
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory,connectWS
from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from DhelmGfeedClient.constants import Constants
import json
import sys




class _GfeedClientProtocol(WebSocketClientProtocol):
    """
       The client protocol
    """

    def __init__(self, *args, **kwargs):
        super(_GfeedClientProtocol, self).__init__(*args, **kwargs)

    def onConnect(self, response):
        """Called when WebSocket server connection was established"""
        self.factory.base_client = self
        if self.factory.on_connect:
            self.factory.on_connect(self, response)
        self.factory.resetDelay()

    def onOpen(self):
        if self.factory.on_open:
            self.factory.on_open(self)

    def onMessage(self, payload, isBinary):
        if self.factory.on_message:
            self.factory.on_message(self, payload, isBinary)

    def onClose(self, wasClean, code, reason):
        if not wasClean:
            if self.factory.on_error:
                self.factory.on_error(self, code, reason)
        if self.factory.on_close:
            self.factory.on_close(self, code, reason)


class _GfeedClientFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol = _GfeedClientProtocol
    maxDelay = 10
    maxRetries = 5

    def __init__(self, *args, **kwargs):
        self.base_client = None
        self.on_open = None
        self.on_error = None
        self.on_close = None
        self.on_connect = None
        self.on_reconnect = None
        self.on_reconnection_max_tries = None
        self.on_disconnect = None
        self.on_authenticated = None
        self.on_message = None
        self.on_message_get_exchanges = None
        self.on_message_instruments_on_search = None
        self.on_message_instruments = None
        self.on_message_last_quote = None
        self.on_message_last_quote_array = None
        self.on_message_snapshot_data = None
        self.on_message_historical_tick_data = None
        self.on_message_historical_ohlc_data = None
        self.on_message_instrument_types = None
        self.on_message_product = None
        self.on_message_expiry_dates = None
        self.on_message_option_types = None
        self.on_message_strike_prices = None
        self.on_message_account_limitations = None
        self.on_message_market_message = None
        self.on_message_exchange_message = None
        self.on_message_realtime_data = None
        self.on_message_realtime_snapshot_data = None

        WebSocketClientFactory.__init__(self, *args, **kwargs)

        def clientConnectionFailed(self, connector, reason):
            if self.on_reconnect:
                self.on_reconnect(self.retries)
            print("Client connection failed .. retrying ..")
            self.retry(connector)
            if self.maxRetries is not None and (self.retries > self.maxRetries):
                if self.on_reconnection_max_tries:
                    self.on_reconnection_max_tries()

        def clientConnectionLost(self, connector, reason):
            print("Client connection lost .. retrying ..")
            if self.retries > 0:
                if self.on_reconnect:
                   self.on_reconnect(self.retries)
            self.retry(connector)
            if self.maxRetries is not None and (self.retries > self.maxRetries):
                if self.on_reconnection_max_tries:
                    self.on_reconnection_max_tries()



class GfeedClient(object):
    """
       The  client to connect to Global datafeed websocket data.

       - **ws_url**: The web socket url.(required)
       - **param api_key**: Your api  key.(required)
       - **param debug**: By default false. Set true to run in debug mode.(optional)
       - **param reconnect**: By default true. Set false to off auto reconnection.(optional)
       - **param reconnect_max_tries**: Maximum no of retries.(optional)
       - **param reconnect_max_delay**: Maximum delay.(optional)
       - **param connect_timeout**: Connection delay.(optional)
    """

    def __init__(self, ws_url, api_key, debug=False, max_retries=Constants.MAX_RETRIES, max_delay=Constants.MAXDELAY,
                 connect_timeout=Constants.TIMEOUT):
        """

        """
        if (ws_url == ""):
            raise Exception("Web socket url cannot be null!")
        if(api_key==""):
            raise Exception("Api key cannot be null!");
       
        self.ws_url = ws_url
        self.api_key = api_key
        self.is_authenticated = False
        self.factory = None
        self.base_client = None
        self.connect_timeout = connect_timeout
        self.is_disconnected_by_user = False
        self.debug = debug
        self.max_retries = max_retries
        self.max_delay = max_delay

        # Placeholders for callbacks.
        self.on_open = None
        self.on_error = None
        self.on_close = None
        self.on_connect = None
        self.on_reconnect = None
        self.on_reconnection_max_tries = None
        self.on_disconnect = None
        self.on_authenticated = None
        self.on_message = None
        self.on_message_get_exchanges = None
        self.on_message_instruments_on_search = None
        self.on_message_instruments = None
        self.on_message_last_quote = None
        self.on_message_last_quote_array = None
        self.on_message_snapshot_data = None
        self.on_message_historical_tick_data = None
        self.on_message_historical_ohlc_data = None
        self.on_message_instrument_types = None
        self.on_message_product = None
        self.on_message_expiry_dates = None
        self.on_message_option_types = None
        self.on_message_strike_prices = None
        self.on_message_account_limitations = None
        self.on_message_market_message = None
        self.on_message_exchange_message = None
        self.on_message_realtime_data = None
        self.on_message_realtime_snapshot_data = None

        # Variables containing response
        self.subscribe_exchanges = Constants.RESULT_NOT_PREPARED
        self.instrument_list_on_search = Constants.RESULT_NOT_PREPARED
        self.instrument_list = Constants.RESULT_NOT_PREPARED
        self.last_quote = Constants.RESULT_NOT_PREPARED
        self.last_quote_array = Constants.RESULT_NOT_PREPARED
        self.snapshot_data = Constants.RESULT_NOT_PREPARED
        self.historical_tick_data = Constants.RESULT_NOT_PREPARED
        self.historical_ohlc_data = Constants.RESULT_NOT_PREPARED
        self.instrument_types = Constants.RESULT_NOT_PREPARED
        self.products = Constants.RESULT_NOT_PREPARED
        self.expiry_dates = Constants.RESULT_NOT_PREPARED
        self.option_types = Constants.RESULT_NOT_PREPARED
        self.strike_prices = Constants.RESULT_NOT_PREPARED
        self.account_limitations = Constants.RESULT_NOT_PREPARED
        self.market_message = Constants.RESULT_NOT_PREPARED
        self.exchange_message = Constants.RESULT_NOT_PREPARED
        self.realtime_result = Constants.RESULT_NOT_PREPARED
        self.realtime_snapshot_result = Constants.RESULT_NOT_PREPARED

    def connect(self):
        """
        Establishes a web socket connection.
        On successful authentication ``on_authenticated(base_client)`` callback is fired.
        The ``base_client`` is the currently initialised WebSocket object.
        """
        if self.debug:
            log.startLogging(sys.stdout)
        self.factory = _GfeedClientFactory(self.ws_url)
        self.factory.on_open = self._on_open
        self.factory.on_error = self._on_error
        self.factory.on_close = self._on_close
        self.factory.on_message = self._on_message
        self.factory.on_connect = self._on_connect
        self.factory.on_reconnect = self._on_reconnect
        self.factory.on_reconnection_max_tries = self._on_reconnection_max_tries
        self.factory.on_disconnect = self._on_disconnect
        self.factory.on_authenticated = self._on_authenticated
        self.factory.on_message_get_exchanges = self._on_message_get_exchanges
        self.factory.on_message_instruments_on_search = self._on_message_instruments_on_search
        self.factory.on_message_instruments = self._on_message_instruments
        self.factory.on_message_last_quote = self._on_message_last_quote
        self.factory.on_message_last_quote_array = self._on_message_last_quote_array
        self.factory.on_message_snapshot_data = self._on_message_snapshot_data
        self.factory.on_message_historical_tick_data = self._on_message_historical_tick_data
        self.factory.on_message_historical_ohlc_data = self._on_message_historical_ohlc_data
        self.factory.on_message_instrument_types =self._on_message_instrument_types
        self.factory.on_message_product = self._on_message_product
        self.factory.on_message_expiry_dates = self._on_message_expiry_dates
        self.factory.on_message_option_types = self._on_message_option_types
        self.factory.on_message_strike_prices = self._on_message_strike_prices
        self.factory.on_message_account_limitations = self._on_message_account_limitations
        self.factory.on_message_market_message = self._on_message_market_message
        self.factory.on_message_exchange_message = self._on_message_exchange_message
        self.factory.on_message_realtime_data = self._on_message_realtime_data
        self.factory.on_message_realtime_snapshot_data = self._on_message_realtime_snapshot_data
        if self.max_retries > 0:
            self.factory.maxRetries = self.max_retries
        if self.max_delay > 0:
            self.factory.maxDelay = self.max_delay

        connectWS(self.factory, timeout=self.connect_timeout)

        if not reactor.running:
            reactor.run()

    def disconnect(self):
        """
        Call this method to disconnect the client.

        On disconnection **on_close(base_client, code, reason)** callback is fired.
        """
        self.is_disconnected_by_user = True
        if self.factory:
            self.factory.stopTrying()
        if self.base_client:
            self.base_client.sendClose(code, reason)

    def is_connected(self):
        """Check if WebSocket connection is established."""
        if self.on_authenticated and self.base_client and self.base_client.state == self.base_client.STATE_OPEN:
            return True
        else:
            return False

    def _authenticate(self, base_client):
        str_message = '{"MessageType":"Authenticate","Password":"' + self.api_key + '"}'
        payload = str_message.encode('utf8')
        base_client.sendMessage(payload, isBinary=False)

    def get_exchanges(self):
        """
        Call this method to get the list of subscribed exchanges.

        On successful execution **on_message_get_exchanges(list_exchanges)** callback is fired.

        **list_exchanges** : The list of subscribed exchanges.
        """
        if self.is_authenticated:
            str_message = '{"MessageType":\"'+Constants.GET_EXCHANGES+'\"}'
            payload = str_message.encode('utf8')
            try:
                self.base_client.sendMessage(payload, isBinary=False)
            except ValueError:
                print("Cannot fetch valid exchange list now.")
        else:
            print("Not authenticated yet")

    def get_instruments_on_search(self, exchange, key_word):
        """
        Call this method to get the list of instruments using search key word.

        On successful execution **on_message_instruments_on_search(list_instruments)** callback is fired.

        **list_instruments** : The list of instruments matching the search word.

        :param exchange: The exchange(required)
        :param key_word: The search word(required).
        """
        if self.is_authenticated:
            str_message = {}
            str_message["MessageType"] = Constants.GET_INSTRUMENTS_ON_SEARCH
            str_message["Exchange"] = exchange
            str_message["Search"] = key_word
            payload = (json.dumps(str_message)).encode('utf8')
            self.base_client.sendMessage(payload, isBinary=False)

    def get_instruments(self, exchange, instrument_type=None, product=None, expiry=None,
                        option_type=None, strike_price=None):
        """
        Call this method to get the list of instruments from an exchange.

        On successful execution **on_message_instruments(list_instruments)** callback is fired.

        **list_instruments** : The list of instruments.

        :param exchange: The exchange(required)
        :param instrument_type: The type of the instrument, e.g. FUTIDX, OPTIDX etc(optional)
        :param product:  The product, e.g. NIFTY, BANKNIFTY etc(optional).
        :param expiry: The expiry date, e.g. 25OCT2018(optional).
        :param option_type: The option type, e.g. PE,CE(optional).
        :param strike_price: The strike price(optional).
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_INSTRUMENTS
        str_message["Exchange"] = exchange
        if instrument_type:
            str_message["InstrumentType"] = instrument_type
        if product:
            str_message["Product"] = product
        if expiry:
            str_message["Expiry"] = expiry
        if option_type:
            str_message["OptionType"] = option_type
        if strike_price:
            strike_price["StrikePrice"] = strike_price
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_last_quote(self, exchange, instrument_identifier):
        """
        Call this method to get the last quote of an instrument.

        On successful execution **on_message_last_quote(l_quote)** callback is fired.

        **l_quote** : The last quote of the given instrument.

        :param exchange: The exchange(required)
        :param instrument_identifier: The instrument identifier(required)
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_LAST_QUOTE
        str_message["Exchange"] = exchange
        str_message["InstrumentIdentifier"] = instrument_identifier
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_last_quotes_array(self, exchange, instrument_identifiers):
        """
        Call this method to get the last quotes of given instruments.

        On successful execution **on_message_last_quote_array(l_quote_array)** callback is fired.

        **l_quote_array** : The last quotes of the given instruments.

        :param exchange: The exchange(required)
        :param instrument_identifiers: The instrument identifiers(required)
        :return:
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_LAST_QUOTE_ARRAY
        str_message["Exchange"] = exchange
        instrument_identifiers_array= []
        for s in instrument_identifiers:
            item = {}
            item["Value"] = s
            instrument_identifiers_array.append(item)
        str_message["InstrumentIdentifiers"] = instrument_identifiers_array
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_snapshot(self, exchange, instrument_identifiers, periodicity=Constants.MINUTE, period=1):
        """
        Call this method to get the snapshot quotes of given instruments.

        On successful execution **on_message_snapshot_data(s_data)** callback is fired.

        **l_data** : The snapshot quotes of the given instruments.

        :param exchange: The exchange(required)
        :param instrument_identifiers: The instrument identifiers(required)
        :param periodicity: The periodicity/"HOUR" or "MINUTE"(optional).
        :param period: The period.E.g. 1,2,3 etc.(optional).
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_SNAPSHOT
        str_message["Exchange"] = exchange
        intrument_identifiers_array= []
        for s in instrument_identifiers:
            item = {}
            item["Value"] = s
            intrument_identifiers_array.append(item)
        str_message["InstrumentIdentifiers"] = intrument_identifiers_array
        str_message["Periodicity"] = periodicity
        str_message["Period"] = period
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_historical_tick_data(self,  exchange, instrument_identifier,
                                 max_no=0, from_timestamp=None, to_timestamp=None):
        """
        Call this method to get historical tick data of the given instruments.

        On successful execution **on_message_historical_tick_data(h_t_d)** callback is fired.

        **h_t_d** : The historical tick data  of the given instrument.

        :param exchange: The exchange(required)
        :param instrument_identifier: The instrument identifier(required).
        :param max_no: Numerical value of maximum records that should be returned(optional).
        :param from_timestamp: The from time in unix timestamp(optional).
        :param to_timestamp: The to time in unix timestamp(optional).
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_HISTORY
        str_message["Exchange"] = exchange
        str_message["InstrumentIdentifier"] = instrument_identifier
        if from_timestamp:
            str_message["From"] = from_timestamp
        if to_timestamp:
            str_message["To"] = to_timestamp
        str_message["Max"] = max_no
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_historical_ohlc_data(self, exchange, instrument_identifier, periodicity,
                                 from_timestamp, to_timestamp, max_no=0):
        """
        Call this method to get historical ohlc data of the given instruments.

        On successful execution **on_message_historical_ohlc_data(h_ohlc_d)** callback is fired.

        **h_ohlc_d** : The historical tick data  of the given instrument.

        :param exchange: The exchange(required)
        :param instrument_identifier: The instrument identifier(required).
        :param periodicity: "HOUR"."MINUTE"."DAY","WEEK", or "MONTH"(required).
        :param from_timestamp: The from time in unix timestamp(required).
        :param to_timestamp: The to time in unix timestamp(required).
        :param max_no: Numerical value of maximum records that should be returned(optional).
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_HISTORY
        str_message["Exchange"] = exchange
        str_message["InstrumentIdentifier"] = instrument_identifier
        str_message["Periodicity"] = periodicity
        str_message["From"] = from_timestamp
        str_message["To"] = to_timestamp
        str_message["Max"] = max_no
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_instrument_types(self, exchange):
        """
        Call this method to get the list of instrument types available for an exchange.

        On successful execution **on_message_instrument_types(i_types)** callback is fired.

        **i_types** : The list of instrument types.

        :param exchange: The exchange(required)
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_INSTRUMENT_TYPES
        str_message["Exchange"] = exchange
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_products(self, exchange, instrument_type=None):
        """
        Call this method to get the list of products available for an exchange.

        On successful execution **on_message_product(p)** callback is fired.

        **p** : The list of products.

        :param exchange: The exchange(required)
        :param instrument_type: The type of the instrument, e.g. FUTIDX, OPTIDX etc(optional)
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_PRODUCTS
        str_message["Exchange"] = exchange
        if instrument_type:
            str_message["InstrumentType"] = instrument_type
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_expiry_dates(self, exchange, instrument_type=None, product=None):
        """
        Call this method to get the list of expiry dates of different contracts for an exchange.

        On successful execution **on_message_expiry_dates(e_dates)** callback is fired.

        **e_dates** : The list of expiry dates.

        :param exchange: The exchange(required)
        :param instrument_type: The type of the instrument, e.g. FUTIDX, OPTIDX etc(optional)
        :param product:  The product, e.g. NIFTY,BANKNIFTY etc(optional).
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_EXPIRY_DATES
        str_message["Exchange"] = exchange
        if instrument_type:
            str_message["InstrumentType"] = instrument_type
        if product:
            str_message["Product"] = product
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_option_types(self, exchange, instrument_type=None, product=None , expiry=None):
        """
        Call this method to get the list of option types available for different contracts for an exchange.

        On successful execution **on_message_option_types(o_types)** callback is fired.

        **o_types** : The list of option types.

        :param exchange: The exchange(required)
        :param instrument_type: The type of the instrument, e.g. FUTIDX, OPTIDX etc(optional)
        :param product:  The product, e.g. NIFTY, BANKNIFTY etc(optional).
        :param expiry: The expiry date, e.g. 25OCT2018(optional).
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_OPTION_TYPES
        str_message["Exchange"] = exchange
        if instrument_type:
            str_message["InstrumentType"] = instrument_type
        if product:
            str_message["Product"] = product
        if expiry:
            str_message["Expiry"] = expiry
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_strike_prices(self, exchange, instrument_type=None, product=None, expiry=None, option_type=None):
        """
        Call this method to get the list of strike prices for different contracts for an exchange.

        On successful execution **on_message_strike_prices(s_prices)** callback is fired.

        **s_prices** : The list of strike prices.

        :param exchange: The exchange(required)
        :param instrument_type: The type of the instrument, e.g. FUTIDX, OPTIDX etc(optional)
        :param product:  The product, e.g. NIFTY, BANKNIFTY etc(optional).
        :param expiry: The expiry date, e.g. 25OCT2018(optional).
        :param option_type: The option type, e.g. PE,CE(optional).
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_STRIKE_PRICES
        str_message["Exchange"] = exchange
        if instrument_type:
            str_message["InstrumentType"] = instrument_type
        if product:
            str_message["Product"] = product
        if expiry:
            str_message["Expiry"] = expiry
        if option_type:
            str_message["OptionType"] = option_type
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_limitations(self):
        """
        Call this method to get your account details and limitations.

        On successful execution **on_message_account_limitations(a_limit)** callback is fired.

        **a_limit** : Account details and limitations.
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_LIMITATIONS
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_market_message(self, exchange):
        """
        Call this method to get the market message for the given exchange.

        On successful execution **on_message_market_message(m_m)** callback is fired.

        **m_m** : The market message.

        :param exchange: The exchange(required)
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_MARKET_MESSAGE
        str_message["Exchange"] = exchange
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_exchange_message(self, exchange):
        """
        Call this method to get the exchange message for the given exchange.

        On successful execution **on_message_exchange_message(e_m)** callback is fired.

        **e_m** : The exchange message.

        :param exchange: The exchange(required)
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_EXCHANGE_MESSAGE
        str_message["Exchange"] = exchange
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def subscribe_realtime(self, exchange, instrument_identifier, unsubscribe=False):
        """
        Call this method to subscribe to real time data for the given exchange and given instrument.

        On successful execution **on_message_realtime_data(r_r)** callback is fired.

        **r_r** : The real time data.

        :param exchange: The exchange(required)
        :param instrument_identifier: The instrument identifier(required)
        :param unsubscribe: Pass True to unsubscribe(optional)
        """
        str_message = {}
        str_message["MessageType"] = Constants.SUBSCRIBE_REAL_TIME
        str_message["Exchange"] = exchange
        str_message["InstrumentIdentifier"] = instrument_identifier
        if unsubscribe:
            str_message["Unsubscribe"] = unsubscribe
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def subscribe_realtime_snapshot(self, exchange, instrument_identifier, periodicity, unsubscribe=False):
        """
        Call this method to subscribe to real time snapshot data for the given exchange, given instrument and given periodicity.

        On successful execution **on_message_realtime_snapshot_data(r_r)** callback is fired.

        **r_r** : The real time snapshot data.

        :param exchange: The exchange(required)
        :param instrument_identifier: The instrument identifier(required)
        :param periodicity: The periodicity.Valid value is either "MINUTE" or "HOUR"(required).
        :param unsubscribe: Pass True to unsubscribe(optional)
        """
        str_message = {}
        str_message["MessageType"] = Constants.SUBSCRIBE_SNAPSHOT
        str_message["Exchange"] = exchange
        str_message["InstrumentIdentifier"] = instrument_identifier
        str_message["Periodicity"] = periodicity
        if unsubscribe:
            str_message["Unsubscribe"] = unsubscribe
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def _on_connect(self, base_client, response):
            self.base_client = base_client
            if self.on_connect:
                self.on_connect(self, response)

    def _on_open(self, base_client):
        self._authenticate(base_client)

    def _on_close(self, base_client, code, reason):
        if self.on_close:
            self.on_close(base_client, code, reason)

    def _on_error(self, base_client, code, reason):
        if self.on_error:
            self.on_error(self, code, reason)

    def _on_reconnect(self, attempts_count):
        if self.on_reconnect:
            self.on_reconnect(self, attempts_count)

    def _on_reconnect_max_tries(self):
        if self.on_reconnection_max_tries:
            self.on_reconnection_max_tries()

    def  _on_disconnect(self):
        if self.on_disconnect:
            self.on_disconnect(self)

    def _on_authenticated(self):
        if self.on_authenticated:
            self.on_authenticated(self)

    def _on_message_get_exchanges(self, list_exchanges):
        if self.on_message_get_exchanges:
            self.on_message_get_exchanges(list_exchanges)

    def _on_message_instruments_on_search(self, list_instruments):
        if self.on_message_instruments_on_search:
            self.on_message_instruments_on_search(list_instruments)

    def _on_message_instruments(self, list_instruments):
        if self.on_message_instruments:
            self.on_message_instruments(list_instruments)

    def _on_message_last_quote(self, l_quote):
        if self.on_message_last_quote:
            self.on_message_last_quote(l_quote)

    def _on_message_last_quote_array(self, l_quote_array):
        if self.on_message_last_quote_array:
            self.on_message_last_quote_array(l_quote_array)

    def _on_message_snapshot_data(self, s_data):
        if self.on_message_snapshot_data:
            self.on_message_snapshot_data(s_data)

    def _on_message_historical_tick_data(self, h_t_d):
        if self.on_message_historical_tick_data:
            self.on_message_historical_tick_data(h_t_d)

    def _on_message_historical_ohlc_data(self, h_ohlc_d):
        if self.on_message_historical_ohlc_data:
            self.on_message_historical_ohlc_data(h_ohlc_d)

    def _on_message_instrument_types(self,i_types):
        if self.on_message_instrument_types:
            self.on_message_instrument_types(i_types)

    def _on_message_product(self, p):
        if self.on_message_product:
            self.on_message_product(p)

    def _on_message_expiry_dates(self, e_dates):
        if self.on_message_expiry_dates:
            self.on_message_expiry_dates(e_dates)

    def _on_message_option_types(self, o_types):
        if self.on_message_option_types:
            self.on_message_option_types(o_types)

    def _on_message_strike_prices(self, s_prices):
        if self.on_message_strike_prices:
            self.on_message_strike_prices(s_prices)

    def _on_message_account_limitations(self, a_limit):
        if self.on_message_account_limitations:
            self.on_message_account_limitations(a_limit)

    def _on_message_market_message(self, m_m):
        if self.on_message_market_message:
            self.on_message_market_message(m_m)

    def _on_message_exchange_message(self, e_m):
        if self.on_message_exchange_message:
            self.on_message_exchange_message(e_m)

    def _on_message_realtime_data(self, r_r):
        if self.on_message_realtime_data:
            self.on_message_realtime_data(r_r)

    def _on_message_realtime_snapshot_data(self, r_r):
        if self.on_message_realtime_snapshot_data:
            self.on_message_realtime_snapshot_data(r_r)

    def _on_message(self,base_client, payload, isBinary):
        """on message"""
        message = format(payload.decode('utf8'))
        if message.find("\"Complete\":true") != -1 or message.find("\"AllowVMRunning\":false") != -1 \
                or message.find("\"AllowServerOSRunning\":false") != -1:
                    self.is_authenticated = True
                    self.base_client = base_client
                    self._on_authenticated()
        elif message.find(Constants.MESSAGE_EXCHANGE_RESULT) != -1:
            self.subscribe_exchanges = message
            self._on_message_get_exchanges(self.subscribe_exchanges)
        elif message.find(Constants.MESSAGE_INSTRUMENTS_ON_SEARCH_RESULT) != -1:
            self.instrument_list_on_search = message
            self._on_message_instruments_on_search(json.loads(self.instrument_list_on_search))
        elif message.find(Constants.MESSAGE_INSTRUMENTS_RESULT) != -1:
            self.instrument_list = message
            self._on_message_instruments(json.loads(self.instrument_list))
        elif message.find(Constants.MESSAGE_LAST_QUOTE_RESULT) != -1 and \
                json.loads(message)['MessageType'] == Constants.MESSAGE_LAST_QUOTE_RESULT:
            self.last_quote = message
            self._on_message_last_quote(json.loads(self.last_quote))
        elif message.find(Constants.MESSAGE_LAST_QUOTE_ARRAY_RESULT) != -1:
            self.last_quote_array = message
            self._on_message_last_quote_array(json.loads(self.last_quote_array))
        elif message.find(Constants.MESSAGE_SNAPSHOT_RESULT) != -1:
            self.snapshot_data = message
            self._on_message_snapshot_data(json.loads(self.snapshot_data))
        elif message.find(Constants.MESSAGE_HISTORY_TICK_RESULT) != -1:
            self.historical_tick_data = message
            self._on_message_historical_tick_data(json.loads(self.historical_tick_data))
        elif message.find(Constants.MESSAGE_HISTORY_OHLC_RESULT) != -1:
            self.historical_ohlc_data = message
            self._on_message_historical_ohlc_data(json.loads(self.historical_ohlc_data))
        elif message.find(Constants.MESSAGE_INSTRUMENT_TYPES_RESULT) != -1:
            self.instrument_types = message
            self._on_message_instrument_types(json.loads(self.instrument_types))
        elif message.find(Constants.MESSAGE_PRODUCTS_RESULT) != -1:
            self.products = message
            self._on_message_product(json.loads(self.products))
        elif message.find(Constants.MESSAGE_EXPIRY_DATE_RESULT) != -1:
            self.expiry_dates = message
            self._on_message_expiry_dates(json.loads(self.expiry_dates))
        elif message.find(Constants.MESSAGE_OPTION_TYPES_RESULT) != -1:
            self.option_types = message
            self._on_message_option_types(json.loads(self.option_types))
        elif message.find(Constants.MESSAGE_STRIKE_PRICES_RESULT) != -1:
            self.strike_prices = message
            self._on_message_strike_prices(json.loads(self.strike_prices))
        elif message.find(Constants.MESSAGE_LIMITATION_RESULT) != -1:
            self.account_limitations = message
            self._on_message_account_limitations(json.loads(self.account_limitations))
        elif message.find(Constants.MESSAGE_MARKET_MESSAGE_RESULT) != -1:
            self.market_message = message
            self._on_message_market_message(json.loads(self.market_message))
        elif message.find(Constants.MESSAGE_EXCHANGE_MESSAGE_RESULT) != -1:
            self.exchange_message = message
            self._on_message_exchange_message(json.loads(self.exchange_message))
        elif message.find(Constants.MESSAGE_REAL_TIME_RESULT) != -1:
            self.realtime_result = message
            self._on_message_realtime_data(json.loads(self.realtime_result))
        elif message.find(Constants.MESSAGE_REAL_TIME_SNAPSHOT_RESULT) != -1:
            self.realtime_snapshot_result = message
            self._on_message_realtime_snapshot_data(json.loads(self.realtime_snapshot_result))









