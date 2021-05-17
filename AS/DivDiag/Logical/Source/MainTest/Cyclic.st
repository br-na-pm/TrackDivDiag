
PROGRAM _CYCLIC
	CASE state OF
		SYS_OFF:
			IF gSysIf.Cmd.PowerOn THEN
				sysFbs.AsmPowerFb.Assembly := ADR(gMcAssembly01);
				sysFbs.AsmPowerFb.Execute := TRUE;
				state := SYS_POWERING_ON;
			END_IF
		SYS_POWERING_ON:
			IF sysFbs.AsmPowerFb.Done THEN
				gSysIf.Sts.Powered := TRUE;
				
				IF gSysIf.Sts.ShuttleAdded THEN
					state := SYS_IDLE;
				ELSE
					sysFbs.AddShuttleFb.Position := 0;
					sysFbs.AddShuttleFb.Sector := ADR(gDivSector_0);
					sysFbs.AddShuttleFb.Execute := TRUE;
					
					state := SYS_ADD_SHUTTLE;
				END_IF
			END_IF
		SYS_POWERING_OFF:
			IF sysFbs.AsmPowerOffFb.Done THEN
				sysFbs.AsmPowerOffFb.Execute := FALSE;
				gSysIf.Sts.Powered := FALSE;
				state := SYS_OFF;
			END_IF	
		SYS_ADD_SHUTTLE:
			IF sysFbs.AddShuttleFb.Error THEN
				state := SYS_ERROR;
			ELSIF sysFbs.AddShuttleFb.Done THEN
				sysFbs.AddShuttleFb.Execute := FALSE;
				gSysIf.Sts.ShuttleAdded := TRUE;
				
				state := SYS_IDLE;
			END_IF
		SYS_IDLE:
			IF NOT gSysIf.Cmd.PowerOn THEN
				sysFbs.AsmPowerOffFb.Execute := TRUE;
				sysFbs.AsmPowerOffFb.Assembly := ADR(gMcAssembly01);
				
				state := SYS_POWERING_OFF;
			END_IF
		SYS_ERROR:
	
	END_CASE;
	
	sysFbs.AsmPowerFb();
	sysFbs.AsmPowerOffFb();
	sysFbs.AddShuttleFb();
		 
END_PROGRAM
