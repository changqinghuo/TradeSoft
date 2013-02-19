import wx
import pandas as pd
from model.quote import Quote
from util.draw import draw_candle
def macd(df):
    pass


def czsc(df):
    pass

def _process_contain(df):
    
    
    pass
def _bi(df):
    pass
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
