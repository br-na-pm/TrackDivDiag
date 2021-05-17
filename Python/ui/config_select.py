import wx
import wx.xrc
import wx.grid

class ConfigSelectWindow ( wx.Frame ):

    def __init__( self, parent, configs ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Select Configuration", pos = wx.DefaultPosition, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.parent = parent

        sizer = wx.GridSizer(2,len(configs),0,0)
        self.cfgOptions = []
        for cfg in configs:
            b = wx.Button(self,label=cfg)
            b.Name = cfg
            sizer.Add(b)
            b.Bind(wx.EVT_BUTTON,self.onCfgSelect,b)
            self.cfgOptions.append(b)
         
        self.SetSizer(sizer)
        self.Layout()
    
    def onCfgSelect(self, evt):
        self.parent.onCfgSelected(evt.GetEventObject().Name)
        self.Destroy()