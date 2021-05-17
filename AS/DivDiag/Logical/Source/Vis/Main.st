
PROGRAM _INIT
	
	// size of Vis structure - this value has to be entered in B&R scene viewer (PVI -> Options -> Size)
	SizeofVis := SIZEOF(Vis);
	// max number of displayed shuttles  
	NumVisShuttle := SIZEOF(Vis.Shuttle) / SIZEOF(Vis.Shuttle[0]);  
	// determine if CPU is simulated
	plcSimulated := DiagCpuIsSimulated();
	
END_PROGRAM

PROGRAM _CYCLIC
	
	// Simple diagnostic tool to read shuttle user data
	IF EDGEPOS(DiagReadUserData) THEN
		brsmemcpy(ADR(DiagUserData), DiagUserDataAddress, SIZEOF(DiagUserData));
	END_IF

	FOR i := 0 TO (NumVisShuttle - 1) DO 
		IF ShuttleMon.Shuttle[i].Available THEN
			// format selected monitor data to fit B&R scene viewer  
			Vis.Shuttle[i].Available    := 1;
			Vis.Shuttle[i].PositionX    := LREAL_TO_REAL(ShuttleMon.Shuttle[i].Position.X);
			Vis.Shuttle[i].PositionY    := LREAL_TO_REAL(ShuttleMon.Shuttle[i].Position.Y);
			Vis.Shuttle[i].RotationZ    := LREAL_TO_REAL(ShuttleMon.Shuttle[i].Orientation.Angle1);
			Vis.Shuttle[i].ExtentToFront    := LREAL_TO_REAL(ShuttleMon.Shuttle[i].ExtentToFront);
			Vis.Shuttle[i].ExtentToBack        := LREAL_TO_REAL(ShuttleMon.Shuttle[i].ExtentToBack);
			Vis.Shuttle[i].Width    := LREAL_TO_REAL(ShuttleMon.Shuttle[i].Width);  
			IF NOT plcSimulated THEN
				brsitoa(ShuttleMon.Shuttle[i].Index, ADR(Vis.Shuttle[i].Text));
			END_IF
			
			Vis.Shuttle[i].ColorRed    := 0.5;    //
			Vis.Shuttle[i].ColorGreen    := 0.5;    // default shuttle color grey
			Vis.Shuttle[i].ColorBlue    := 0.5;        //
			
			IF ShuttleMon.Shuttle[i].UserData <> 0 THEN
				pUserData ACCESS ShuttleMon.Shuttle[i].UserData;
//				IF plcSimulated THEN //Overwrite the Shuttle ID from the ShuttleMon Index with the ID that is in the Userdata to assist in troubleshooting
//					brsitoa(pUserData.ShuttleID, ADR(Vis.Shuttle[i].Text));	
//				END_IF
				
                CASE pUserData.Color OF
                    
                    SHUTTLE_COLOR_GRAY:
                        
                        Vis.Shuttle[i].ColorRed := 0.5;
                        Vis.Shuttle[i].ColorGreen := 0.5;
                        Vis.Shuttle[i].ColorBlue := 0.5;
                        
                    SHUTTLE_COLOR_WHITE:
                        
                        Vis.Shuttle[i].ColorRed := 1.0;
                        Vis.Shuttle[i].ColorGreen := 1.0;
                        Vis.Shuttle[i].ColorBlue := 1.0;
                        
                    SHUTTLE_COLOR_BLACK:
                        
                        Vis.Shuttle[i].ColorRed := 0.0;
                        Vis.Shuttle[i].ColorGreen := 0.0;
                        Vis.Shuttle[i].ColorBlue := 0.0;
                    
                    SHUTTLE_COLOR_RED:
                        
    					Vis.Shuttle[i].ColorRed := 1.0;
    					Vis.Shuttle[i].ColorGreen := 0.0;
                        Vis.Shuttle[i].ColorBlue := 0.0;
                        
                    SHUTTLE_COLOR_PINK:
                        
                        Vis.Shuttle[i].ColorRed := 1.0;
                        Vis.Shuttle[i].ColorGreen := 0.25;
                        Vis.Shuttle[i].ColorBlue := 0.5;
    				
                    SHUTTLE_COLOR_GREEN:
                        
    					Vis.Shuttle[i].ColorRed := 0.0;
    					Vis.Shuttle[i].ColorGreen := 1.0;
    					Vis.Shuttle[i].ColorBlue := 0.0;
    
    			    SHUTTLE_COLOR_BLUE:
    					Vis.Shuttle[i].ColorRed := 0.0;
    					Vis.Shuttle[i].ColorGreen := 0.0;
    					Vis.Shuttle[i].ColorBlue := 1.0;
    				
    				SHUTTLE_COLOR_YELLOW:
    					Vis.Shuttle[i].ColorRed := 0.8;
    					Vis.Shuttle[i].ColorGreen := 0.8;
    					Vis.Shuttle[i].ColorBlue := 0.0;
    
    				SHUTTLE_COLOR_ORANGE:
    					Vis.Shuttle[i].ColorRed := 1.0;
    					Vis.Shuttle[i].ColorGreen := 0.5;
                        Vis.Shuttle[i].ColorBlue := 0.0;
                        
                    SHUTTLE_COLOR_PURPLE:
                        Vis.Shuttle[i].ColorRed := 0.6;
                        Vis.Shuttle[i].ColorGreen := 0.0;
                        Vis.Shuttle[i].ColorBlue := 1.0;                        
						
                    ELSE
                        
    					Vis.Shuttle[i].ColorRed := 0.5;
    					Vis.Shuttle[i].ColorGreen := 0.5;
                        Vis.Shuttle[i].ColorBlue := 0.5;
                        
                END_CASE
                
			END_IF
		ELSE
			brsmemset(ADR(Vis.Shuttle[i]), 0, SIZEOF(Vis.Shuttle[0]));
		END_IF
	END_FOR
	
	UserVis.Vis := Vis;
	
    
	 
END_PROGRAM
