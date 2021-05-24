
(* Get segment offset data *)
FUNCTION_BLOCK GetSegmentOffsets
    
    CASE Internal.State OF
        
        GET_OFFSET_STATE_IDLE:
            
            IF Execute THEN
                Busy := 1;
                Internal.ParId1[0].ParID := mcACPPAR_EPROM_PRODUCT_CODE;
                Internal.ParId1[0].DataType := mcACPTRAK_SEG_PARTYPE_UDINT;
                Internal.ParId1[0].VariableAddress := ADR(Internal.ProductCode1);
                Internal.ParId1[1].ParID := mcACPPAR_ENCOD0_POS_ACT;
                Internal.ParId1[1].DataType := mcACPTRAK_SEG_PARTYPE_DINT;
                Internal.ParId1[1].VariableAddress := ADR(Internal.PosAct1);
                Internal.ParId1[2].ParID := mcACPPAR_PCTRL_LAG_ERROR;
                Internal.ParId1[2].DataType := mcACPTRAK_SEG_PARTYPE_REAL;
                Internal.ParId1[2].VariableAddress := ADR(Internal.LagError1);
                Internal.ParId2[0].ParID := mcACPPAR_EPROM_PRODUCT_CODE;
                Internal.ParId2[0].DataType := mcACPTRAK_SEG_PARTYPE_UDINT;
                Internal.ParId2[0].VariableAddress := ADR(Internal.ProductCode2);
                Internal.ParId2[1].ParID := mcACPPAR_ENCOD0_POS_ACT;
                Internal.ParId2[1].DataType := mcACPTRAK_SEG_PARTYPE_DINT;
                Internal.ParId2[1].VariableAddress := ADR(Internal.PosAct2);
                Internal.ParId2[2].ParID := mcACPPAR_PCTRL_LAG_ERROR;
                Internal.ParId2[2].DataType := mcACPTRAK_SEG_PARTYPE_REAL;
                Internal.ParId2[2].VariableAddress := ADR(Internal.LagError2);
                Internal.SegProcessParID1.DataAddress := ADR(Internal.ParId1);
                Internal.SegProcessParID1.NumberOfParIDs := 3;
                Internal.SegProcessParID1.Mode := mcACPTRAK_SEG_PARID_GET;
                Internal.SegProcessParID1.ChannelIndex := 0;
                Internal.SegProcessParID2.DataAddress := ADR(Internal.ParId2);
                Internal.SegProcessParID2.NumberOfParIDs := 3;
                Internal.SegProcessParID2.Mode := mcACPTRAK_SEG_PARID_GET;
                Internal.SegProcessParID2.ChannelIndex := 0;
                Internal.Status1 := PV_xgetadr(ADR(SegmentName1), ADR(Internal.Seg1Ref), ADR(Internal.Seg1Len));
                Internal.Status2 := PV_xgetadr(ADR(SegmentName2), ADR(Internal.Seg2Ref), ADR(Internal.Seg2Len));
                
				IF DiagCpuIsARsim() OR DiagCpuIsSimulated () THEN
					Done := TRUE;
					Internal.State := GET_OFFSET_STATE_DONE;
				ELSE
					Internal.State := GET_OFFSET_STATE_GET_SEG;
				END_IF
            END_IF
            
        GET_OFFSET_STATE_GET_SEG:
            
            IF Internal.Status1 <> ERR_OK THEN
                Error := 1;
                ErrorID := Internal.Status1;
                Internal.State := GET_OFFSET_STATE_RESET_FB;
            ELSIF Internal.Status2 <> ERR_OK THEN
                Error := 1;
                ErrorID := Internal.Status2;
                Internal.State := GET_OFFSET_STATE_RESET_FB;
            ELSE
                Internal.SegProcessParID1.Segment := Internal.Seg1Ref;
                Internal.SegProcessParID2.Segment := Internal.Seg2Ref;
                Internal.SegProcessParID1.Execute := 1;
                Internal.SegProcessParID2.Execute := 1;
                Internal.State := GET_OFFSET_STATE_GET_VALUES;
            END_IF
        
        GET_OFFSET_STATE_GET_VALUES:
            
            IF Internal.SegProcessParID1.Error THEN
                Error := 1;
                ErrorID := Internal.SegProcessParID1.ErrorID;
                Internal.State := GET_OFFSET_STATE_RESET_FB;
            ELSIF Internal.SegProcessParID2.Error THEN
                Error := 1;
                ErrorID := Internal.SegProcessParID2.ErrorID;
                Internal.State := GET_OFFSET_STATE_RESET_FB;
            ELSIF Internal.SegProcessParID1.Done AND Internal.SegProcessParID2.Done THEN
                Internal.SegProcessParID1.Execute := 0;
                Internal.SegProcessParID2.Execute := 0;
                Internal.Position1 := DINT_TO_REAL(Internal.PosAct1)/10000000.0;
                Internal.Position2 := DINT_TO_REAL(Internal.PosAct2)/10000000.0;
                Internal.SegType1.ProductCode := Internal.ProductCode1;
                Internal.SegType1.Execute := 1;
                Internal.SegType2.ProductCode := Internal.ProductCode2;
                Internal.SegType2.Execute := 1;
                Internal.State := GET_OFFSET_STATE_GET_TYPE;
            END_IF
            
        GET_OFFSET_STATE_GET_TYPE:
            
            IF Internal.SegType1.Error THEN
                Error := 1;
                ErrorID := Internal.SegType1.ErrorID;
                Internal.State := GET_OFFSET_STATE_RESET_FB;
            ELSIF Internal.SegType2.Error THEN
                Error := 1;
                ErrorID := Internal.SegType2.ErrorID;
                Internal.State := GET_OFFSET_STATE_RESET_FB;
            ELSIF Internal.SegType1.Valid AND Internal.SegType2.Valid THEN
                Internal.SegType1.Execute := 0;
                Internal.SegType2.Execute := 0;
                // calculate track-connection point at the pos/neg end of track segment 2
                IF(Internal.Position2 <= (Internal.SegType2.Length/2.0))THEN
                    Config.Seg2PosRelToStart	:= 0.0;
                    Config.Seg2PosRelToEnd	    := Internal.SegType2.Length;
                    Config.Seg1PosRelToStart	:= Internal.Position1 + Internal.Position2;
                ELSE
                    Config.Seg2PosRelToStart	:= Internal.SegType2.Length;
                    Config.Seg2PosRelToEnd	    := 0.0;
                    Config.Seg1PosRelToStart	:= Internal.Position1 - (Internal.SegType2.Length - Internal.Position2);
                END_IF
                Config.Seg1PosRelToEnd		    := Internal.SegType1.Length - Config.Seg1PosRelToStart;
                Config.Deviation	            := Internal.LagError1 + Internal.LagError2;
			
                // shift track-connection point if it is outside the existing track segment
                IF(Config.Seg1PosRelToStart < 0.0)THEN
                    Config.Seg2PosRelToStart	:= Config.Seg2PosRelToStart	+ Config.Seg1PosRelToStart;
                    Config.Seg2PosRelToEnd	    := Config.Seg2PosRelToEnd	- Config.Seg1PosRelToStart;
                    Config.Seg1PosRelToStart	:= 0.0;
                    Config.Seg1PosRelToEnd	    := Internal.SegType1.Length;
                END_IF
                IF(Config.Seg1PosRelToEnd < 0.0)THEN
                    Config.Seg2PosRelToStart	:= Config.Seg2PosRelToStart	- Config.Seg1PosRelToEnd;
                    Config.Seg2PosRelToEnd	    := Config.Seg2PosRelToEnd	+ Config.Seg1PosRelToEnd;
                    Config.Seg1PosRelToStart	:= Internal.SegType1.Length;
                    Config.Seg1PosRelToEnd	    := 0.0;
                END_IF
			
                // check for result valid
                IF(	(Internal.SegType1.Length > 0.0) AND
                    (Internal.Position1 <> 0.0) AND
                    (Config.Seg1PosRelToStart >= 0.0) AND
                    (Config.Seg1PosRelToStart <= Internal.SegType1.Length) AND
                    (Config.Seg1PosRelToEnd >= 0.0) AND
                    (Config.Seg1PosRelToEnd <= Internal.SegType1.Length) AND
                    (Internal.SegType2.Length > 0.0) AND
                    (Internal.Position2 <> 0.0) AND
                    (Config.Seg2PosRelToStart >= 0.0) AND
                    (Config.Seg2PosRelToStart <= Internal.SegType2.Length) AND
                    (Config.Seg2PosRelToEnd >= 0.0) AND
                    (Config.Seg2PosRelToEnd <= Internal.SegType2.Length) )THEN
                    brsstrcpy(ADR(Config.Seg1Name), ADR(SegmentName1));
                    brsstrcpy(ADR(Config.Seg2Name), ADR(SegmentName2));
                    brsstrcpy(ADR(Config.Seg1Type), ADR(Internal.SegType1.Type));
                    brsstrcpy(ADR(Config.Seg2Type), ADR(Internal.SegType2.Type));
                    Done := 1;
                    Internal.State := GET_OFFSET_STATE_DONE;
                ELSE
                    Error := 1;
                    ErrorID := ERR_INVALID_CONFIG;
                    Internal.State := GET_OFFSET_STATE_RESET_FB;
                END_IF
            END_IF
        
        GET_OFFSET_STATE_DONE:
            
            IF NOT Execute THEN
                Done := 0;
                brsmemset(ADR(Config), 0, SIZEOF(Config));
                Internal.State := GET_OFFSET_STATE_WAIT_NOT_BUSY;
            END_IF
            
        GET_OFFSET_STATE_RESET_FB:
            
            Internal.SegProcessParID1.Execute := 0;
            Internal.SegProcessParID2.Execute := 0;
            Internal.SegType1.Execute := 0;
            Internal.SegType2.Execute := 0;
            IF Error THEN
                Internal.State := GET_OFFSET_STATE_ERROR;
            ELSE
                Internal.State := GET_OFFSET_STATE_WAIT_NOT_BUSY;
            END_IF
        
        GET_OFFSET_STATE_WAIT_NOT_BUSY:
            
            IF NOT (Internal.SegProcessParID1.Busy OR Internal.SegProcessParID2.Busy) THEN
                Busy := 0;
                Internal.State := GET_OFFSET_STATE_IDLE;
            END_IF
        
        GET_OFFSET_STATE_ERROR:
        
            IF NOT Execute THEN
                Error := 0;
                ErrorID := ERR_OK;
                Internal.State := GET_OFFSET_STATE_WAIT_NOT_BUSY;
            END_IF
        
    END_CASE
    
    Internal.SegProcessParID1();
    Internal.SegProcessParID2();
    Internal.SegType1();
    Internal.SegType2();
    
END_FUNCTION_BLOCK
