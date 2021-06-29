import wx
import wx.xrc
import wx.grid

from src.AssemblyParse import DivReferenceType, Diverter, Segment

class AddImplicitWindow ( wx.Frame ):

    def __init__( self, parent , segList):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Add New Implicit Divert", size = wx.Size( 374,161 ), pos = wx.DefaultPosition, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.parent = parent
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
        gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
        
        fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Spur Segment", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
        self.m_staticText1.Wrap( -1 )
        
        fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        sortedSegList = sorted(segList, key = lambda x:x.lower())                       #Sorts the segments alphabetically
        self.cbSpurSegment = wx.ComboBox( self, wx.ID_ANY, u"Segment Name", wx.DefaultPosition, wx.Size( 200,-1 ), sortedSegList, 0 )
        fgSizer1.Add( self.cbSpurSegment, 0, wx.ALL, 5 )
        
        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Base Segment", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        
        fgSizer1.Add( self.m_staticText11, 0, wx.ALL, 5 )
        
        self.cbBaseSegment = wx.ComboBox( self, wx.ID_ANY, u"Segment Name", wx.DefaultPosition, wx.Size( 200,-1 ), sortedSegList, 0 )
        fgSizer1.Add( self.cbBaseSegment, 0, wx.ALL, 5 )
        
        self.btnAddDivert = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.btnAddDivert, 0, wx.ALL, 5 )
        
        
        gSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )
        
        self.btnAddDivert.Bind(wx.EVT_BUTTON, self.onAddDivert)
        
        self.SetSizer( gSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )

    def onAddDivert(self,event)-> None:
        self.parent.onAddDivertConfirm(self.cbSpurSegment.StringSelection, self.cbBaseSegment.StringSelection)
        self.Destroy ()