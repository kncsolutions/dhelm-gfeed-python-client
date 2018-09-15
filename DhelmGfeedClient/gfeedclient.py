
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

        # Variables containing response
        self.subscribe_exchanges = Constants.RESULT_NOT_PREPARED
        self.instrument_list_on_search = Constants.RESULT_NOT_PREPARED

    def connect(self, proxy = None):
        """
        Establishes a web socket connection.
        """
        self.factory = _GfeedClientFactory(self.ws_url, proxy = proxy)
        self.factory.on_open = self._on_open
        self.factory.on_close = self._on_close
        self.factory.on_message = self._on_message
        self.factory.on_authenticated = self._on_authenticated
        self.factory.on_connect = self._on_connect
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
            print(str_message)

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

    def _on_close(self):
        """on close"""

    def _on_message(self,base_client, payload, isBinary):
        """on message"""
        message = format(payload.decode('utf8'))
        # print(message)
        if message.find("\"Complete\":true") != -1 or message.find("\"AllowVMRunning\":false") != -1 \
                or message.find("\"AllowServerOSRunning\":false") != -1:
                    print(message)
                    self.is_authenticated = True
                    self.base_client = base_client
                    self._on_authenticated()
        elif message.find(Constants.MESSAGE_EXCHANGE_RESULT) != -1:
            self.subscribe_exchanges = message
            print(self.subscribe_exchanges)
        elif message.find(Constants.MESSAGE_INSTRUMENTS_ON_SEARCH_RESULT) != -1:
            self.instrument_list_on_search = message
            print(self.instrument_list_on_search)







