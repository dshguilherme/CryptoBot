from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date
from datetime import datetime
import os


page = requests.get("https://coinmarketcap.com/")
soup = BeautifulSoup(page.content, 'html.parser')

today = date.today()
d1 = today.strftime("%d/%m/%Y")
print("Today's Date:", d1)

now = datetime.now()
timestr = now.strftime("%H:%M:%S")
print("Current Time:", timestr)

btc = soup.find(href="/currencies/bitcoin/markets/")
print("BTC Price:", btc.text)
price_btc = btc.text[1:len(btc.text)]
comma = price_btc.find(",")
price_btc = price_btc[0:comma] +price_btc[comma+1:len(price_btc)]
price_btc = int(price_btc[0:-3] +price_btc[-2:len(price_btc)])/100

eth = soup.find(href="/currencies/ethereum/markets/")
print("Ethereum Price:", eth.text)
price_eth = eth.text[1:len(eth.text)]
price_eth = int(price_eth[0:-3] +price_eth[-2:len(price_eth)])/100

xrp = soup.find(href="/currencies/xrp/markets/")
print("Ripple Price:", xrp.text)
price_xrp = xrp.text[1:len(xrp.text)]
# Since XRP is below 1 dollar, we take everything after the point
point = price_xrp.find(".")
price_xrp = price_xrp[point+1:len(price_xrp)]
price_xrp = int(price_xrp)/10**(len(price_xrp))

d = {'Date': [d1], 'Time': [timestr], 'BTC': [price_btc], 'ETH': [price_eth], 'XRP': [price_xrp]}
df = pd.DataFrame(data=d)
print(df)


if not os.path.isfile('prices.csv'):
    df.to_csv('prices.csv', header = 'column_names')
else:
    df.to_csv('prices.csv', mode='a', header=False) 
