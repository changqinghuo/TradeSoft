# -*- coding: utf-8 -*-
#!/usr/bin/python
import urllib2
import re
import datetime
import time
class StockRealtime:
    def __init__(self, data=""):
        self.stockId = ""
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
             
        if data != "":
            self.parseData(data)
    def parseData(self, data):
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
        

        
        

def sina_parse(data):
    rval = {}
    values = data.split(',')
    idname = values[0]
    index = idname.index('=')
    stockid = idname[index-8: index]
    stockname = idname[index+2:]
    rval["stockid"] = stockid
    rval["stockname"] = stockname
    rval["open"] = float(values[1])
    rval["lastclose"] = float(values[2])
    rval["currentprice"] = float(values[3])
    rval["highest"] = float(values[4])
    return rval
        
    
    
    
    



def main():
    data = """var hq_str_sz002094="青岛金王,7.97,7.90,7.96,8.05,7.90,7.96,7.97,4263677,34059034.42,17220,7.96,65001,7.95,25400,7.94,30100,7.93,8700,7.92,34254,7.97,82800,7.98,7400,7.99,42900,8.00,11090,8.01,2012-12-31,15:05:46,00";"""
    url = "http://hq.sinajs.cn/list=sz002094"
    realtimedata = []
    datafile = open("realdata.txt", 'a')
    count = 0
    with open("realdata.txt", 'a') as datafile:
        a = StockRealtime(data)
        endtime = datetime.datetime(2013, 1, 4, 15, 01)
        oldtime = datetime.datetime.now()
        while a.datetime < endtime:
            try:
                data = urllib2.urlopen(url,timeout=1).read().decode('gbk')
                print data
                a = StockRealtime(data)
                if oldtime != a.datetime:
                    datafile.write(data)
                    oldtime = a.datetime               
             
                time.sleep(0.1)
                
            except:
                pass
                    
            
            
    


    



if __name__ == '__main__':
    main()