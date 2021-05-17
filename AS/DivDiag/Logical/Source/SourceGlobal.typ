
TYPE
	SysStateEnum : 
		(
		SYS_OFF,
		SYS_POWERING_ON,
		SYS_POWERING_OFF,
		SYS_ADD_SHUTTLE,
		SYS_IDLE,
		SYS_ERROR
		);
	SysIfTyp : 	STRUCT 
		Cmd : SysIfCmdTyp;
		Sts : SysIfStsTyp;
	END_STRUCT;
	SysIfCmdTyp : 	STRUCT 
		PowerOn : BOOL;
	END_STRUCT;
	SysIfStsTyp : 	STRUCT 
		Powered : BOOL;
		ShuttleAdded : BOOL;
	END_STRUCT;
	SysFbsTyp : 	STRUCT 
		AsmPowerFb : MC_BR_AsmPowerOn_AcpTrak;
		AsmPowerOffFb : MC_BR_AsmPowerOff_AcpTrak;
		AddShuttleFb : MC_BR_SecAddShuttle_AcpTrak;
	END_STRUCT;
END_TYPE
