
from ui.add_new_implicit import AddImplicitWindow
from ui.config_select import ConfigSelectWindow
import wx
import wx.xrc
import wx.grid
import wx.svg
import os
import src.AssemblyParse
###########################################################################
## Class Main
###########################################################################

class MainWindow ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Diverter Diagnostic Task Builder", pos = wx.DefaultPosition, size = wx.Size( 1280,800 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.miFileImportProject = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Import Project", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.miFileImportProject )

        self.Export = wx.MenuItem(self.m_menu1, wx.ID_ANY, "Export", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append( self.Export)

        self.m_menu2 = wx.Menu()
        self.miAddImplicitDivert = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Add Implicit Divert", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append(self.miAddImplicitDivert)

        self.m_menubar1.Append( self.m_menu1, u"File" )
        self.m_menubar1.Append( self.m_menu2, u"Edit" )

        self.SetMenuBar( self.m_menubar1 )

        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        gSizer1 = wx.GridSizer( 0, 2, 0, 0 )

        self.m_grid1 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.m_grid1.CreateGrid( 1, 9 )
        self.m_grid1.EnableEditing( True )
        self.m_grid1.EnableGridLines( True )
        self.m_grid1.EnableDragGridSize( False )
        self.m_grid1.SetMargins( 0, 0 )
        
        # Columns
        
        self.m_grid1.SetColSize( 0, 130 )
        self.m_grid1.SetColSize( 1, 90 )
        self.m_grid1.SetColSize( 2, 80 )
        self.m_grid1.SetColSize( 3, 80 )
        self.m_grid1.SetColSize( 4, 130 )
        self.m_grid1.SetColSize( 5, 90 )
        self.m_grid1.SetColSize( 6, 80 )
        self.m_grid1.SetColSize( 7, 80 )
        self.m_grid1.SetColSize( 8, 130 )
        self.m_grid1.EnableDragColMove( False )
        self.m_grid1.EnableDragColSize( True )
        self.m_grid1.SetColLabelSize( 30 )
        self.m_grid1.SetColLabelValue( 0, u"Spur Segment Name" )
        self.m_grid1.SetColLabelValue( 1, u"Segment Type" )
        self.m_grid1.SetColLabelValue( 2, u"Relative To" )
        self.m_grid1.SetColLabelValue( 3, u"Position" )
        self.m_grid1.SetColLabelValue( 4, u"Base Segment Name" )
        self.m_grid1.SetColLabelValue( 5, u"Segment Type" )
        self.m_grid1.SetColLabelValue( 6, u"Position" )
        self.m_grid1.SetColLabelValue( 7, u"Relative To" )
        self.m_grid1.SetColLabelValue( 8, u"Reference Segment" )
        self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.m_grid1.EnableDragRowSize( True )
        self.m_grid1.SetRowLabelSize( 80 )
        self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )
        
        self.m_grid1.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.onGridCellChanged)
        # Label Appearance

        # Cell Defaults
        self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        gSizer1.Add( self.m_grid1, 0, wx.ALL, 5 )

        # self.img = wx.svg.SVGimage.CreateFromFile("./gMcAssembly01.svg")
        # self.Bind(wx.EVT_PAINT, self.onPaint)

        self.SetSizer( gSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

		# Connect Events
        self.Bind( wx.EVT_MENU, self.onFileImportProjectSelection, id = self.miFileImportProject.GetId() )
        self.Bind( wx.EVT_MENU, self.onAddImplicitDivert, id = self.miAddImplicitDivert.GetId() )
        self.Bind(wx.EVT_MENU, self.onExportSelection, id= self.Export.GetId()
        )


    def __del__( self ):
        pass

	# Virtual event handlers, overide them in your derived class

    def onAddImplicitDivert(self, event):
        keys = self.Proj.Segments.keys()
        addImplicit = AddImplicitWindow(self,list(keys))
        addImplicit.Show()

    def onAddDivertConfirm(self,spurName, baseName) -> None:
        divert = src.AssemblyParse.Diverter(src.AssemblyParse.DivReferenceType.RelToOne,self.Proj.Segments[spurName],self.Proj.Segments[baseName])
        self.m_grid1.AppendRows(1)
        idx = self.m_grid1.GetNumberRows()-1
        choices = []
        choices.append(divert.SpurTrackSegment.SegName)
        choices.append(divert.BaseTrackSegment.SegName)
        self.m_grid1.SetCellValue(idx,0,divert.SpurTrackSegment.SegName)
        self.m_grid1.SetCellValue(idx,1,str(divert.SpurTrackSegment.SegmentType))
        self.m_grid1.SetCellValue(idx,2,str(divert.SpurTrackSegment.RelativeTo))
        self.m_grid1.SetCellValue(idx,3,str(divert.SpurTrackSegment.Position))
        self.m_grid1.SetCellValue(idx,4,divert.BaseTrackSegment.SegName)
        self.m_grid1.SetCellValue(idx,5,str(divert.BaseTrackSegment.SegmentType))
        self.m_grid1.SetCellValue(idx,6,str(divert.BaseTrackSegment.RelativeTo))
        self.m_grid1.SetCellValue(idx,7,str(divert.BaseTrackSegment.Position))
        choice_editor = wx.grid.GridCellChoiceEditor(choices)
        self.m_grid1.SetCellEditor(idx,8,choice_editor)
        self.m_grid1.SetCellValue(idx,8,choices[0])
        self.Proj.Diverts.append(divert)

    def onFileImportProjectSelection( self, event ):
        dlg = wx.DirDialog(None,"Choose directory","",wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dlg.ShowModal()
        self.Proj = src.AssemblyParse.ASProject(dlg.GetPath())
        configs = next(os.walk(self.Proj.ProjectPath+"\\Physical\\"))[1]
        if len(configs) > 1:
            cfgSelect = ConfigSelectWindow(self,configs)
            cfgSelect.Show()

    def onCfgSelected(self,CfgName):
        self.Proj.Config = CfgName
        self.Proj.parseProject()
        self.fillGrid(self.Proj.Diverts)

    def fillGrid(self,DivertList):
        self.m_grid1.ClearGrid()
        self.m_grid1.AppendRows(len(DivertList)-1)
        for idx,divert in enumerate(DivertList):
            choices = []
            choices.append(divert.SpurTrackSegment.SegName)
            choices.append(divert.BaseTrackSegment.SegName)
            self.m_grid1.SetCellValue(idx,0,divert.SpurTrackSegment.SegName)
            self.m_grid1.SetCellValue(idx,1,str(divert.SpurTrackSegment.SegmentType))
            self.m_grid1.SetCellValue(idx,2,str(divert.SpurTrackSegment.RelativeTo))
            self.m_grid1.SetCellValue(idx,3,str(divert.SpurTrackSegment.Position))
            self.m_grid1.SetCellValue(idx,4,divert.BaseTrackSegment.SegName)
            self.m_grid1.SetCellValue(idx,5,str(divert.BaseTrackSegment.SegmentType))
            self.m_grid1.SetCellValue(idx,6,str(divert.BaseTrackSegment.RelativeTo))
            self.m_grid1.SetCellValue(idx,7,str(divert.BaseTrackSegment.Position))
            choice_editor = wx.grid.GridCellChoiceEditor(choices)
            self.m_grid1.SetCellEditor(idx,8,choice_editor)
            self.m_grid1.SetCellValue(idx,8,choices[0])
            
        self.m_grid1.AutoSize()

    def onGridCellChanged(self,event):
        r = event.GetRow()
        c = event.GetCol()
        if c == 0 or c == 4:
            #If the cell that was changed was a segment name, validate the segment name and update the type
            if c == 0: self.setSpurInformation(self.m_grid1.GetCellValue(r,c),r)
            if c == 4: self.setSpurInformation(self.m_grid1.GetCellValue(r,c),r)
            #If the cell that was changed was a position or a reference to, update the diverter information on that index
            print(self.m_grid1.GetCellValue(r,c))

    def onExportSelection(self,event):
        self.Proj.exportProject()
    

