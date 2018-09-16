
import logging
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory,connectWS
from twisted.internet import reactor
from DhelmGfeedClient.constants import Constants
import json


log = logging.getLogger(__name__)


class _GfeedClientProtocol(WebSocketClientProtocol):
    """
       The client protocol
    """

    def __init__(self, *args, **kwargs):
        super(_GfeedClientProtocol, self).__init__(*args, **kwargs)

    def onConnect(self, response):
        """Called when WebSocket server connection was established"""
        print("Connected...")
        self.factory.base_client = self
        if self.factory.on_connect:
            self.factory.on_connect(self, response)

    def onOpen(self):
        print("opened")
        if self.factory.on_open:
            self.factory.on_open(self)

    def onMessage(self, payload, isBinary):
        if self.factory.on_message:
            self.factory.on_message(self, payload, isBinary)


class _GfeedClientFactory(WebSocketClientFactory):
    protocol = _GfeedClientProtocol

    def __init__(self, *args, **kwargs):
        self.base_client = None
        self.on_open = None
        self.on_close = None
        self.on_connect = None
        self.on_authenticated = None
        self.on_message = None
        self.on_message_get_exchanges = None
        self.on_message_instruments_on_search = None
        self.on_message_last_quote = None
        self.on_message_last_quote_array = None
        self.on_message_snapshot_data = None
        self.on_message_instrument_types = None
        self.on_message_product = None
        self.on_message_expiry_dates = None
        self.on_message_option_types = None
        self.on_message_strike_prices = None

        WebSocketClientFactory.__init__(self, *args, **kwargs)



