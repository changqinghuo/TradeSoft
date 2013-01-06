import wx
import random
from sina_parse_realtime import StockRealtime

class CandleData():
    def __init__(self):
        self.rec = (0,0,0,0)
        self.upperLine = (0,0,0,0)
        self.lowerLine =(0,0,0,0)

class SketchFrame(wx.Frame):
    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "Sketch Frame",size=(350,350))
        self.sketch = SketchWindow(self, -1)

class SketchWindow(wx.Window):

    def __init__ (self, parent,ID):

        wx.Window.__init__(self, parent, ID)
        self.Buffer = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

    def InitBuffer(self):
        size=self.GetClientSize()
        # if buffer exists and size hasn't changed do nothing
        if self.Buffer is not None and self.Buffer.GetWidth() == size.width and self.Buffer.GetHeight() == size.height:
            return False
        
        self.Buffer=wx.EmptyBitmap(size.width,size.height)
        dc=wx.MemoryDC()
        dc.SelectObject(self.Buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.__stockList = []
        for i in range(10):
            stock = StockRealtime("")
            stock.open = 300
            stock.close = 320
            stock.high = 390
            stock.low = 290
            self.__stockList.append(stock)
       
        
        self.DrawCandleLineList(dc, self.__stockList)
        dc.SelectObject(wx.NullBitmap)
        return True

#    def __getStockDataListRange(self, stockdataList):
#        return (30, 50)
    
    def DrawCandleLineList(self, dc, stockdataList):        
         size=self.GetClientSize()
         windowWidth = size.width
         windowHeight = size.height
         candleWith = windowWidth/len(stockdataList)
         stockRange = (300., 500.)
         recwidth = windowWidth/len(stockdataList)
         recs = []
         lines = []     
         for i in range(len(stockdataList)):
             stock = stockdataList[i]
             pricediff = stockRange[1] - stockRange(0)
             recheight = windowHeight*abs(stock.close - stock.open)/pricediff
             x = i*recwidth
             if stock.close > stock.open:
                 y = windowHeight*stock.close/pricediff                 
                 upperlineendY = y - (stock.high - stock.close) 
                 lowerlineendY = y + (stock.open - stock.low)
             else:
                 y = windowHeight*stock.open/pricediff
                 upperlineendY = y - (stock.high - stock.open) 
                 lowerlineendY = y + (stock.close - stock.low)
             rec = (x, y, recwidth, recheight)
             upperline = (x+candleWith/2, y, x+candleWith/2, upperlineendY)
             lowerline = (x+candleWith/2, y-recheight, x+candleWith/2, y-recheight + upperlineendY)
             recs.append(rec)
             lines.append(upperline)
             lines.append(lowerline)
            
         dc.DrawRectangleList(recs)
         dc.DrawLineList(lines) 
                 
             
             
         
         
         
        
        
        
    def DrawCandleLine(self, dc, rec, upperLine, lowerLine):
        stock = StockRealtime("")
        stock.open = 300
        stock.close = 320
        stock.high = 390
        stock.low = 290
        size=self.GetClientSize()
        W = size.width
        H = size.height
        pen=wx.Pen('blue',1)
        dc.SetPen(pen)
        rects = []
        rec = (W/2, H/2, 10, abs(stock.close-stock.open))
        rects.append(rec)
        upperLine = (rec[0]+rec[2]/2, rec[1], rec[0]+rec[2]/2, rec[1]-(stock.high-stock.close))
        lowerLine = (rec[0]+rec[2]/2, rec[1]+rec[3], rec[0]+rec[2]/2, rec[1]+rec[3]+(stock.close - stock.low))
        lines = [upperLine, lowerLine]
        dc.DrawRectangleList(rects)
        dc.DrawLineList(lines)

    def OnEraseBack(self, event):
        pass # do nothing to avoid flicker

    def OnPaint(self, event):
        if self.InitBuffer():
            self.Refresh() # buffer changed paint in next event, this paint event may be old
            return

        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.Buffer, 0, 0)
        
        
        self.DrawCandleLineList(dc, self.__stockList)

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=SketchFrame(None)
    frame.Show(True)
    app.MainLoop()