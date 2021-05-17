
FUNCTION_BLOCK TestOffsets

    CASE Internal.State OF
        
        TEST_OFFSETS_STATE_IDLE:
            
            IF Execute THEN
                Busy := TRUE;
                Internal.DivertIndex := FALSE;
                Internal.SecGetShuttle.Sector := ADR(ShSourceSector);
                Internal.SecGetShuttle.Mode := mcACPTRAK_SEARCH_BACKWARD;
                Internal.SecGetShuttle.Enable := TRUE;
                Internal.RoutedMoveAbs.Axis := ADR(Internal.SecGetShuttle.Axis);
                Internal.RoutedMoveAbs.Velocity := Parameters.Velocity;
                Internal.RoutedMoveAbs.Acceleration := Parameters.Acceleration;
                Internal.RoutedMoveAbs.Deceleration := Parameters.Deceleration;
                Internal.RoutedMoveAbs.AdvancedParameters.StartDirection := mcDIR_UNDEFINED;
                Internal.RoutedMoveAbs.AdvancedParameters.EndDirection := mcDIR_POSITIVE;
                Internal.RoutedMoveAbs.AdvancedParameters.ShuttleOrientation := mcDIR_UNDEFINED;
                Internal.SettleTON.PT := Parameters.SettleTime;
                Internal.State := TEST_OFFSETS_STATE_GET_SH;
            END_IF
        
        TEST_OFFSETS_STATE_GET_SH:
            
            IF NOT Execute THEN
                Internal.State := TEST_OFFSETS_STATE_RESET_FB;
            ELSIF Internal.SecGetShuttle.Error THEN
                Error := TRUE;
                ErrorID := Internal.SecGetShuttle.ErrorID;
                Internal.State := TEST_OFFSETS_STATE_RESET_FB;
            ELSIF Internal.SecGetShuttle.Valid THEN
                IF Internal.SecGetShuttle.TotalCount = 0 THEN
                    Error := TRUE;
                    ErrorID := ERR_NO_SH_ON_SEC;
                    Internal.State := TEST_OFFSETS_STATE_RESET_FB;
                ELSE
                    Internal.RoutedMoveAbs.Sector := ADR(Sectors[Internal.DivertIndex]);
                    Internal.RoutedMoveAbs.Position := Parameters.Positions[Internal.DivertIndex];
                    Internal.RoutedMoveAbs.AdvancedParameters.PosRelativeTo := Parameters.PosRelativeTo[Internal.DivertIndex];
                    Internal.RoutedMoveAbs.Execute := TRUE;
                    Internal.State := TEST_OFFSETS_STATE_SEND;
                END_IF
            END_IF
        
        TEST_OFFSETS_STATE_SEND:
            
            IF NOT Execute THEN
                Internal.State := TEST_OFFSETS_STATE_RESET_FB;
            ELSIF Internal.RoutedMoveAbs.Error THEN
                Error := TRUE;
                ErrorID := Internal.RoutedMoveAbs.ErrorID;
                Internal.State := TEST_OFFSETS_STATE_RESET_FB;
            ELSIF Internal.RoutedMoveAbs.Done THEN
                Internal.RoutedMoveAbs.Execute := FALSE;
                Internal.SettleTON.IN := TRUE;
                Internal.State := TEST_OFFSETS_STATE_SETTLE;
            END_IF
        
        TEST_OFFSETS_STATE_SETTLE:
            
            IF NOT Execute THEN
                Internal.State := TEST_OFFSETS_STATE_RESET_FB;
            ELSIF Internal.SettleTON.Q THEN
                Internal.SettleTON.IN := FALSE;
                Internal.GetSegOffsets.SegmentName1 := SegmentName1[Internal.DivertIndex];
                Internal.GetSegOffsets.SegmentName2 := SegmentName2[Internal.DivertIndex];
                Internal.GetSegOffsets.Execute:= TRUE;
                Internal.State := TEST_OFFSETS_STATE_GET_SEG;
            END_IF
        
        TEST_OFFSETS_STATE_GET_SEG:
            
            IF NOT Execute THEN
                Internal.State := TEST_OFFSETS_STATE_RESET_FB;
            ELSIF Internal.GetSegOffsets.Error THEN
                Error := TRUE;
                ErrorID := Internal.GetSegOffsets.ErrorID;
                Internal.State := TEST_OFFSETS_STATE_RESET_FB;
            ELSIF Internal.GetSegOffsets.Done THEN
                Internal.GetSegOffsets.Execute := FALSE;
                brsmemcpy(ADR(Config[Internal.DivertIndex]), ADR(Internal.GetSegOffsets.Config), SIZEOF(Config[Internal.DivertIndex]));
                IF Internal.DivertIndex < mlMAX_DIVERT_IDX THEN
                    Internal.DivertIndex := Internal.DivertIndex + TRUE;
                    Internal.RoutedMoveAbs.Sector := ADR(Sectors[Internal.DivertIndex]);
                    Internal.RoutedMoveAbs.Position := Parameters.Positions[Internal.DivertIndex];
                    Internal.RoutedMoveAbs.AdvancedParameters.PosRelativeTo := Parameters.PosRelativeTo[Internal.DivertIndex];
                    Internal.RoutedMoveAbs.Execute := TRUE;
                    Internal.State := TEST_OFFSETS_STATE_SEND;
                ELSE
                    Internal.SecGetShuttle.Enable := FALSE;
                    Done := TRUE;
                    Internal.State := TEST_OFFSETS_STATE_DONE;
                END_IF
            END_IF
        
        TEST_OFFSETS_STATE_DONE:
            
            IF NOT Execute THEN
                Done := FALSE;
                brsmemset(ADR(Config), 0, SIZEOF(Config));
                Internal.State := TEST_OFFSETS_STATE_WAIT_NOT_BUSY;
            END_IF
        
        TEST_OFFSETS_STATE_RESET_FB:
            
            Internal.SecGetShuttle.Enable := FALSE;
            Internal.RoutedMoveAbs.Execute := FALSE;
            Internal.GetSegOffsets.Execute := FALSE;
            Internal.SettleTON.IN := FALSE;
            IF Error THEN
                Internal.State := TEST_OFFSETS_STATE_ERROR;
            ELSE
                Internal.State := TEST_OFFSETS_STATE_WAIT_NOT_BUSY;
            END_IF
        
        TEST_OFFSETS_STATE_WAIT_NOT_BUSY:
            
            IF NOT (Internal.SecGetShuttle.Busy OR Internal.RoutedMoveAbs.Busy OR Internal.GetSegOffsets.Busy) THEN
                Busy := FALSE;
                Internal.State := TEST_OFFSETS_STATE_IDLE;
            END_IF
        
        TEST_OFFSETS_STATE_ERROR:
        
            IF NOT Execute THEN
                Error := FALSE;
                ErrorID := ERR_OK;
                Internal.State := TEST_OFFSETS_STATE_WAIT_NOT_BUSY;
            END_IF
        
    END_CASE
    
    Internal.SecGetShuttle();
    Internal.RoutedMoveAbs();
    Internal.GetSegOffsets();
    Internal.SettleTON();
    
END_FUNCTION_BLOCK
