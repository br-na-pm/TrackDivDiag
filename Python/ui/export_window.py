from pathlib import Path
from src.AssemblyParse import ASProject
from src.export_cfg import ExportConfig
from ui.popup_dialog import popupDialog
import wx
import wx.xrc
import time

class ExportWindow ( wx.Frame ):

    def __init__( self, parent , Project : ASProject):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Export Diverter Test Task..", pos = wx.DefaultPosition, size = wx.Size( 802,247 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL ) # Initializes window   
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )    
        gSizer4 = wx.GridSizer( 0, 1, 1, 0 )    
        fgSizer6 = wx.FlexGridSizer( 0, 1, 0, 0 )
        fgSizer6.SetFlexibleDirection( wx.BOTH )
        fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )   
        fgSizer4 = wx.FlexGridSizer( 0, 2, 1, 0 )
        fgSizer4.SetFlexibleDirection( wx.BOTH )
        fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )   
        self.cbUpdateSectorFile = wx.CheckBox( self, wx.ID_ANY, u"Sector File Path", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cbUpdateSectorFile.SetValue(True)
        fgSizer4.Add( self.cbUpdateSectorFile, 0, wx.ALL, 5 )   
        self.fpSectorFilePath = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 650,-1 ), wx.FLP_USE_TEXTCTRL|wx.FLP_FILE_MUST_EXIST)
        fgSizer4.Add( self.fpSectorFilePath, 0, wx.ALL, 5 ) 
        self.cbUpdateInitFile = wx.CheckBox( self, wx.ID_ANY, u"Task Init File Path", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cbUpdateInitFile.SetValue(True)
        fgSizer4.Add( self.cbUpdateInitFile, 0, wx.ALL, 5 ) 
        self.fpTaskInitFilePath = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 650,-1 ), wx.FLP_USE_TEXTCTRL|wx.FLP_FILE_MUST_EXIST)
        fgSizer4.Add( self.fpTaskInitFilePath, 0, wx.ALL, 5 )   
        self.cbUpdateVarFile = wx.CheckBox( self, wx.ID_ANY, u"Task .var File Path", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cbUpdateVarFile.SetValue(True)
        fgSizer4.Add( self.cbUpdateVarFile, 0, wx.ALL, 5 )  
        self.fpTaskVarFilePath = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 650,-1 ), wx.FLP_USE_TEXTCTRL|wx.FLP_FILE_MUST_EXIST)
        fgSizer4.Add( self.fpTaskVarFilePath, 0, wx.ALL, 5 )    
        fgSizer6.Add( fgSizer4, 1, wx.BOTTOM|wx.EXPAND, 15 )    
        fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer5.SetFlexibleDirection( wx.BOTH )
        fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )   
        self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, u"Number of Diverts:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText24.Wrap( -1 )  
        fgSizer5.Add( self.m_staticText24, 0, wx.ALL, 5 )   
        self.m_numDiverts = wx.StaticText( self, wx.ID_ANY, u"##", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_numDiverts.Wrap( -1 )    
        fgSizer5.Add( self.m_numDiverts, 0, wx.ALL, 5 ) 
        fgSizer6.Add( fgSizer5, 1, wx.EXPAND, 5 )   
        self.btnExport = wx.Button( self, wx.ID_ANY, u"Export", wx.DefaultPosition, wx.Size( 150,50 ), 0 )
        fgSizer6.Add( self.btnExport, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 ) 
        gSizer4.Add( fgSizer6, 1, wx.EXPAND, 5 )    
        self.SetSizer( gSizer4 )
        self.Layout()   
        self.Centre( wx.BOTH )  

        self.cbUpdateInitFile.Bind(wx.EVT_CHECKBOX,lambda evt, name = "UpdateInitFile":self.onCbClicked(evt,name))
        self.cbUpdateSectorFile.Bind(wx.EVT_CHECKBOX,lambda evt, name = "UpdateSectorFile":self.onCbClicked(evt,name))
        self.cbUpdateVarFile.Bind(wx.EVT_CHECKBOX,lambda evt, name = "UpdateVarFile":self.onCbClicked(evt,name))

        self.btnExport.Bind(wx.EVT_BUTTON,self.onExportClicked)

        self.fpSectorFilePath.Bind(wx.EVT_FILEPICKER_CHANGED, self.onTextModify)            #Created event binding for any change to the filepicker box
        self.fpTaskVarFilePath.Bind(wx.EVT_FILEPICKER_CHANGED, self.onTextModify)
        self.fpTaskInitFilePath.Bind(wx.EVT_FILEPICKER_CHANGED, self.onTextModify)
        
        self.Project = Project
        self.exportCfg = ExportConfig()

        defaultPath = True
        if defaultPath:               #Changed Lines 68-73 to only execute if the input field has not modified (User wants to use a different path from parser-derived one)
            self.fpSectorFilePath.SetPath(str(Project.SectorPath.absolute()))                   
        if defaultPath:
            self.fpTaskVarFilePath.SetPath(str(Project.MaintVarsPath.absolute()))
        if defaultPath:    
            self.fpTaskInitFilePath.SetPath(str(Project.MaintInitPath.absolute()))

        self.m_numDiverts.LabelText = str(len(Project.Diverts))
    
    def __del__( self ):
        pass

    def onCbClicked(self, event, name):
        if name == "UpdateSectorFile":
            self.exportCfg.SectorExportEnabled = self.cbUpdateSectorFile.GetValue()
        elif name == "UpdateInitFile":
            self.exportCfg.TaskInitExportEnabled = self.cbUpdateInitFile.GetValue()
        elif name == "UpdateVarFile":
            self.exportCfg.TaskVarExportEnabled = self.cbUpdateVarFile.GetValue()
    
    def onTextModify(self, event):
        defaultPath = False
                         
        self.Project.SectorPath =  Path(self.fpSectorFilePath.GetPath())                        
        self.Project.MaintVarsPath = Path(self.fpTaskVarFilePath.GetPath())
        self.Project.MaintInitPath = Path(self.fpTaskInitFilePath.GetPath())
        
        
    def onExportClicked(self, event):
        try:
            self.Project.ExportProject(self.exportCfg)
            popupFenster = popupDialog(None, popupWords="Export Successful")
            popupFenster.Show(True)
        except: 
            popupFenster = popupDialog(None, popupWords="Export Failed")
            popupFenster.Show(True)
        time.sleep(1.5)
        self.Destroy()
        popupFenster.Destroy()