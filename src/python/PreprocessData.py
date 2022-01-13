from numpy import genfromtxt
import mysql.connector
from datetime import datetime
from datetime import timedelta
#from DataLoader import DataLoader
class PreprocessData():
    def __init__(this):
        this.mydb = mysql.connector.connect(host = "127.0.0.1", user = "root", passwd = "root",database = "crypto")
        this.symbol_list= ['ETH','EOS','XRP','BCH','LTC','TRX','ETC','BNB','OKB']
    def generate(this):
        for symbol in this.symbol_list:
            sql = "SELECT totimes,open FROM price where symbol='"+symbol+"' order by totime asc"
            mycursor = this.mydb.cursor(prepared=True)
            mycursor.execute(sql)
            x = mycursor.fetchall()
            mycursor.close()
            y = []
            for i in x:
                #print(type(i[0]))
                u=datetime.fromtimestamp(i[0])
                if datetime.fromtimestamp(i[0])==(datetime(u.year,u.month,u.day,u.hour,0,0,0)):
                    #print("yes",u)
                    y.append((u,i[1]))
            f = open("training_data_"+symbol+".csv","w+")
            beta=1
            prevvalue=None
            for i in range(0,len(y)-30):
                open1 = y[i][1]
                str1 = str(open1)
                for j in range(1,30):
                    str1 +=","
                    v=y[i+j][1]
                    if prevvalue is None:
                        ov=v
                    else:
                        ov=v*beta+prevvalue
                    str1+= str(ov)
                    prevvalue=ov
                str1 += ","
                f.write(str1)
                f.write(str(y[i+j+1][1]))
                f.write("\n")
            f.close()