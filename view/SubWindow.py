import wx
from CandlePanel import *
from CurvePanel import *

class MyChildFrame(wx.MDIChildFrame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyChildFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.MDIChildFrame.__init__(self, *args, **kwds)
        
        self.main_panel = CandlePanel(self, -1)
        self.sym = ""
        self.data = None
        self.interval = "5Min"
        #self.main_panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def SetStockData(self, sym, df, interval):
        self.main_panel.data = df
        self.sym = sym
        self.interval = interval
        self.SetTitle(self.interval+":"+self.sym)
        self.main_panel.Refresh()
        
    def OnClose(self, evt):
        self.Show(False)

        
    def __set_properties(self):
        # begin wxGlade: MyChildFrame.__set_properties
        self.SetTitle("frame_1")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyChildFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.main_panel, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyChildFrame
    