# portugal_fuel_prices
Two python scrips to get fuel prices from DGEG - Direcção Geral de Energia e Geologia and calculate the the cheapest one based on your personal needs.

- read_and_store_shops.py 

Reads the json file of the DGEG - Direcção Geral de Energia e Geologia and stores in a SQL database.

- shop_rank.py

Asks for various input ( Fuel type, your location, maximum distance to the shop, average car consumption, money to spend. brand discount).

It then gets the shop's data from the SQL database used in the previous script, based on the distance and fuel type.

In the end it calculates which is the best 3 fuel shops based on how many liters you can get from the shop taking in account the fuel wasted driving there and the brand discounts.