class GfeedClient(object):
    """
       The WebSocket client for connecting to Kite Connect's streaming quotes service.
    """
    # Default connection timeout
    CONNECT_TIMEOUT = 30
    # Default Reconnect max delay.
    RECONNECT_MAX_DELAY = 60
    # Default reconnect attempts
    RECONNECT_MAX_TRIES = 50
    # Flag to set if its first connect
    _is_first_connect = True

    def __init__(self, ws_url, api_key, debug=False,
                 reconnect=True, reconnect_max_tries=RECONNECT_MAX_TRIES, reconnect_max_delay=RECONNECT_MAX_DELAY,
                 connect_timeout=CONNECT_TIMEOUT):
        """
        :param ws_url: The web socket url.
        :param api_key: Your api  key.
        :param debug: By default false. Set true to run in debug mode.
        :param reconnect: By default true. Set false to off auto reconnection.
        :param reconnect_max_tries:
        :param reconnect_max_delay:
        :param connect_timeout:
        """
        if (ws_url == ""):
            raise Exception("Web socket url cannot be null!")
        if(api_key==""):
            raise Exception("Api key cannot be null!");
        print(ws_url)
        self.ws_url = ws_url
        self.api_key = api_key
        self.is_authenticated = False
        self.factory = None
        self.base_client = None
        self.connect_timeout = connect_timeout

        # Placeholders for callbacks.
        self.on_open = None
        self.on_close = None
        self.on_connect = None
        self.on_authenticated = None
        self.on_message = None
        self.on_message_get_exchanges = None
        self.on_message_instruments_on_search = None
        self.on_message_last_quote = None
        self.on_message_last_quote_array = None
        self.on_message_snapshot_data = None
        self.on_message_instrument_types = None
        self.on_message_product = None
        self.on_message_expiry_dates = None
        self.on_message_option_types = None
        self.on_message_strike_prices = None

        # Variables containing response
        self.subscribe_exchanges = Constants.RESULT_NOT_PREPARED
        self.instrument_list_on_search = Constants.RESULT_NOT_PREPARED
        self.last_quote = Constants.RESULT_NOT_PREPARED
        self.last_quote_array = Constants.RESULT_NOT_PREPARED
        self.snapshot_data = Constants.RESULT_NOT_PREPARED
        self.instrument_types = Constants.RESULT_NOT_PREPARED
        self.products = Constants.RESULT_NOT_PREPARED
        self.expiry_dates = Constants.RESULT_NOT_PREPARED
        self.option_types = Constants.RESULT_NOT_PREPARED
        self.strike_prices = Constants.RESULT_NOT_PREPARED

    def connect(self, proxy = None):
        """
        Establishes a web socket connection.
        """
        self.factory = _GfeedClientFactory(self.ws_url, proxy = proxy)
        self.factory.on_open = self._on_open
        self.factory.on_close = self._on_close
        self.factory.on_message = self._on_message
        self.factory.on_connect = self._on_connect
        self.factory.on_authenticated = self._on_authenticated
        self.factory.on_message_get_exchanges = self._on_message_get_exchanges
        self.factory.on_message_instruments_on_search = self._on_message_instruments_on_search
        self.factory.on_message_last_quote = self._on_message_last_quote
        self.factory.on_message_last_quote_array = self._on_message_last_quote_array
        self.factory.on_message_snapshot_data = self._on_message_snapshot_data
        self.factory.on_message_instrument_types =self._on_message_instrument_types
        self.factory.on_message_product = self._on_message_product
        self.factory.on_message_expiry_dates = self._on_message_expiry_dates
        self.factory.on_message_option_types = self._on_message_option_types
        self.factory.on_message_strike_prices = self._on_message_strike_prices
        connectWS(self.factory, timeout=self.connect_timeout)
        reactor.run()

    def is_connected(self):
        """Check if WebSocket connection is established."""
        if self.on_authenticated and self.base_client and self.base_client.state == self.base_client.STATE_OPEN:
            return True
        else:
            return False

    def _authenticate(self, base_client):
        str_message = '{"MessageType":"Authenticate","Password":"' + self.api_key + '"}'
        print(str_message)
        payload = str_message.encode('utf8')
        base_client.sendMessage(payload, isBinary=False)

    def get_exchanges(self):
        if self.is_authenticated:
            str_message = '{"MessageType":\"'+Constants.GET_EXCHANGES+'\"}'
            print(str_message)
            payload = str_message.encode('utf8')
            try:
                self.base_client.sendMessage(payload, isBinary=False)
            except ValueError:
                print("Cannot fetch valid exchange list now.")
        else:
            print("Not authenticated yet")

    def get_instruments_on_search(self, exchange, key_word):
        """
        :param exchange: The exchange(required)
        :param key_word:The search word(required).
        :return:
        """
        if self.is_authenticated:
            str_message = {}
            str_message["MessageType"] = Constants.GET_INSTRUMENTS_ON_SEARCH
            str_message["Exchange"] = exchange
            str_message["Search"] = key_word
            payload = (json.dumps(str_message)).encode('utf8')
            self.base_client.sendMessage(payload, isBinary=False)

    def get_intruments(self):
        """
        """
    def get_last_quote(self, exchange, intrument_identifier):
        """
        :param exchange: The exchange(required)
        :param intrument_identifier: The instrument identifier(required)
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_LAST_QUOTE
        str_message["Exchange"] = exchange
        str_message["InstrumentIdentifier"] = intrument_identifier
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_last_quotes_array(self, exchange, instrument_identifiers):
        """
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
        :param exchange: The exchange(required)
        :param instrument_identifiers: The instrument identifiers(required)
        :param periodicity : The periodicity/"HOUR" or "MINUTE"(optional).
        :param period : The period.E.g. 1,2,3 etc.(optional).
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

    def get_historical_tick_data(self):
        """
        :return:
        """

    def get_historical_ohlc_data(self):
        """
        :return:
        """
    def get_instrument_types(self, exchange):
        """
        :param exchange : The exchange(required)
        """
        str_message = {}
        str_message["MessageType"] = Constants.GET_INSTRUMENT_TYPES
        str_message["Exchange"] = exchange
        payload = (json.dumps(str_message)).encode('utf8')
        self.base_client.sendMessage(payload, isBinary=False)

    def get_products(self, exchange, instrument_type=None):
        """
        :param exchange : The exchange(required)
        :param instrument_type : The type of the instrument, e.g. FUTIDX, OPTIDX etc(optional)
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
        :param exchange : The exchange(required)
        :param instrument_type : The type of the instrument, e.g. FUTIDX, OPTIDX etc(optional)
        :param product :  The product, e.g. NIFTY,BANKNIFTY etc(optional).
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
        :param exchange : The exchange(required)
        :param instrument_type : The type of the instrument, e.g. FUTIDX, OPTIDX etc(optional)
        :param product :  The product, e.g. NIFTY, BANKNIFTY etc(optional).
        :param expiry : The expiry date, e.g. 25OCT2018(optional).
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
        :param exchange : The exchange(required)
        :param instrument_type : The type of the instrument, e.g. FUTIDX, OPTIDX etc(optional)
        :param product :  The product, e.g. NIFTY, BANKNIFTY etc(optional).
        :param expiry : The expiry date, e.g. 25OCT2018(optional).
        :param option_type : The option type, e.g. PE,CE(optional).
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

    def _on_connect(self, base_client, response):
            self.base_client = base_client
            print("Base client assigned")
            if self.on_connect:
                self.on_connect(self, response)

    def _on_open(self, base_client):
        self._authenticate(base_client)

    def _on_authenticated(self):
        if self.on_authenticated:
            self.on_authenticated(self)

    def _on_message_get_exchanges(self, list_exchanges):
        if self.on_message_get_exchanges:
            self.on_message_get_exchanges(list_exchanges)

    def _on_message_instruments_on_search(self, list_instruments):
        if self.on_message_instruments_on_search:
            self.on_message_instruments_on_search(list_instruments)

    def _on_message_last_quote(self, l_quote):
        if self.on_message_last_quote:
            self.on_message_last_quote(l_quote)

    def _on_message_last_quote_array(self, l_quote_array):
        if self.on_message_last_quote_array:
            self.on_message_last_quote_array(l_quote_array)

    def _on_message_snapshot_data(self, s_data):
        if self.on_message_snapshot_data:
            self.on_message_snapshot_data(s_data)

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

    def _on_close(self):
        """on close"""

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








