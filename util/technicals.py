import wx
import pandas as pd
from model.quote import Quote
from util.draw import draw_candle

DIRECTION_UP = 0
DIRECTION_DOWN = 1
K_DING = -1
K_DI = 1

def macd(df):
    pass


def czsc(df):
    pass

def _process_contain(df):  
    
    pass
def _getfirstdirection(df):
    highlast = df.ix[0]["high"]
    lowlast = df.ix[0]["low"]
    for i in range(1, len(df.index)):        
        high = df.ix[i]["high"]
        low = df.ix[i]["low"]
        if high > highlast and low > lowlast:
            direction = DIRECTION_UP
            break
        elif low < lowlast and high < highlast:
            direction = DIRECTION_DOWN
            break
    return direction


def _processdata_test(df):
    result = pd.DataFrame(index= [i for i in range(len(df.index))], columns=["high", "low"])
#    result.set_value(df.index[0], 'high', df.ix[0]['high'])
#    result.set_value(df.index[0], 'low', df.ix[0]['low'])
    direction = _getfirstdirection(df)
    #result.set_value(0, 'high', df.ix[0]['high'])
    #result.set_value(0, 'low', df.ix[0]['low'])
    i = 0
    while i < len(df)-1:
        high = df.ix[i]["high"]
        low = df.ix[i]["low"]
        highnext = df.ix[i+1]["high"]
        lownext = df.ix[i+1]["low"]    
        
        tmp = result.dropna()       
        if len(tmp.index) > 0:
            highlast = tmp.ix[tmp.index[-1]]['high']
            lowlast = tmp.ix[tmp.index[-1]]['low']
            if high > highlast and low > lowlast:
                direction = DIRECTION_UP            
            elif low < lowlast and high < highlast:
                direction = DIRECTION_DOWN            
        else:
            direction = _getfirstdirection(df)    
 
        iscontain = False
        isave = i
        while (high >= highnext and low <= lownext) or (highnext >= high and lownext <= low):
            iscontain = True           
            if direction == DIRECTION_UP:
                if highnext > high:
                    isave = i
                high = max(high, highnext)
                low = max(low, lownext)
            
            elif direction == DIRECTION_DOWN :
                if lownext < low:
                    isave = i
                high = min(high, highnext)
                low = min(low, lownext)
            i = i + 1 
            if i < len(df)-1:
                highnext = df.ix[i]["high"]
                lownext = df.ix[i]["low"]
            else:
                break       

#        result.set_value(df.index[isave], 'high', high)
#        result.set_value(df.index[isave], 'low', low)
        result.set_value(isave, 'high', high)
        result.set_value(isave, 'low', low)
        if iscontain:
            pass
#            result.set_value(df.index[i], 'high', highnext)
#            result.set_value(df.index[i], 'low', lownext)
            #result.set_value(i, 'high', highnext)
            #result.set_value(i, 'low', lownext)
        else:
            i = i + 1
    return result.dropna()
        
def _processdata(df):
    result = pd.DataFrame(index= df.index, columns=["high", "low"])   
    
    i = 0
    while i < len(df):
        high = df.ix[i]["high"]
        low = df.ix[i]["low"]
        if i < len(df)-1:
            highnext = df.ix[i+1]["high"]
            lownext = df.ix[i+1]["low"] 
        else:
            result.set_value(df.index[i], 'high', high)
            result.set_value(df.index[i], 'low', low)  
            break 
        
        tmp = result.dropna()       
        if len(tmp.index) > 0:
            highlast = tmp.ix[tmp.index[-1]]['high']
            lowlast = tmp.ix[tmp.index[-1]]['low']
            if high > highlast and low > lowlast:
                direction = DIRECTION_UP            
            elif low < lowlast and high < highlast:
                direction = DIRECTION_DOWN            
        else:
            direction = _getfirstdirection(df)    
 
        iscontain = False
        isave = i
        while (high >= highnext and low <= lownext) or (highnext >= high and lownext <= low):
            iscontain = True           
            if direction == DIRECTION_UP:
                if highnext > high:
                    isave = i
                high = max(high, highnext)
                low = max(low, lownext)
            
            elif direction == DIRECTION_DOWN :
                if lownext < low:
                    isave = i
                high = min(high, highnext)
                low = min(low, lownext)
            i = i + 1 
            if i < len(df):
                highnext = df.ix[i]["high"]
                lownext = df.ix[i]["low"]
            else:
                break       

        if len(tmp) > 0:
            highlast = tmp.ix[tmp.index[-1]]['high']
            lowlast = tmp.ix[tmp.index[-1]]['low']
            if (high >= highlast and low <= lowlast) or (highlast >= high and lowlast <= low):
                if direction == DIRECTION_UP:
                    if highlast > high:
                        isave = tmp.index[-1]
                    high = max(high, highnext)
                    low = max(low, lownext)
                
                elif direction == DIRECTION_DOWN :
                    if lowlast < low:
                        isave = tmp.index[-1]
                    high = min(high, highnext)
                    low = min(low, lownext)              
              
                
        result.set_value(df.index[isave], 'high', high)
        result.set_value(df.index[isave], 'low', low)

        if iscontain:
            pass
        else:
            i = i + 1

    return result.dropna()        
        
