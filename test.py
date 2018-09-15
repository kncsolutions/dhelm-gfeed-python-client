from DhelmGfeedClient.gfeedclient import  GfeedClient

client = GfeedClient("ws://nimblestream.lisuns.com:4526","f31b6d7d-0138-428d-93ef-28acbd9632d2")

def on_authenticated(ws):
    ws.get_exchanges()
    ws.get_instruments_on_search("NSE","SBIN")


client.on_authenticated = on_authenticated
client.connect()
#client.is_connected()
#print(client.ws_url);
#print(client.api_key);