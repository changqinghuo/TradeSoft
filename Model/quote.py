# Copyright (c) 2011, Mark Chenoweth
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted 
# provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following 
#   disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS 
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#Modify by TerryHUO: 2013-2
#==1 Modify for ChinaStock market

import urllib2,time,datetime
import pandas as pd
import sys
import numpy as np
import StringIO


class Quote(object):
  
  DATE_FMT = '%Y-%m-%d'
  TIME_FMT = '%H:%M:%S'
  
  #dataframe field
  COL_DATE = 'Date'
  COL_OPEN = 'Open'
  COL_CLOSE = 'Close'
  COL_HIGH = 'High'
  COL_LOW = 'Low'
  COL_VOLUME = 'Volume'
  COL_ADJCLOSE = 'Adj Close'
  def __init__(self):
    self.symbol = ''
    self.dtstamp ,self.open,self.high,self.low,self.close,self.volume = ([] for _ in range(6))
    self.df = None
  def append(self,dt,open,high,low,close,volume):
     
    self.dtstamp.append(dt)
    self.open.append(float(open))
    self.high.append(float(high))
    self.low.append(float(low))
    self.close.append(float(close))
    self.volume.append(int(volume))
      
  def to_csv(self):
      #return self.df.to_csv(path_or_buf, sep, na_rep, float_format, cols, header, index, index_label, mode, nanRep, encoding, quoting, line_terminator)
      output = StringIO.StringIO()
      self.df.to_csv(output, float_format='%.2f')
      return output.getvalue()
#    return ''.join(["{0},{1},{2:.2f},{3:.2f},{4:.2f},{5:.2f},{6}\n".format(self.symbol,
#              self.dtstamp[bar].strftime(self.DATE_FMT+' '+self.TIME_FMT),
#              self.open[bar],self.high[bar],self.low[bar],self.close[bar],self.volume[bar]) 
#              for bar in xrange(len(self.close))])
    
  def write_csv(self,filename):
      self.df.to_csv(filename, float_format='%.2f')
        
  def read_csv(self,filename):
#    self.symbol = ''
#    self.date,self.time,self.open,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
#    for line in open(filename,'r'):
#      symbol,dt,open_,high,low,close,volume = line.rstrip().split(',')
#      self.symbol = symbol
#      dt = datetime.datetime.strptime(dt,self.DATE_FMT+' '+self.TIME_FMT)
#      self.append(dt,open_,high,low,close,volume)
    self.symbol = filename
    self.df = pd.read_csv(filename, index_col=0)
    return True

  def __repr__(self):
    return self.to_csv()