def _fx(df):
    result = []
    

    i = 1
    knum = 0
    while i < len(df)-1:
        highlast = df.ix[i-1]["high"]
        lowlast = df.ix[i-1]["low"]
        high = df.ix[i]["high"]
        low = df.ix[i]["low"]
        highnext = df.ix[i+1]["high"]
        lownext = df.ix[i+1]["low"]     
        knum = knum + 1
       
        if high > highlast and high > highnext and low > lowlast and low > lownext:
            result.append((K_DING, i, knum+1))  
            knum = 0    
        elif low < lowlast and low < lownext and high < highnext and high < highlast:
            result.append((K_DI, i, knum+1))  
            knum = 0 
        i = i + 1 
    
    fxreulst = [(result[0][0], result[0][1])]  
    fx_tmp = result[0]
    i = 1
#    while i < len(result):
#        fx = result[i]
#        if fx_tmp[0] == K_DI:
#            if fx[0] == K_DI:
#                i = i + 1
#                continue
#            if fx[1] - fx_tmp[1] <= 5:
#                i = i + 1
#                continue
           
            
            
        
    return result                    
                          
                          
        
        
        
        
def _bi(df):
    highlast = df.ix[0]["high"]
    lowlast = df.ix[0]["low"]
    bi_start = 0
    bi_end = 0
    for i in range(1, len(df.index)):
        high = df.ix[i]["high"]
        low = df.ix[i]["low"]
        if high > highlast and low > lowlast:
            direction = DIRECTION_UP
            break
        elif low < lowlast and high < highlast:
            direction = DIRECTION_DOWN
            break
           
    knum_up = 0
    knum_down = 0

    result = []
    result.append(0)
    i = 1
    direction = DIRECTION_DOWN
    while i < len(df):
        high = df.ix[i]["high"]
        low = df.ix[i]["low"]
        i = i+1       
       
       #up trend
        while i < len(df):      
            
            high = df.ix[i]["high"]
            low = df.ix[i]["low"]        
            i = i + 1
            if high > highlast:
                knum_up = knum_up +1
                highlast = high
                lowlast = low
#            elif high <= highlast and low >= lowlast:
#                lowlast = low
            else:
                highlast = high
                lowlast = low
                break
        
        
        
        #down trend
        while i < len(df):         
            high = df.ix[i]["high"]
            low = df.ix[i]["low"] 
            i = i +1 
            if low < lowlast:                
                knum_down = knum_down + 1
                highlast = high
                lowlast = low
#            elif high <= highlast and low >= lowlast:
#                highlast = high
            else:
                highlast = high
                lowlast = low
                break
            
        if direction == DIRECTION_DOWN:
            if knum_up < 5:
                knum_down = knum_down + knum_up
                knum_up = 0
            else:
                direction = DIRECTION_UP
                result.append(i-knum_up-2)
                

        if direction ==  DIRECTION_UP:
            if knum_down < 5:
                knum_up = knum_up + knum_down
                knum_down = 0
            else:
                direction = DIRECTION_DOWN
                result.append(i-knum_down-2)        
            
#        if direction ==  DIRECTION_UP and knum_down < 5:
#            knum_up = knum_up + knum_down              
#            
#        
#        if knum_up >= 5 and direction == DIRECTION_DOWN:
#            direction = DIRECTION_UP
#            result.append(i-knum_up)
#            knum_up = 0
#        
#            
#        if knum_down >= 5 and direction == DIRECTION_UP:
#            direction = DIRECTION_DOWN
#            result.append(i-knum_down)
#            knum_down = 0 
        
    return result
         
            
        
#    for i in range(1, len(df.index)):
#        high = df.ix[i]["high"]
#        low = df.ix[i]["low"]
#        #contain
#        if high <= highlast and low >= lowlast:
#            if direction == DIRECTION_UP:
#                lowlast = low
#            else:
#                highlast = high            
#        elif high < highlast and low < lowlast and direction == DIRECTION_DOWN:
#            highlast = high
#            lowlast = low
#            knum_olddir = knum_olddir + 1
#        elif high > highlast and low > lowlast and direction == DIRECTION_UP: 
#            highlast = high
#            lowlast = low
#            knum_olddir = knum_olddir + 1
        
        
        
            
            
        
        
        
    

def _duan(df):
    pass
def _zhongshu(df):
    pass

def _firstbuy(df):
    pass
def _firstsell(df):
    pass
def _secondbuy(df):
    pass
def _secondsell(df):
    pass
def _thirdbuy(df):
    pass
def _thirdsell(df):
    pass


def test():
    "test case for czsc technical"
    df = pd.DataFrame.from_csv('600016test.csv')
#    testdf = _processdata(df)
#    print testdf
#    df = df.reindex(testdf.index)
#    df['high'] = testdf['high']
#    df['low'] = testdf['low']
    

    print _fx(df)
    
    class TestPanel(wx.Panel): 
        def __init__(self, parent):
            wx.Panel.__init__(self, parent)
            self.SetBackgroundColour('WHITE')    
            self.Bind(wx.EVT_PAINT, self.OnPaint)
            
    
        def OnPaint(self, event):
            dc = wx.PaintDC(self)           
            draw_candle(dc, df)
            
    class TestWindow(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(800, 600))
    
            panel = wx.Panel(self, -1)
            panel.SetBackgroundColour('WHITE')
    
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            linechart = TestPanel(panel)
            hbox.Add(linechart, 1, wx.EXPAND | wx.ALL, 15)
            panel.SetSizer(hbox)
    
            self.Centre()
            self.Show(True)


    app = wx.App()
    TestWindow(None, -1, 'Test')
    app.MainLoop()
    
    
    
    #assert 1 == 1
    
    #return "czsc test cases pass!"


if __name__ == '__main__':
    test()
