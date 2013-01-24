import wx
from wx.lib.pubsub import Publisher as pub
from view.AnalysisPanel import *
from view.MainWindow import *
from model.DataManager import *
from util.draw import *
import threading

class Control:
    def __init__(self, app):        
        self.model = DataManager() 
        self.mainwindow = MyParentFrame()           
        self.mainwindow.Bind(wx.EVT_MENU, self.OnNewAnalysisWindow, id=ID_Menu_New)
        
        
        
        
        self.mainwindow.Show(True)
        app.SetTopWindow(self.mainwindow)
        self.analysis_data = self.model.GetQuoteData('002094', 300, 5).df
        
        for d in self.model.symbol_quote_dict.keys():            
            pub.subscribe(self.AnalysisDataArrive, d+"ANALYSISDATA")
        


    def OnAnalysisPaint(self, evt):
       dc = wx.PaintDC(self.analysis_panel)
       #dc.DrawBitmap(self.Buffer, 0, 0) 
       dc.Clear()     
       draw_candle(dc, self.analysis_data)
                

    def OnEraseBack(self, evt):        
        pass
    def AnalysisDataArrive(self, message):        
        self.analysis_data = message.data
        self.analysis_panel.Refresh()
    def OnTimer(self, evt):
        self.model.GetQuoteData('002094', 300, 5)
    def OnNewAnalysisWindow(self, evt):
        win = wx.MDIChildFrame(self.mainwindow, -1, "Child Window: %d" % 1)
        self.timer = wx.Timer(win)
        #win.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.analysis_panel = AnalysisPanel(win)
        self.analysis_panel.Bind(wx.EVT_PAINT, self.OnAnalysisPaint)
        self.analysis_panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        #self.timer.Start(5000)        
        #canvas = ScrolledWindow.MyCanvas(win)
        win.Show(True)
        #t = threading.Thread(target=self.model.QuoteDataThreads())
        #t.start()
        self.model.start()

        
        
        
        



