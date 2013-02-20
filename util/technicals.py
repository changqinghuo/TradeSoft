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
def _bi(df):
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
           
    knum_up = 0
    knum_down = 0

    result = []
    result.append(0)
    i = 1
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
            elif high <= highlast and low >= lowlast:
                lowlast = low
            else:
                break
        if knum_up >= 5 and direction == DIRECTION_DOWN:
            direction = DIRECTION_UP
            result.append(i)
        knum_up = 0
        
        #down trend
        while i < len(df):         
            high = df.ix[i]["high"]
            low = df.ix[i]["low"] 
            i = i +1 
            if low < lowlast:                
                knum_down = knum_down + 1
                highlast = high
                lowlast = low
            elif high <= highlast and low >= lowlast:
                highlast = high
            else:
                break
        if knum_down >= 5:
            direction = DIRECTION_DOWN
            result.append(i)
        knum_down = 0 
        
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
    print _bi(df)
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
