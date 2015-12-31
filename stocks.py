# Gets current stock price for all stocks on the TSX/SP composite index.
# Pulls the data from ca.finance.yahoo.com.
# Author: Brendan Jennings

import urllib
import re
import MySQLdb
from getpass import getpass

# get username and password
username = raw_input("User name: ")
password = getpass()

# Open database connection
db = MySQLdb.connect("localhost", username, password, "stock_info")

# Prepare symbol and price cursor objects
symCursor = db.cursor()
priCursor = db.cursor()

# get number of stocks in database to scrape
symCursor.execute("select symbol from stock")
numStocks = symCursor.rowcount

i = 0
while i <= numStocks:
    symbol = str(symCursor.fetchone())
    symbol = symbol[2:-3]
    htmlfile = urllib.urlopen("https://ca.finance.yahoo.com/q?s=" 
        + symbol + "&ql=0")
    htmltext = htmlfile.read()
    symbol = symbol.lower()
    regex ='<span id="yfs_l84_' + symbol + '">(.+?)</span>'
    pattern = re.compile(regex)
    price = re.findall(pattern, htmltext)
    price = str(price)
    price = price[2:-2]
    query = "update stock set price='" + price + "' where symbol like '" + symbol + "';"
    priCursor.execute(query)
    db.commit()
    print ("current price of " + symbol + " is: " + price)
    i += 1

symCursor.close()
priCursor.close()
