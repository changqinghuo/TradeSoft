# -*- coding: utf-8 -*-
#!/usr/bin/python
import pandas
import urllib2
import re
import datetime
import time

class StockData:
    def __init__(self, stockid):
        self.stockId = stockid
        self.stockName = ""
        self.open = 0
        self.lastClose = 0
        self.currentPrice = 0
        self.high = 0
        self.low = 0
        self.buy = 0
        self.sell = 0
        self.buyList = []
        self.sellList = []
        self.tradeVolume = 0
        self.tradeMoney = 0
        self.datetime = 0
        self.type = 'r'
        self.__storeData = pandas.Series()        
        self.url = "http://hq.sinajs.cn/list="+self.stockId            
        
    def parseData(self, data):
        try:            
            values = data.split(',')
            idname = values[0]
            index = idname.index('=')
            self.stockId = idname[index-8: index]
            self.stockName = idname[index+2:]
            self.open = float(values[1])
            self.lastClose = float(values[2])
            self.currentPrice = float(values[3])
            self.high = float(values[4])
            self.low = float(values[5])
            self.buy = float(values[6])
            self.sell = float(values[7])
            self.tradeVolume = int(values[8])
            self.tradeMoney = float(values[9])
            for i in range(10, 20, 2):
                self.buyList.append((float(values[i]), float(values[i+1])))
            for i in range(20, 29, 2):
                self.sellList.append((float(values[i]), float(values[i+1])))
            line = values[30] + " " + values[31]
            rep = re.compile(r'(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})')
            m = rep.match(line)
            self.datetime = datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),\
                                              int(m.group(4)), int(m.group(5)), int(m.group(6)))
            return True
        except:
            return False

    def getRealData(self):
        pass
    def get5MinData(self):
        listdata = []
        df = self.__storeData.resample('5Min', 'ohlc',  fill_method='pad')
        for val in df.values:
            a = StockData(self.stockId)
            a.open = val[0]
            a.high = val[1]
            a.close =val[2]
            a.low = val[3]
            listdata.append(a)
        return listdata
                
            
        pass
    def get30MinData(self):
        pass
    def getDayData(self):
        pass
    def getRealtimeData(self):
        pass
    def getDataFromSina(self):
        with open("model/realdata.txt", 'r') as datafile:
            val = {}
            for line in datafile:
                a = StockData(self.stockId)
                if a.parseData(line):
                    val[a.datetime] = a.currentPrice
        self.__storeData = pandas.Series(val)
       
            
#            with open("realdata.txt", 'a') as datafile:
#                endtime = datetime.date + datetime.timedelta(hours=15)
#                oldtime = datetime.datetime.now()
#                
#                while oldtime <= endtime:
#                    try:
#                        data = urllib2.urlopen(self.url,timeout=1).read().decode('gbk')
#                        a = StockData(self.stockId)
#                        a.parseData(data)
#                        if oldtime <= a.datetime:
#                            datafile.write(data)
#                            oldtime = a.datetime 
#                            self.__storeData[a.datetime] =  a           
#                     
#                        time.sleep(1)
#                        
#                    except:
#                        pass
            

class StockData5Min(StockData):
    def __init__(self, stockid):
        StockData.__init__(self, stockid)
        self.__storeData = {}
    
#a = StockData('sz002094')
#a.getDataFromSina()
#list = a.get5MinData()
#for a in list:
#    print a.open
        
        
