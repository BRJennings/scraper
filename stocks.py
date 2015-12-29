# Gets current stock price for all stocks on the TSX/SP composite index.
# Pulls the data from ca.finance.yahoo.com.

import urllib
import re
import MySQLdb

# open symbol file and read it, split on delimiter (\n)
symbolfile = open("symbols.txt")
symbolslist = symbolfile.read()
symbolslist = symbolslist.split("\n")


i = 0
while i <= len(symbolslist):
    symbol = symbolslist[i]
    htmlfile = urllib.urlopen("https://ca.finance.yahoo.com/q?s=" 
        + symbol + "&ql=0")
    htmltext = htmlfile.read()
    symbol = symbol.lower()
    regex ='<span id="yfs_l84_' + symbol + '*">(.+?)</span>'
    pattern = re.compile(regex)
    price = re.findall(pattern, htmltext)
    print ("current price of " + symbol + " is: " + str(price))
    i += 1

symbolfile.close()
