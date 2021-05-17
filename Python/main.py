import wx
from ui.main_window import MainWindow

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None)
    frame.Show(True)
    app.MainLoop()
    
