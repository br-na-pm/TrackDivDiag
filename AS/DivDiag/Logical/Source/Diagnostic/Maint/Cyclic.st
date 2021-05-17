	
PROGRAM _CYCLIC
		
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
	    	    
	END_IF
	
	DivertTestOffsets();
	
END_PROGRAM
