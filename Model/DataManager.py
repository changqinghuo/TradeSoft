# -*- coding: utf-8 -*- 

from quote import *
from wx.lib.pubsub import Publisher as pub
import datetime
import threading
import time
import codecs
import sys
from StockData import StockData

class QuoteDataThread(threading.Thread):
    def __init__(self, symbol, period=300, num_day=5):
        threading.Thread.__init__(self)
        self.symbol = symbol
        self.period = period
        self.num_day = num_day
        self.dt = datetime.datetime(2000, 1, 1)
        self.quotedata = None
        self.lastupdate_time = datetime.datetime(2000, 1, 1)
        self._message_topic = "ANALYSISDATA"
        if self.period == 60:
            self._message_topic = "REALTIMEDATA"
        self.done = False
        
    def run(self):

        old = datetime.datetime.now() + datetime.timedelta(minutes = -1)
        old = datetime.datetime(old.year, old.month, old.day, old.hour, old.minute)
        while not self.done:
            try:                
                now = datetime.datetime.now()                
               # print now, "  ", old
                
                if self._IsMarketOpen(now):#now > old: 
                    if now.second > 10:
                        now =  datetime.datetime(now.year, now.month, now.day, now.hour, now.minute) 
                        if now > old:                 
                            q = GoogleIntradayQuote(self.symbol,self.period, self.num_day)
                            if q.datetime[-1] == now:
                                self.lastupdate_time = q.datetime[-1]
                                old = now
                                self.quotedata = q
                                pub.sendMessage(self._message_topic, self.quotedata.df) 
                    time.sleep(1)
                                #print q.df.ix[-1]
                                #print q.datetime[-1], ",", q.open[-1], ", ", q.high[-1], ", ", q.close[-1], ", ", q.low[-1], ", ", q.volume[-1]
 
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
        if dt.time()> datetime.time(15,0,0) or dt.time < datetime.time(9, 15, 0):
            return False
        return True


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
    def GetLastClose(self, sym):
        if sym.startswith('6') or sym == '000001':
            sym = "sh"+sym
        else:
            sym = 'sz'+sym        
        q = StockData(sym)
        return q.lastClose
        
                      
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
        self.symbol = sym
        self.thread_list = []
        realtime_thread = QuoteDataThread(self.symbol, 60, 1)
        realtime_thread.start()
        self.thread_list.append(realtime_thread)
        analysis_thread = QuoteDataThread(self.symbol, 300, 5)
        analysis_thread.start();
        self.thread_list.append(analysis_thread)     
        
        
        
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
#                                                   self.symbol_quote_dict.get(t.symbol).datetime[-1] < t.lastupdate_time:
#                        self.symbol_quote_dict[t.symbol] = t.quotedata  
#                    
#                        #if t.lastupdate_time > self.symbol_quote_dict.setdefault(t.symbol, None).lastupdate_time:
#                        pub.sendMessage(t.symbol+"ANALYSISDATA", t.quotedata.df)
#                        print t.lastupdate_time, "  Updated"
#                    print t.lastupdate_time
                       
        
    def run(self):
        self.QuoteDataThreads()
                
        
        
        

