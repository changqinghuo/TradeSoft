import wx
from wx.lib.pubsub import Publisher as pub
from view.CandlePanel import *
from view.MainWindow import *
from view.SubWindow import MyChildFrame
from model.DataManager import *
from util.draw import *
from util.czsc import ChanlunCore
import threading

class Control:
    def __init__(self, app):        
        
        #main window
        self.mainwindow = MyParentFrame()           
        self.mainwindow.Bind(wx.EVT_MENU, self.On5MinAnalysis, id=ID_Menu_5Min)
        self.mainwindow.Bind(wx.EVT_MENU, self.On30MinAnalysis, id=ID_Menu_30Min)
        self.mainwindow.Bind(wx.EVT_MENU, self.OnDayAnalysis, id=ID_Menu_Day)
        self.mainwindow.Bind(wx.EVT_MENU, self.OnNewRealtimeWindow, id=ID_Menu_Realtime) 
        self.mainwindow.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.mainwindow.symbol_ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnSymbolCtrlEnter)  
        self.mainwindow.Show(True)
        app.SetTopWindow(self.mainwindow)
        self.mainwindow.SetFocus()
        
        self.symbol = '000001'
        

       
        #subwindow initialize
        self._InitComponet()
             
        #model initialize
        self.data_manager = DataManager() 
        self.data_manager.start()        
        self.data_manager.UpdateSymbol(self.symbol)
        #self.realtime_data = self.data_manager.GetQuoteData(self.symbol, 60, 1).df
        #self.analysis_data = self.data_manager.GetQuoteData(self.symbol, 1800, 30).df 
        self._lastclose = self.data_manager.GetLastClose(self.symbol)
        self.realtime_data = None
        self.analysis_data = None
        #for d in self.data_manager.symbol_quote_dict.keys():            
        pub.subscribe(self.AnalysisDataArrive, "ANALYSISDATA")
        pub.subscribe(self.RealtimeDataArrive, "REALTIMEDATA")
        pub.subscribe(self.Min30DataArrive, "MIN30DATA")
        pub.subscribe(self.DayDataArrive, "DAYDATA")
        
        
        
        
        
    def Min30DataArrive(self, message):
        self.min30_window.SetStockData(self.symbol, message.data, "30Min")  
    
    def DayDataArrive(self, message):
        self.day_window.SetStockData(self.symbol, message.data, "Day")  
        
    def _InitComponet(self):
        self.realtime_window = MyChildFrame(self.mainwindow, -1)
        self.realtime_window.SetStockData(self.symbol, None, "1Min")  
        
        self.analysis_window =  MyChildFrame(self.mainwindow, -1)
        self.min30_window = MyChildFrame(self.mainwindow, -1)
        self.day_window = MyChildFrame(self.mainwindow, -1)
        self.analysis_window.SetStockData(self.symbol, None, "5Min") 
        self.min30_window.SetStockData(self.symbol, None, "30Min")
        self.day_window.SetStockData(self.symbol, None, "Day")
        
        
    def OnSymbolCtrlEnter(self, evt):
        sym = self.mainwindow.symbol_ctrl.GetValue()
        if sym in self.data_manager.symbol_dict:
            self.symbol = sym
            self.analysis_window.SetStockData(self.symbol, None, "5Min") 
            self.min30_window.SetStockData(self.symbol, None, "30Min")
            self.day_window.SetStockData(self.symbol, None, "Day")
            self.realtime_window.SetStockData(self.symbol, None, "1Min")
            self.data_manager.UpdateSymbol(sym)
#            self.realtime_window.SetTitle(sym)
#            self.analysis_window.SetTitle(sym)
            self._lastclose = self.data_manager.GetLastClose(sym)
        
    def OnKeyDown(self, evt):
        keycode = evt.GetKeyCode()
        print keycode


    def OnAnalysisPaint(self, evt):
        
        dc = wx.PaintDC(self.analysis_window.main_panel)
        dc.Clear()     
        draw_candle(dc, self.analysis_data)
        czsc = ChanlunCore()
        czsc.Draw(dc, self.analysis_data)
        print "refreshing analysis"
                

    def OnEraseBack(self, evt):        
        pass
    def AnalysisDataArrive(self, message):
        #if self.analysis_window.IsShownOnScreen():           
        self.analysis_data = message.data 
        self.analysis_window.SetStockData(self.symbol, message.data, "5Min")      
        #self.analysis_window.Refresh()  
        #self.analysis_window.Refresh()
    def On5MinAnalysis(self, evt):
           
        self.analysis_window.Show(True)
        self.analysis_window.SetFocus()
    
    def On30MinAnalysis(self, evt):  
        self.min30_window.Show(True)
        self.min30_window.SetFocus()
    
    def OnDayAnalysis(self, evt):
        self.day_window.Show(True)
        self.day_window.SetFocus()
    
    def OnNewRealtimeWindow(self, evt):              
        self.realtime_window.Show(True)
        self.realtime_window.SetFocus()
        
    def OnRealtimePaint(self, evt):
       dc = wx.PaintDC(self.realtime_window.main_panel)
       #dc.DrawBitmap(self.Buffer, 0, 0) 
       dc.Clear()     
       draw_realtime(dc, self.realtime_data, self._lastclose)
       
    def RealtimeDataArrive(self, message):      
        self.realtime_data = message.data
        self.realtime_window.SetStockData(self.symbol, message.data, "1Min")    
#        self.realtime_window.main_panel.data =  message.data   
#        self.realtime_window.main_panel.Refresh()  
        

        
        
        
        



