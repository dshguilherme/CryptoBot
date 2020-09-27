import requests
import os
from datetime import date
from datetime import datetime

from bs4 import BeautifulSoup
import pandas as pd


page = requests.get("https://coinmarketcap.com/")
soup = BeautifulSoup(page.content, 'html.parser')

today = date.today()
d1 = today.strftime("%d/%m/%Y")
print("Today's Date:", d1)

now = datetime.now()
timestr = now.strftime("%H:%M:%S")
print("Current Time:", timestr)

bitcoin_data = soup.find(href="/currencies/bitcoin/markets/")
print("BTC Price:", bitcoin_data.text)
bitcoin_price = bitcoin_data.text[1:len(bitcoin_data.text)]
comma = bitcoin_price.find(",")
bitcoin_price = bitcoin_price[0:comma] + bitcoin_price[comma+1:len(bitcoin_price)]
bitcoin_price = bitcoin_price[0:-3] + bitcoin_price[-2:len(bitcoin_price)]
bitcoin_price = int(bitcoin_price)/100

ethereum_data = soup.find(href="/currencies/ethereum/markets/")
print("Ethereum Price:", ethereum_data.text)
ethereum_price = ethereum_data.text[1:len(ethereum_data.text)]
ethereum_price = ethereum_price[0:-3] + ethereum_price[-2:len(ethereum_price)]
ethereum_price = int(ethereum_price)/100

ripple_data = soup.find(href="/currencies/xrp/markets/")
print("Ripple Price:", ripple_data.text)
ripple_price = ripple_data.text[1:len(ripple_data.text)]
# Since XRP is below 1 dollar, we take everything after the point
point = ripple_price.find(".")
ripple_price = ripple_price[point+1:len(ripple_price)]
ripple_price = int(ripple_price)/10**(len(ripple_price))

d = {'Date': [d1], 'Time': [timestr], 'BTC': [bitcoin_price],
     'ETH': [ethereum_price], 'XRP': [ripple_price]}
df = pd.DataFrame(data=d)
print(df)

'''
if not os.path.isfile('prices.csv'):
    df.to_csv('prices.csv', header = 'column_names')
else:
    df.to_csv('prices.csv', mode='a', header=False)
'''