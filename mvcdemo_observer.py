#!/usr/bin/env python

import wx
# an observable calls callback functions when the data has changed
#o = Observable()
#def func(data):
# print "hello", data
#o.addCallback(func)
#o.set(1)
# --| "hello", 1
class Observable:
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
            func(self.data)

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None

class Model:
    def __init__(self):
        self.myMoney = Observable(0)

    def addMoney(self, value):
        self.myMoney.set(self.myMoney.get() + value)

    def removeMoney(self, value):
        self.myMoney.set(self.myMoney.get() - value)


class View(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main View")
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label="My Money")
        ctrl = wx.TextCtrl(self)
        sizer.Add(text, 0, wx.EXPAND | wx.ALL)
        sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)
        ctrl.SetEditable(False)
        self.SetSizer(sizer)
        self.moneyCtrl = ctrl

    def SetMoney(self, money):
        self.moneyCtrl.SetValue(str(money))


class ChangerWidget(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main View")
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.add = wx.Button(self, label="Add Money")
        self.remove = wx.Button(self, label="Remove Money")
        sizer.Add(self.add, 0, wx.EXPAND | wx.ALL)
        sizer.Add(self.remove, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

class Controller:
    def __init__(self, app):
        self.model = Model()
        self.view1 = View(None)
        self.view2 = ChangerWidget(self.view1)
        self.MoneyChanged(self.model.myMoney.get())
        self.view2.add.Bind(wx.EVT_BUTTON, self.AddMoney)
        self.view2.remove.Bind(wx.EVT_BUTTON, self.RemoveMoney)
        self.model.myMoney.addCallback(self.MoneyChanged)
        self.view1.Show()
        self.view2.Show()

    def AddMoney(self, evt):
        self.model.addMoney(10)

    def RemoveMoney(self, evt):
        self.model.removeMoney(10)

    def MoneyChanged(self, money):
        self.view1.SetMoney(money)

app = wx.App(False)
controller = Controller(app)
app.MainLoop()