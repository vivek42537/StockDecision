import pandas as pd
import quandl as qd
import numpy as np
import matplotlib.pyplot as plt

qd.ApiConfig.api_key = "PUT IN API KEY FROM QUANDL" #removed mine
 
# STRATEGY: 
# Buy when Moving average of 1 month, goes above Moving average of 200 days. Sell when shot term MAV dips below lon term MAV
# AND
# Relative Strength Indes (RSI) - buy when RSI below 30 (oversold) sell when above 70 (overbought)

#get current TSLA data - tutorial from Geeks for Geeks for calculating MAV in python
data = qd.get_table('WIKI/PRICES', ticker = 'TSLA') #data is only from 2010-07-06 to 2018-03-27 , pandas DF
print(data.head())

closePrice = data[['adj_close']]
dailyReturn = closePrice.pct_change() #pct_change formula is (price at time t - opening price) / opening price
dailyReturn.fillna(0, inplace=True)
print("Daily Return: ")
print(dailyReturn)

#moving average
mavShort = closePrice.rolling(window = 30).mean() #Average across 30 days (1 month)
mavLong = closePrice.rolling(window = 200).mean() #Average across 30 days (1 month)

print("MAV: ")
print(mavShort)
data['MAVshort'] = mavShort
data['MAVlong'] = mavLong


#calculate rsi - 2 week window - RSI = 100 - (100/ (1 + RS))
delta = closePrice.diff() #diff between close price from yesterday to today
profit = (delta.where(delta > 0, 0)).rolling(window = 14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window = 14).mean()
rs = profit / loss
data['RSI'] = 100 - (100 / (1 + rs))

# closePrice.plot()
# mav.plot()
# plt.show()

def BuyorSell(row): #strategy described at top
    if row['MAVshort'] > row['MAVlong'] and row['RSI'] < 30:
        return 'Buy'
    elif row['MAVshort'] > row['MAVlong'] and row['RSI']  > 70:
        return 'Sell'
    else:
        return 'Hold'

data['Decision'] = data.apply(BuyorSell, axis = 1)
print(data[['ticker', 'date', 'adj_close', 'MAVshort', 'MAVlong', 'RSI', 'Decision']].tail(10))
print(data[['ticker', 'date', 'adj_close', 'MAVshort', 'MAVlong', 'RSI', 'Decision']].head(10))

data.to_csv('TSLA_historicData.csv', index=True)