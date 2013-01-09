import wx
import random
from sina_parse_realtime import StockData

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
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)

        
        
    
    def OnClick(self, event):
        print event.GetPosition()
        

    def InitBuffer(self):
        size=self.GetClientSize()
        # if buffer exists and size hasn't changed do nothing
        if self.Buffer is not None and self.Buffer.GetWidth() == size.width and self.Buffer.GetHeight() == size.height:
            return False
        
        self.Buffer=wx.EmptyBitmap(size.width,size.height)
        dc=wx.MemoryDC()
        #dc = wx.ClientDC()
        dc.SelectObject(self.Buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.__stockList = []
        for i in range(100):
            stock = StockData("")
            stock.open = random.uniform(1.,100.)
            stock.close = random.uniform(1.,100.)
            stock.high = max(stock.open, stock.close) + random.uniform(1.,10.)
            stock.low = min(stock.open, stock.close)- random.uniform(1.,10.)
            self.__stockList.append(stock)
       
        
        self.DrawCandleLineList(dc, self.__stockList)
        dc.SelectObject(wx.NullBitmap)
        return True

    def __getStockDataListRange(self, stockdataList):
        highlist = [s.high for s in stockdataList]
        lowlist = [s.low for s in stockdataList]
        return (max(highlist), min(lowlist))
    
    def DrawCandleLineList(self, dc, stockdataList):
                                
        size=self.GetClientSize()         
        windowWidth = size.width-10
        windowHeight = size.height-10
        dc.SetDeviceOrigin(0, windowHeight)
        dc.SetAxisOrientation(True, True)

        stockRange = self.__getStockDataListRange(stockdataList)
        recwidth = windowWidth/len(stockdataList)-2  
        for i in range(len(stockdataList)):
            stock = stockdataList[i]
            pricediff = stockRange[1] - stockRange[0]
            recheight = windowHeight*abs(stock.close - stock.open)/pricediff
            x = i*windowWidth/len(stockdataList)
            upperlineendY = (stock.high - stockRange[0])*windowHeight/pricediff                 
            lowerlineendY = (stock.low - stockRange[0])*windowHeight/pricediff
            drop = False
            if stock.close >= stock.open:                 
                y = upperlineendY - (stock.high - stock.open)*windowHeight/pricediff       
            else:                
                drop = True             
                y = upperlineendY - (stock.high - stock.close)*windowHeight/pricediff  
                   
            rec = (x, y, recwidth, recheight)
            upperline = (x+recwidth/2, y+recheight, x+recwidth/2, upperlineendY)
            lowerline = (x+recwidth/2, y, x+recwidth/2, lowerlineendY)
           
            if drop:
                dc.SetBrush(wx.BLACK_BRUSH)
            else:                
                dc.SetBrush(wx.WHITE_BRUSH)
            dc.DrawRectangle(rec[0], rec[1], rec[2], rec[3])
            dc.DrawLine(upperline[0], upperline[1], upperline[2], upperline[3])
            dc.DrawLine(lowerline[0], lowerline[1], lowerline[2], lowerline[3])
            


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