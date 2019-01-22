All notable changes to this project will be documented in this file.

V 1.0.3
-------
Following changes are made in the callbacks:<br/>
1.  `on_message_get_exchanges(list_exchanages)` has been changed to `on_message_get_exchanges(base_client,list_exchanages)`.
2. `on_message_instruments_on_search(list_instruments)` has been changed to def `on_message_instruments_on_search(base_client,list_instruments)`.
3. `on_message_instruments(list_instruments)` has been changed to `on_message_instruments(base_client,list_instruments)`.
4. `on_message_last_quote(last_quote)` has been changed to `on_message_last_quote(base_client,last_quote)`.
5. `on_message_last_quote_array(last_quote_array)`has been changed to def `on_message_last_quote_array(base_client,last_quote_array)`.
6. `on_message_snapshot_data(snapshot_data)` has been changed to def `on_message_snapshot_data(base_client,snapshot_data)`.
7. `on_message_instrument_types(instrument_types)` has been changed to `on_message_instrument_types(base_client,instrument_types)`.
8. `on_message_products(products)` has been changed to `on_message_products(base_client,products)`.
9. `on_message_expiry_dates(expiry_dates)` has been changed to `on_message_expiry_dates(base_client,expiry_dates)`.
10. `on_message_option_types(option_types)` has been changed to `on_message_option_types(base_client,option_types)`.
11. `on_message_strike_prices(strike_prices)` has been changed to `on_message_strike_prices(base_client,strike_prices)`.
12. `on_message_account_limitations(account_limitations)` has been changed to `on_message_account_limitations(base_client,account_limitations)`.
13. `on_message_market_message(market_message)` has been changed to `on_message_market_message(base_client,market_message)`.
14. `on_message_exchange_message(exchange_message)` has been changed to `on_message_exchange_message(base_client,exchange_message)`.
15. `on_message_realtime_data(realtime_data)` has been changed to `on_message_realtime_data(base_client,realtime_data)`.
16. `on_message_realtime_snapshot_datarealtime_snapshot_data)` has been changed to `on_message_realtime_snapshot_data(base_client,realtime_snapshot_data)`.
17. `on_message_historical_tick_data(historical_tick_data)` has been changed to `on_message_historical_tick_data(base_client,historical_tick_data)`.
18. `on_message_historical_ohlc_data(historical_ohlc_data)`has been changed to `on_message_historical_ohlc_data(base_client,historical_ohlc_data)`.
19. `on_reconnect(count)` has been changed to `on_reconnect(base_client,count)`  