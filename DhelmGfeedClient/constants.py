# -*- coding: utf-8 -*-
"""
    **constants.py**

    - Copyright (c) 2018, KNC Solutions Private Limited.
    - License: 'Apache License, Version 2.0'.
    - version: 1.0.0
"""

class Constants:

    MAX_RETRIES = 30
    MAXDELAY = 5000
    TIMEOUT = 30
    TICK = "TICK"
    HOUR = "HOUR"
    MINUTE = "MINUTE"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"

    AUTHENTICATE = "Authenticate"
    GET_EXCHANGES = "GetExchanges"
    GET_INSTRUMENTS_ON_SEARCH = "GetInstrumentsOnSearch"
    GET_INSTRUMENTS = "GetInstruments"
    GET_LAST_QUOTE = "GetLastQuote"
    GET_LAST_QUOTE_ARRAY = "GetLastQuoteArray"
    GET_SNAPSHOT = "GetSnapshot"
    GET_HISTORY = "GetHistory"
    GET_INSTRUMENT_TYPES = "GetInstrumentTypes"
    GET_PRODUCTS = "GetProducts"
    GET_EXPIRY_DATES = "GetExpiryDates"
    GET_OPTION_TYPES = "GetOptionTypes"
    GET_STRIKE_PRICES = "GetStrikePrices"
    GET_LIMITATIONS = "GetLimitation"
    GET_SERVER_INFO = "GetServerInfo"
    GET_MARKET_MESSAGE = "GetMarketMessages"
    GET_EXCHANGE_MESSAGE = "GetExchangeMessages"
    SUBSCRIBE_REAL_TIME = "SubscribeRealtime"
    SUBSCRIBE_SNAPSHOT = "SubscribeSnapshot"

    MESSAGE_EXCHANGE_RESULT = "ExchangesResult"
    MESSAGE_INSTRUMENTS_ON_SEARCH_RESULT = "InstrumentsOnSearchResult"
    MESSAGE_INSTRUMENTS_RESULT = "InstrumentsResult"
    MESSAGE_LAST_QUOTE_RESULT = "LastQuoteResult"
    MESSAGE_LAST_QUOTE_ARRAY_RESULT = "LastQuoteArrayResult"
    MESSAGE_SNAPSHOT_RESULT = "SnapshotResult"
    MESSAGE_HISTORY_TICK_RESULT = "HistoryTickResult"
    MESSAGE_HISTORY_OHLC_RESULT = "HistoryOHLCResult"
    MESSAGE_INSTRUMENT_TYPES_RESULT = "InstrumentTypesResult"
    MESSAGE_PRODUCTS_RESULT = "ProductsResult"
    MESSAGE_EXPIRY_DATE_RESULT = "ExpiryDatesResult"
    MESSAGE_OPTION_TYPES_RESULT = "OptionTypesResult"
    MESSAGE_STRIKE_PRICES_RESULT = "StrikePricesResult"
    MESSAGE_LIMITATION_RESULT = "LimitationResult"
    MESSAGE_SERVER_INFO_RESULT = "ServerInfoResult"
    MESSAGE_MARKET_MESSAGE_RESULT = "MarketMessagesResult"
    MESSAGE_EXCHANGE_MESSAGE_RESULT = "ExchangeMessagesResult"
    MESSAGE_REAL_TIME_RESULT = "RealtimeResult"
    MESSAGE_REAL_TIME_SNAPSHOT_RESULT = "RealtimeSnapshotResult"
    RESULT_NOT_PREPARED = '{"Message:ResponseNotAvailable"}'
