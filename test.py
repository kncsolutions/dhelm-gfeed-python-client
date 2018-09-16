from DhelmGfeedClient.gfeedclient import  GfeedClient
import  json
client = GfeedClient("ws://nimblestream.lisuns.com:4526","f31b6d7d-0138-428d-93ef-28acbd9632d2")


def on_authenticated(ws):
    ws.get_exchanges()
    ws.get_instruments_on_search("NSE", "SBIN")
    ws.get_last_quote("NSE", "SBIN")
    ws.get_last_quotes_array("NSE", ["SBIN", "BEPL", "INFY"])
    ws.get_snapshot("NSE", ["SBIN", "BEPL", "INFY"])
    ws.get_instrument_types("NFO")
    ws.get_products("NFO", "FUTIDX")
    ws.get_expiry_dates("NFO", "FUTIDX", "NIFTY")
    ws.get_option_types("NFO", "FUTIDX", "NIFTY", "25OCT2018")
    ws.get_strike_prices("NFO", "FUTIDX", "NIFTY", "25OCT2018")


def on_message_get_exchanges(list_exchanages):
    print("\n*********LIST OF EXCHANGES*************\n")
    response = (json.loads(list_exchanages))
    print(response)
    print("\n")
    print(response['Result'])


def on_message_instruments_on_search(list_instruments):
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


client.on_authenticated = on_authenticated
client.on_message_get_exchanges = on_message_get_exchanges
client.on_message_instruments_on_search = on_message_instruments_on_search
client.on_message_last_quote = on_message_last_quote
client.on_message_last_quote_array = on_message_last_quote_array
client.on_message_snapshot_data = on_message_snapshot_data
client.on_message_instrument_types = on_message_instrument_types
client.on_message_product = on_message_products
client.on_message_expiry_dates = on_message_expiry_dates
client.on_message_option_types = on_message_option_types
client.on_message_strike_prices = on_message_strike_prices

client.connect()
