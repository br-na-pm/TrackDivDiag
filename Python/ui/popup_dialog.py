import wx
import wx.xrc

class popupDialog ( wx.Dialog ):
    def __init__( self, parent, popupWords):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 300,200 ), style = wx.CAPTION|wx.DEFAULT_DIALOG_STYLE|wx.DIALOG_NO_PARENT|wx.STAY_ON_TOP )
        self.SetSizeHints( wx.Size( 300,200 ), wx.DefaultSize )
        popupSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
        self.popupText = wx.StaticText( popupSizer.GetStaticBox(), wx.ID_ANY, popupWords, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
        self.popupText.Wrap( -1 )
        self.popupText.SetMinSize( wx.Size( 200,100 ) )
        popupSizer.Add( self.popupText, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.popupButton = wx.Button( popupSizer.GetStaticBox(), wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        popupSizer.Add( self.popupButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        self.SetSizer( popupSizer )
        self.Layout()
        self.Centre( wx.BOTH )
        self.Bind(wx.EVT_BUTTON, self.onButtonClick)
    def __del__( self ):
        pass
    def onButtonClick( self , event):
        self.Destroy()