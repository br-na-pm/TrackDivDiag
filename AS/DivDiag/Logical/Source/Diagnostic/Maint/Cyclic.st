	
PROGRAM _CYCLIC
	
	mpReportFb.MpLink := ADR(gOffsetsReport);
	mpReportFb.DeviceName := ADR('Report');	//Change to match whatever file device your project uses
	mpReportFb.Language := ADR('en');
	mpReportFb.Enable := TRUE;
	
	CASE State OF
		DIV_TEST_STATE_IDLE:
			IF RunTest THEN
				DivertTestOffsets.Execute := TRUE;
				State := DIV_TEST_STATE_TEST_OFFSETS;
			END_IF
		DIV_TEST_STATE_TEST_OFFSETS:
			IF DivertTestOffsets.Done THEN
				DivertTestOffsets.Execute := 0;
				brsmemcpy(ADR(TestResults), ADR(DivertTestOffsets.Config), SIZEOF(TestResults));
				FOR i := 0 TO mlMAX_DIVERT_IDX DO
					IF i = 0 THEN
						MaxDeviation := TestResults[i].Deviation;
						MinDeviation := TestResults[i].Deviation;
					ELSE
						MaxDeviation := MAX(MaxDeviation, TestResults[i].Deviation);
						MinDeviation := MIN(MinDeviation, TestResults[i].Deviation);
					END_IF
				END_FOR
	    	    
				
				mpReportFb.Name := ADR('DiverterOffsetResults');
				mpReportFb.Generate := TRUE;
				
				State := DIV_TEST_STATE_GENERATE_REPORT;
			END_IF
		DIV_TEST_STATE_GENERATE_REPORT:
			IF mpReportFb.CommandDone THEN
				mpReportFb.Generate := FALSE;
				
				State := DIV_TEST_STATE_DONE;
			END_IF
		DIV_TEST_STATE_DONE:
			RunTest := FALSE;
		  	State := DIV_TEST_STATE_IDLE;

	END_CASE;
	
	mpReportFb();
	DivertTestOffsets();
	
END_PROGRAM
