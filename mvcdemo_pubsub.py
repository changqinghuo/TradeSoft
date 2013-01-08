#!/usr/bin/env python

"""
An example of a Model-View-Controller architecture,
using wx.lib.pubsub to handle proper updating of widget (View) values.
"""
import wx
from wx.lib.pubsub import Publisher as pub

class Model:
    def __init__(self):
        self.myMoney = 0

    def addMoney(self, value):
        self.myMoney += value
        #now tell anyone who cares that the value has been changed
        pub.sendMessage("MONEY CHANGED", self.myMoney)

    def removeMoney(self, value):
        self.myMoney -= value
        #now tell anyone who cares that the value has been changed
        pub.sendMessage("MONEY CHANGED", self.myMoney)

class View(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main View")

        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label="My Money")
        ctrl = wx.TextCtrl(self)
        sizer.Add(text, 0, wx.EXPAND | wx.ALL)
        sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)

        self.moneyCtrl = ctrl
        ctrl.SetEditable(False)
        self.SetSizer(sizer)

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

        #set up the first frame which displays the current Model value
        self.view1 = View(None)
        self.view1.SetMoney(self.model.myMoney)

        #set up the second frame which allows the user to modify the Model's value
        self.view2 = ChangerWidget(self.view1)
        self.view2.add.Bind(wx.EVT_BUTTON, self.AddMoney)
        self.view2.remove.Bind(wx.EVT_BUTTON, self.RemoveMoney)
        #subscribe to all "MONEY CHANGED" messages from the Model
        #to subscribe to ALL messages (topics), omit the second argument below
        pub.subscribe(self.MoneyChanged, "MONEY CHANGED")

        self.view1.Show()
        self.view2.Show()

    def AddMoney(self, evt):
        self.model.addMoney(10)

    def RemoveMoney(self, evt):
        self.model.removeMoney(10)

    def MoneyChanged(self, message):
        """
        This method is the handler for "MONEY CHANGED" messages,
        which pubsub will call as messages are sent from the model.

        We already know the topic is "MONEY CHANGED", but if we
        didn't, message.topic would tell us.
        """
        self.view1.SetMoney(message.data)

if __name__ == "__main__":
    app = wx.App(False)
    controller = Controller(app)
    app.MainLoop()