import wx
from wx.lib.pubsub import Publisher as pub
from view.AnalysisPanel import *
from view.MainWindow import *
from model.DataManager import *
from util.draw import *
import threading

class Control:
    def __init__(self, app):        
        
        self.mainwindow = MyParentFrame()           
        self.mainwindow.Bind(wx.EVT_MENU, self.OnNewAnalysisWindow, id=ID_Menu_Aanalysis)
        self.mainwindow.Bind(wx.EVT_MENU, self.OnNewRealtimeWindow, id=ID_Menu_Realtime)
        
        
        self.mainwindow.Show(True)
        app.SetTopWindow(self.mainwindow)      
        
        
        
        self.mainwindow.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.mainwindow.symbol_ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnSymbolCtrlEnter)      
        
        self.data_manager = DataManager() 
        self.data_manager.start()
        self.symbol = '002094'
        self.data_manager.UpdateSymbol(self.symbol)
        #self.realtime_data = self.data_manager.GetQuoteData(self.symbol, 60, 1).df
        #self.analysis_data = self.data_manager.GetQuoteData(self.symbol, 1800, 30).df 
        self._lastclose = self.data_manager.GetLastClose(self.symbol)
        self.realtime_data = None
        self.analysis_data = None
        #for d in self.data_manager.symbol_quote_dict.keys():            
        pub.subscribe(self.AnalysisDataArrive, "ANALYSISDATA")
        pub.subscribe(self.RealtimeDataArrive, "REALTIMEDATA")
        self.mainwindow.SetFocus()
        self.realtime_window = None
        self.analysis_window = None
        

    def OnSymbolCtrlEnter(self, evt):
        sym = self.mainwindow.symbol_ctrl.GetValue()
        if sym in self.data_manager.symbol_dict:
            self.symbol = sym
            self.data_manager.UpdateSymbol(sym)
            self.realtime_window.SetTitle(sym)
            self.analysis_window.SetTitle(sym)
            self._lastclose = self.data_manager.GetLastClose(sym)
        
    def OnKeyDown(self, evt):
        keycode = evt.GetKeyCode()
        print keycode


    def OnAnalysisPaint(self, evt):
       dc = wx.PaintDC(self.analysis_panel)
       #dc.DrawBitmap(self.Buffer, 0, 0) 
       dc.Clear()     
       draw_candle(dc, self.analysis_data)
                

    def OnEraseBack(self, evt):        
        pass
    def AnalysisDataArrive(self, message):
        #if self.analysis_window.IsShownOnScreen():           
            self.analysis_data = message.data
            self.analysis_panel.Refresh()  
    def OnNewAnalysisWindow(self, evt):
        if self.analysis_window is None:            
            self.analysis_window = wx.MDIChildFrame(self.mainwindow, -1, "Analysis Window:"+self.symbol)
            self.analysis_panel = AnalysisPanel(self.analysis_window)
            self.analysis_panel.Bind(wx.EVT_PAINT, self.OnAnalysisPaint)
            self.analysis_panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        else:        
            self.analysis_window.Show(True)
            self.analysis_window.SetFocus()
       
    
    def OnNewRealtimeWindow(self, evt):
        if self.realtime_window is None:
            self.realtime_window = wx.MDIChildFrame(self.mainwindow, -1, "Realtime Window:"+self.symbol)
            self.realtime_panel = AnalysisPanel(self.realtime_window)
            self.realtime_panel.Bind(wx.EVT_PAINT, self.OnRealtimePaint)
            self.realtime_panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        else:        
            self.realtime_window.Show(True)
            self.realtime_window.SetFocus()
    def OnRealtimePaint(self, evt):
       dc = wx.PaintDC(self.realtime_panel)
       #dc.DrawBitmap(self.Buffer, 0, 0) 
       dc.Clear()     
       draw_realtime(dc, self.realtime_data, self._lastclose)
    def RealtimeDataArrive(self, message):      
        self.realtime_data = message.data
        self.realtime_panel.Refresh()  
        

        
        
        
        