class GoogleIntradayQuote(Quote):
    
    ''' Intraday quotes from Google. Specify interval seconds and number of days '''
    
    def __init__(self,symbol,interval_seconds=300,num_days=5):              
        super(GoogleIntradayQuote,self).__init__()
        #google does not support for interval > 30Min
        if interval_seconds > 1800:
            return None
        self.symbol = symbol.upper()
        self.interval_seconds = interval_seconds
        dict = {}
        url_string = "http://www.google.com/finance/getprices?q={0}".format(self.symbol)
        url_string += "&i={0}&p={1}d&f=d,o,h,l,c,v".format(interval_seconds,num_days)
        csv = urllib2.urlopen(url_string, timeout=3).readlines()
        
        for bar in xrange(7,len(csv)):
            
            if csv[bar].count(',')!=5: continue
            offset,close,high,low,open_,volume = csv[bar].split(',')
            if offset[0]=='a':
                day = float(offset[1:])
                offset = 0
            else:
                offset = float(offset)
            open_,high,low,close = [float(x) for x in [open_,high,low,close]]
            dt = datetime.datetime.fromtimestamp(day+(interval_seconds*offset))
            self.append(dt, open_, high, low, close, volume)
      
        dict = {'open':self.open, 'high':self.high, 
            'low':self.low, 'close':self.close, 'volume':self.volume}
        df = pd.DataFrame(dict, index=pd.Index(self.dtstamp, name=Quote.COL_DATE))
        
        self.df = df
        if df is None:
            return
        self.df = self._AdjustData(df)       

   
    def _CreateIndex(self, df):
        d1 = df.index[0].date()
        days = [d1]
        for t in df.index:#self.dtstamp:#df.index:#
            if t.date() != d1:
                days.append(t)
                d1 = t.date()               

        ts = pd.date_range(start=d1, periods=0)
        for day in days:            
            morning = datetime.datetime(day.year, day.month, day.day, 9, 30, 0)
            morning_end = datetime.datetime(day.year, day.month, day.day, 11, 30, 0)
            rng_morning = pd.date_range(start=morning, end=morning_end, freq=str(self.interval_seconds)+'s')
            ts = ts.append(rng_morning[1:])
            afternoon = datetime.datetime(day.year, day.month, day.day, 13, 00, 0)
            afternoon_end = datetime.datetime(day.year, day.month, day.day, 15, 00, 0)
            rng_afternoon = pd.date_range(start=afternoon, end=afternoon_end, freq=str(self.interval_seconds)+'s')
            ts = ts.append(rng_afternoon[1:])
        lastupdate = df.index[-1]#self.dtstamp[-1]
        ts = [t for t in ts if t <= lastupdate ]
        print self.interval_seconds, "s:", ts[-1]
        return ts
            
        
            
    def _AdjustData(self, df):
        new_index = pd.Index(self._CreateIndex(df), name=Quote.COL_DATE)
        df = df.reindex(new_index)
                     
        timeselected = [t for t in df.index if t.time() < datetime.time(9, 31,0) or \
                        (t.time() > datetime.time(11, 30, 0) and t.time()<datetime.time(12,0,0))\
                        or t.time() <= datetime.time(13,00,00) and t.time() >datetime.time(12, 30,0)\
                         or t.time() > datetime.time(15, 00,0)]
  
        a = df.ix[timeselected]    
        for t in a.index: 
            if t.time()  < datetime.time(9, 31,0):
                timetomodify = datetime.datetime(t.year, t.month, t.day, 9,30,0) + datetime.timedelta(seconds=self.interval_seconds)
                df = df.set_value(timetomodify, 'open', df.get_value(t, 'open'))
                if np.isnan(df.get_value(timetomodify, 'close')):
                    df.set_value(timetomodify, 'close', df.get_value(t, 'close'))                   
                
            elif t.time() > datetime.time(11, 30, 0) and t.time()<datetime.time(12,0,0):            
                timetomodify = datetime.datetime(t.year, t.month, t.day, 11, 30, 0)           
                df = df.set_value(timetomodify, 'close', df.get_value(t,'close'))
                if np.isnan(df.get_value(timetomodify, 'open')):
                    df.set_value(timetomodify, 'open', df.get_value(t, 'open'))
            elif t.time() >  datetime.time(15, 00,0):
                timetomodify = datetime.datetime(t.year, t.month, t.day, 15, 0, 0)       
                df = df.set_value(timetomodify, 'close', df.get_value(t,'close'))
                if np.isnan(df.get_value(timetomodify, 'open')):
                    df.set_value(timetomodify, 'open', df.get_value(t, 'open'))
            elif t.time() <= datetime.time(13,00,00) and t.time() >datetime.time(12, 30,0):
                timetomodify = datetime.datetime(t.year, t.month, t.day, 13, 0, 0)+ datetime.timedelta(seconds=self.interval_seconds)
                df = df.set_value(timetomodify, 'open', df.get_value(t, 'open'))
                if np.isnan(df.get_value(timetomodify, 'close')):
                    df.set_value(timetomodify, 'close', df.get_value(t, 'close'))         
                
            if not np.isnan(df.get_value(timetomodify, 'volume')):                            
                df.set_value(timetomodify, 'volume', df.get_value(t, 'volume')+df.get_value(timetomodify, 'volume'))
            else:
                df.set_value(timetomodify, 'volume', df.get_value(t, 'volume'))
                
            if not np.isnan(df.get_value(timetomodify, 'high')):
                df.set_value(timetomodify, 'high', max(df.get_value(t, 'high'), df.get_value(timetomodify, 'high')))
            else:
                df.set_value(timetomodify, 'high', df.get_value(t, 'high'))
                
            if not np.isnan(df.get_value(timetomodify, 'low')):                
                df.set_value(timetomodify, 'low', min(df.get_value(t, 'low'), df.get_value(timetomodify, 'low')))
            else:
                df.set_value(timetomodify, 'low', df.get_value(t, 'low'))
        
        df['volume'].fillna(0, inplace=True)
        df.fillna(method='ffill', inplace=True)
        df.fillna(method = 'bfill', inplace=True)
        
        return df

            


    

   
if __name__ == '__main__':
   

    
    
#    day = datetime.date(2013, 2, 1)
#    ts = pd.date_range(start=day, periods=0)
#    morning = datetime.datetime(day.year, day.month, day.day, 9, 30, 0)
#    morning_end = datetime.datetime(day.year, day.month, day.day, 11, 30, 0)
#    rng_morning = pd.date_range(start=morning, end=morning_end, freq='60s')
#    ts = ts.append(rng_morning[1:])
#    
##    for t in ts:
##        print t
#    afternoon = datetime.datetime(day.year, day.month, day.day, 13, 00, 0)
#    afternoon_end = datetime.datetime(day.year, day.month, day.day, 15, 00, 0)
#    rng_afternoon = pd.date_range(start=afternoon, end=afternoon_end, freq='60s')
#    ts = ts.append(rng_afternoon[1:])
#    for t in ts:
#        print t
#    df = pd.DataFrame(index=ts, columns=['open', 'close'])
#    print df.ix[1]
#    dfmorning = pd.DataFrame(np.zeros((3, 2)),    index = ['a', 'b', 'c'], columns=['open', 'close'])
#    dfafternoon = pd.DataFrame(np.ones((3,2)), index = ['a', 'b', 'd'],columns=['open', 'close'])
#    print dfafternoon
#    print dfmorning.reindex(['a', 'b', 'd'])
#    print dfmorning
    
  
    while True:
        try:
            q = GoogleIntradayQuote('600016', 1800, 10) 
            print q.to_csv()
     
            #q.write_csv(q.symbol)
            q = Quote()
            q.read_csv('000019.SZ.csv')
            print q.df.head()
            time.sleep(1)
            print q.df.index[-1], ",", q.df['open'][-1], ",", q.df['close'][-1]#, ", " ,q.high[-1], ",", q.low[-1], ",", q.volume[-1]/100 
        except :
            print str(sys.exc_info())


