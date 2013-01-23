import wx
import pandas as pd

def dfrange(df):
    pass


def draw_candle(dc, df):
    """ dc: device context
        df: pandas.dataframe
                   open high low close volume
        datetime   xx   xx   xx   xx    xx
    """
    size=dc.GetSize()         
    windowWidth = size.width-50
    windowHeight = size.height-100
    dc.SetDeviceOrigin(0, windowHeight)
    dc.SetAxisOrientation(True, True)    
    

    stockRange = (pd.Series.min(df['low']), pd.Series.max(df['high']))
    dfindex_len = df.shape[0]   
    recwidth = float(windowWidth)/dfindex_len
    i = 0
    for dt in df.index:
        row = df.ix[i]
        close = row['close']
        high = row['high']
        open = row['open']
        low = row['low']
        pricediff = stockRange[1] - stockRange[0]
        recheight = windowHeight*abs(close - open)/pricediff+1
        x = i*windowWidth/dfindex_len + 1        
        upperlineendY = (high - stockRange[0])*windowHeight/pricediff                 
        lowerlineendY = (low - stockRange[0])*windowHeight/pricediff
        drop = False
        if close >= open:                 
            y = upperlineendY - (high - open)*windowHeight/pricediff       
        else:                
            drop = True             
            y = upperlineendY - (high - close)*windowHeight/pricediff  
                   
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
        i = i+1