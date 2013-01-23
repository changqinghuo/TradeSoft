from quote import *
from wx.lib.pubsub import Publisher as pub
import datetime
import threading
import time

class QuoteDataThread(threading.Thread):
    def __init__(self, symbol, period=300, num_day=5):
        threading.Thread.__init__(self)
        self.symbol = symbol
        self.period = period
        self.num_day = num_day
        self.dt = datetime.datetime(2000, 1, 1)
        self.quotedata = None
        self.lastupdate_time = datetime.datetime(2000, 1, 1)
        
    def run(self):
        done = False
        while not done:
            try:
                q = GoogleIntradayQuote(self.symbol,self.period, self.num_day)
                if q.datetime[-1] > self.dt:
                    self.lastupdate_time = q.datetime[-1]
                    self.quotedata = q 
                
                done = True           
                
            except:
                done = False

class DataManager(object):
    """Singleton datamanager"""
    def __init__(self):
        self.quotedata = None
        self.symbol_quote_dict = {"002094":None, '000001':None} 
        
                  

    def GetQuoteData(self, quote, period=300, num_day=5): 
        try:       
            self.quotedata = GoogleIntradayQuote(quote,period, num_day)
            pub.sendMessage("ANALYSISDATA", self.quotedata.df)
            return self.quotedata
        except:
            pass       
        
    def GetQuoteRealtime(self, quote):
        pass
    
    def QuoteDataThreads(self):
        thread_list = []
        for d in self.symbol_quote_dict.keys(): 
            t = QuoteDataThread(d)
            t.start()            
            thread_list.append(t)
        done = True
        while True:
            done = True
            for t in thread_list: 
                time.sleep(5)               
                if t.is_alive():
                    done = False
                else:
                    self.symbol_quote_dict[t.symbol] = t
                    #if t.lastupdate_time > self.symbol_quote_dict.setdefault(t.symbol, None).lastupdate_time:
                    pub.sendMessage(t.symbol+"ANALYSISDATA", t.quotedata.df)
                       
        
            
        
        
        

