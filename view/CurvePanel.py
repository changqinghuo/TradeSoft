import wx
from util.draw import *
class CurvePanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: CandlePanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.__set_properties()
        self.__do_layout() 
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)  
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.EraseBack)
        self.data = None 
        self.last_close = 0


    
    def EraseBack(self, evt):
        pass
       
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        if self.data is None:
            return        
        dc = wx.PaintDC(self.realtime_window.main_panel)
        #dc.DrawBitmap(self.Buffer, 0, 0) 
        dc.Clear()     
        draw_realtime(dc, self.data, self.last_close)
           
        
        
    def __set_properties(self):
        # begin wxGlade: CandlePanel.__set_properties
        self.SetSize((588, 422))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CandlePanel.__do_layout
        pass
        # end wxGlade