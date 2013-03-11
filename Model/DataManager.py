# -*- coding: utf-8 -*- 

from quote import *
from wx.lib.pubsub import Publisher as pub
import datetime
import threading
import time
import codecs
import sys
from quote_realtime import QuoteRealtimeSina
import pandas as pd
import numpy as np

class QuoteDataThread(threading.Thread):
    def __init__(self, symbol, period=300, num_day=5):
        threading.Thread.__init__(self)
        self.symbol = symbol
        self.period = period
        self.num_day = num_day
        self.dt = datetime.datetime(2000, 1, 1)
        self.quotedata = None      
        
        self.realtimedata = pd.DataFrame()
        self.analysisdata = None
        self.lastupdate = datetime.datetime(2000, 1, 1)
        self.lastupdate_analysis = datetime.datetime(2000, 1, 1)
        self._message_topic = "ANALYSISDATA"
       
        if self.period == 60:
            self._message_topic = "REALTIMEDATA"
            realtime_index = self._GetRealtimeIndex()
            rows = len(realtime_index)
            matrix = np.zeros((rows, 5), dtype=np.float)
            self.realtimedata = pd.DataFrame(matrix, index=realtime_index, columns=['open', 'high', 'low', 'close', 'volume'])
        elif self.period == 1800:
            self._message_topic = "MIN30DATA" 
        elif self.period == 3600*4:
            self._message_topic = "DAYDATA"
        self.done = False
        
    def run(self):

        old = datetime.datetime.now() + datetime.timedelta(minutes = -1)
        old = datetime.datetime(old.year, old.month, old.day, old.hour, old.minute)
        while not self.done:
            try:                
                now = datetime.datetime.now()                
               # print now, "  ", old
                
                if self._IsMarketOpen(now):#now > old: 
                    self._RealtimeMode() 
                    time.sleep(10)                   
 
                else:
                    q = GoogleIntradayQuote(self.symbol,self.period, self.num_day)
                    self.quotedata = q
                    pub.sendMessage(self._message_topic, self.quotedata.df) 
                    self.done = True    
                        
                         
     
                
            except:
                print str(sys.exc_info())
                self.done = False
    def _IsMarketOpen(self, dt):
        if dt.weekday() == 5 or dt.weekday() == 6:
            return False
        if dt.time()> datetime.time(15,0,0) or dt.time() < datetime.time(9, 15, 0):        
            return False
        return True
    def _RealtimeMode(self):
        now = datetime.datetime.now()          
        now =  datetime.datetime(now.year, now.month, now.day, now.hour, now.minute) 
        if now > self.lastupdate:                 
            q = GoogleIntradayQuote(self.symbol,self.period, self.num_day)
            if self.lastupdate == q.dtstamp[-1]:
                return
            if True:#q.dtstamp[-1] == now:
                self.lastupdate = q.dtstamp[-1]
                if self.period == 60:
                    self.realtimedata = q.df
                    pub.sendMessage(self._message_topic, self.realtimedata) 
                else:                    
                    self.quotedata = q
                    pub.sendMessage(self._message_topic, self.quotedata.df) 
            
    def _GetRealtimeIndex(self):
        today = datetime.date.today()
        start = datetime.datetime(today.year, today.month, today.day , 9, 31,0)
        end = datetime.datetime(today.year, today.month, today.day , 11, 30,0)
        index = pd.date_range(start, end, freq='MIN')
        start = datetime.datetime(today.year, today.month, today.day , 13, 01,0)
        end = datetime.datetime(today.year, today.month, today.day , 15, 01,0)
        index2 = pd.date_range(start, end, freq='MIN')
        index0 =  pd.date_range(datetime.datetime(today.year, today.month, today.day , 9,26,0), periods=1)
        index =index0+index+index2
        return index
 


