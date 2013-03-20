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
        self.main_panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        #self.main_panel.Bind(wx.EVT_CHAR, self.OnChar)
        
        #zoom in and zoom out:
        self._dataleft = -1
        self._dataright = -1
        
    def OnChar(self, evt):
        keycode = evt.GetKeyCode()
        if True:#keycode == wx.WXK_UP:
            self._dataleft = self._dataleft + 10
            self.main_panel.data = self.data[self._dataleft: self._dataright]
            self.main_panel.Refresh()

    def OnKeyDown(self, evt):
        #don't know why wx.wxk_up and wx.wxk_down cannot be captured
        keycode = evt.GetKeyCode()
     
        if keycode == wx.WXK_SPACE:#keycode == wx.WXK_UP:
            self._dataleft = self._dataleft + 10
            self.main_panel.data = self.data[self._dataleft: self._dataright]
            self.main_panel.Refresh()
        elif keycode == wx.WXK_ALT:
            if self._dataleft - 10 >=0:
                self._dataleft = self._dataleft - 10
            else:
                return
            self.main_panel.data = self.data[self._dataleft: self._dataright]
            self.main_panel.Refresh()
            
            
    def SetStockData(self, sym, df, interval):
        if df is None:
            return
        self.data = df
        self._dataleft = 0
        self._dataright = len(df)
        
#        if self._dataleft <0 and self._dataright <0:            
#            self._dataright = len(df)
#            self._dataleft = self._dataright - 240
#            if self._dataleft < 0:
#                self._dataleft = 0
        
        
        self.main_panel.data = df[self._dataleft:self._dataright]
               
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
    