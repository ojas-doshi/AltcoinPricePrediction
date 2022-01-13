import requests
from datetime import datetime, timedelta

import mysql.connector

__all__ = ['DataLoader']

class DataLoader:
	'''
	Historical Data Loader 
	takes data from historical data provider for e.g cryptocompare
	'''
	CRYPTO_SYMBOLS = ['ETH','EOS','XRP','BCH','LTC','TRX','ETC','BNB','OKB']
	def __init__(self):
		# configuration of my sql database
		self.host = '127.0.0.1'
		self.user = 'root'
		self.password = 'root'
		self.database = 'crypto'

		self._mydb = None
		self._mycursor =None
		self._time = None


	@property
	def time(self):
		'''
		this will return time delta
		'''
		if self._time is None:
			self._time = datetime.now()
		else:
			self._time = self._time+timedelta(minutes=15)
		return self._time

	@property
	def mydb(self):
		'''
		connects to database
		'''
		if self._mydb is None:
			self._mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password,database=self.database)
		return self._mydb

	@property
	def mycursor(self):
		'''
		this will cursor of database
		'''
		if self._mycursor is None:
			self._mycursor = self.mydb.cursor(prepared=True)
		return self._mycursor

	@property
	def symbol_list(self):
		'''
		return list of symbols
		'''
		return self.CRYPTO_SYMBOLS

	def get_data_link(self,from_crypto,limit,time,to_crypto="BTC",aggregate=15):
		'''
		This will return data link in which  from crypto to crypto conversion link of data provider is created
		'''
		provider_link = f"https://min-api.cryptocompare.com/data/histominute?"
		from_crypto_link =provider_link + f"fsym={from_crypto}"
		to_crypto_link = from_crypto_link + f"&tsym={to_crypto}"
		aggregate_link =to_crypto_link + f"&aggregate={aggregate}"
		limit_link = aggregate_link + f"&limit={limit}"
		
		data_link = limit_link

		if time:
			if not isinstance(time,str):
				time = str(time)
			data_link = data_link + f"&toTs={time}"

		return data_link
	
	def get_response_data(self,link):
		'''
		this will return response data from data received from link 
		'''
		response= requests.get(link)
		raw_data = response.json()
		data = raw_data["Data"]

		return data

	def add_data(self,totimeseconds):
		'''
		this will fetch data and insert it into database
		'''
		for symbol in self.symbol_list:
			each_symbol_data_link = self.get_data_link(from_crypto=symbol,limit=100,time=totimeseconds)
			each_symbol_data = self.get_response_data(each_symbol_data_link)
			if each_symbol_data:
				self.insert_data_into_database(symbol,each_symbol_data)
				totimeseconds=each_symbol_data[0]['time']
	
	def insert_data_into_database(self,symbol,each_symbol_data):
		'''
		this will insert data into database
		'''
		print(f'Inserting Data of {symbol} into database {self.database}')
		for symbol_data in each_symbol_data:
			sql = """insert ignore into price (symbol,fromtimes,totimes,fromtime,totime,fromvolume,tovolume,open,high,low,close,processed) values(%s,%s,%s,from_unixtime(%s),from_unixtime(%s),%s,%s,%s,%s,%s,%s,%s)"""
			data = (symbol,symbol_data['time']-900,symbol_data['time'],symbol_data['time']-900,symbol_data['time'],symbol_data['volumefrom'],symbol_data['volumeto'],symbol_data['open'],symbol_data['high'],symbol_data['low'],symbol_data['close'],'0')
			self.mycursor.execute(sql,data)
		
		print(f'Data Inserted into database')

	def load_data(self):
		'''
		this will load data into database
		'''
		try:
			while(1):
				data_link = self.get_data_link(from_crypto='ETH',limit=1)
				data = self.get_response_data(data_link)
				time_ = data[1]['time']
				for k in range(100):
					self.add_data(totimeseconds=time_)
				
				print(self.time)
		except:
			pass

	def close(this):
		this.mydb.close()


if __name__ == '__main__':
	dl = DataLoader()
	dl.load_data()

	dl.close()