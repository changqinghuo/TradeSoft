from quote import *
from wx.lib.pubsub import Publisher as pub

class DataManager(object):
    """Singleton datamanager"""
    def __init__(self):
        self.quotedata = None        
        pass
    def GetQuoteData(self, quote, period=300, num_day=5): 
        try:       
            self.quotedata = GoogleIntradayQuote(quote,period, num_day)
            pub.sendMessage("ANALYSISDATA", self.quotedata.df)
            return self.quotedata
        except:
            pass
        
        
    def GetQuoteRealtime(self, quote):
        pass
    
    

