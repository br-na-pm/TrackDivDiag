class ExportConfig():
    def __init__(self, SectorExportEnabled = True,
                    TaskInitExportEnabled = True,
                    TaskVarExportEnabled = True) -> None:
        self.SectorExportEnabled = SectorExportEnabled
        self.TaskInitExportEnabled = TaskInitExportEnabled
        self.TaskVarExportEnabled = TaskVarExportEnabled