class DataManager(threading.Thread):
    """Singleton datamanager"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.quotedata = None
        self.symbol_quote_dict = {"000001":None} 
        self.symbol_dict = {}
        self._GetStockList()
        self.symbol = "000001"
        self.thread_list = []
        self.realtimequote_dict = {}
        self.QuoteDataThreads()
        self.InitializeRealtimeQuote()
        
    def GetLastClose(self, sym):
        return self.realtimequote_dict[sym].last_close
    def InitializeRealtimeQuote(self):
        def convertsym(sym):
            if sym.startswith('6') or sym == '000001':
                sym = "sh"+sym
            else:
                sym = 'sz'+sym
            return sym
        stock = [key for key in self.symbol_dict]
        
        try:
            i = 0
            step = 500
            while i < len(stock):
                if i+step < len(stock):                
                    url = "http://hq.sinajs.cn/list=" + ','.join(convertsym(stock)for stock in stock[i:i+step])
                    i = i +step
                else:
                    url = url = "http://hq.sinajs.cn/list=" + ','.join(convertsym(stock)for stock in stock[i:])
                    i= len(stock)
                print url
                lines = urllib2.urlopen(url, timeout=5).readlines()
                for line in lines:
                    rtquote = QuoteRealtimeSina(line)
                    self.realtimequote_dict[rtquote.stock_id[2:]] = rtquote
            for key in self.realtimequote_dict:
                print key, ":", self.realtimequote_dict[key].stock_name, self.realtimequote_dict[key].last_close
        except:
            print str(sys.exc_info())

                      
    def _GetStockList(self):
        f = codecs.open("../model/chinastock_utf.txt", 'r', 'utf-8')
        for line in f:
            sym, name = line.split(',')
            self.symbol_dict[sym] = name
    def GetQuoteData(self, quote, period=300, num_day=5): 
        try:       
            self.quotedata = GoogleIntradayQuote(quote,period, num_day)
            pub.sendMessage("ANALYSISDATA", self.quotedata.df)
            return self.quotedata
        except:
            pass       
        
    def GetQuoteRealtime(self, quote):
        pass
    
    def UpdateSymbol(self, sym):
        for t in self.thread_list:
            t.done = True
        self.symbol = sym
        self.thread_list = []
        realtime_thread = QuoteDataThread(self.symbol, 60, 3)
        realtime_thread.start()
        self.thread_list.append(realtime_thread)
        analysis_thread = QuoteDataThread(self.symbol, 300, 5)
        analysis_thread.start();
        self.thread_list.append(analysis_thread)  
        
        min30_thread = QuoteDataThread(self.symbol, 1800, 40)
        min30_thread.start()        
        self.thread_list.append(min30_thread)  
        
#        day_thread =  QuoteDataThread(self.symbol, 3600*4, 20)
#        day_thread.start()        
#        self.thread_list.append(day_thread)    
        
        
        
    def QuoteDataThreads(self):
        
       
        done = True
       # while True:

        realtime_thread = QuoteDataThread(self.symbol, 60, 1)
        realtime_thread.start()
        self.thread_list.append(realtime_thread)
        analysis_thread = QuoteDataThread(self.symbol, 300, 10)
        analysis_thread.start();
        self.thread_list.append(analysis_thread)
#        for d in self.symbol_quote_dict.keys(): 
#            t = QuoteDataThread(d, 60, 1)
#            t.start()            
#            thread_list.append(t)
#            done = True
#            for t in thread_list: 
#                time.sleep(1)               
#                if t.is_alive():
#                    done = False
#                else:
#                    
#                    if self.symbol_quote_dict.setdefault(t.symbol) is None or\
#                                                   self.symbol_quote_dict.get(t.symbol).dtstamp[-1] < t.lastupdate_time:
#                        self.symbol_quote_dict[t.symbol] = t.quotedata  
#                    
#                        #if t.lastupdate_time > self.symbol_quote_dict.setdefault(t.symbol, None).lastupdate_time:
#                        pub.sendMessage(t.symbol+"ANALYSISDATA", t.quotedata.df)
#                        print t.lastupdate_time, "  Updated"
#                    print t.lastupdate_time
                       
        
    def run(self):
        self.QuoteDataThreads()


if __name__ == '__main__':
    today = datetime.date.today()
    start = datetime.datetime(today.year, today.month, today.day , 9, 31,0)
    end = datetime.datetime(today.year, today.month, today.day , 11, 30,0)
    index = pd.date_range(start, end, freq='MIN')
    start = datetime.datetime(today.year, today.month, today.day , 13, 01,0)
    end = datetime.datetime(today.year, today.month, today.day , 15, 01,0)
    index2 = pd.date_range(start, end, freq='MIN')
    index0 =  pd.date_range(datetime.datetime(today.year, today.month, today.day , 9,26,0), periods=1)
    index =index0+index+index2
    
    print len(index)
    a = QuoteDataThread('002094', 60, 1)
    a.start()
        
        
        

