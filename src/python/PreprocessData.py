from datetime import datetime

from numpy import genfromtxt

import mysql.connector


class PreprocessData:
	'''
	Here data is pre processed
	'''
	
	CRYPTO_SYMBOLS = ['ETH','EOS','XRP','BCH','LTC','TRX','ETC','BNB','OKB']
	
	def __init__(self):
		self._mydb = None
		self._mycursor = None

	@property
	def mydb(self):
		self._mydb = mysql.connector.connect(host = "127.0.0.1", user = "root", passwd = "root",database = "crypto")
	
	@property
	def symbol_list(self):
		return self.CRYPTO_SYMBOLS
	
	@property
	def mycursor(self):
		'''
		this will cursor of database
		'''
		if self._mycursor is None:
			self._mycursor = self.mydb.cursor(prepared=True)
		return self._mycursor

	def get_data_from_database(self,symbol):
		'''
		this will return data from database
		'''
		sql = "SELECT totimes,open FROM price where symbol='"+symbol+"' order by totime asc"
		self.mycursor.execute(sql)
		data = self.mycursor.fetchall()
		self.mycursor.close()

		return data

	def get_data_with_timestamp(self,data):
		'''
		this will series of data with timestamp
		'''
		time_stamp_data = list()
		for _d in data:
			#print(type(i[0]))
			u=datetime.fromtimestamp(_d[0])
			if datetime.fromtimestamp(_d[0])==(datetime(u.year,u.month,u.day,u.hour,0,0,0)):
				#print("yes",u)
				time_stamp_data.append((u,_d[1]))
		return time_stamp_data

	def yeild_data(self,data):
		'''
		here data will be manipulated and yeild it 
		'''
		beta=1
		prevvalue=None
		for i in range(0,len(data)-30):
			open1 = data[i][1]
			ts_data = str(open1)
			for j in range(1,30):
				ts_data = ts_data + ","
				v=data[i+j][1]
				if prevvalue is None:
					ov=v
				else:
					ov=v*beta+prevvalue
				ts_data = ts_data + str(ov)
				prevvalue=ov
			ts_data = ts_data + ","
			ts_data = ts_data +data[i+j+1][1]
			ts_data = ts_data + "\n"

			yield ts_data

	
	def generate(self):
		for symbol in self.symbol_list:
			data = self.get_data_from_database(symbol=symbol)
			
			ts_data = self.get_data_with_timestamp(data=data)
			
			f = open(f"training_data\training_data_{symbol}.csv","w+")
			for ts_data in self.yeild_data(ts_data):
				f.write(ts_data)
			f.close()

if __name__ == '__main__':
	ppd = PreprocessData()
	ppd.generate()