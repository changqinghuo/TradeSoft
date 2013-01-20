from quote import *
class DataManager(object):
    """Singleton datamanager"""
    def __init__(self):        
        pass
    def GetQuoteData(self, quote, period=300, num_day=5):        
        q = GoogleIntradayQuote(quote,period, num_day)
        return q
        
    def GetQuoteRealtime(self, quote):
        pass
    
    

