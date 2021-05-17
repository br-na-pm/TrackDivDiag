
FUNCTION_BLOCK GetSegType

    IF Execute THEN
        CASE ProductCode OF
            16#EBFE:
                Type	:= 'PT1 8YFIZ1.AA63.00-1';
                Length	:= 0.630;
                Valid := 1;
            16#EE0A:	
                Type	:= 'PT1 8YFIZ1.AA63.10-1';
                Length	:= 0.630;
                Valid := 1;
            16#EC00:	
                Type	:= 'PT1 8YFIZ1.AB43.00-1';
                Length	:= 0.435642;
                Valid := 1;
            16#EE0B:	
                Type	:= 'PT1 8YFIZ1.AB43.10-1';
                Length	:= 0.435642;
                Valid := 1;
            16#EC01:	
                Type	:= 'PT1 8YFIZ1.BA43.00-1';
                Length	:= 0.435642;
                Valid := 1;
            16#EE0C:	
                Type	:= 'PT1 8YFIZ1.BA43.10-1';
                Length	:= 0.435642;
                Valid := 1;
            16#F255:	
                Type	:= 'PT2 8YF1I01.AA66.00-1';
                Length	:= 0.660;
                Valid := 1;
            16#F256:	
                Type	:= 'PT2 8YF1I01.AB2B.00-1';
                Length	:= 0.450585;
                Valid := 1;
            16#F257:	
                Type	:= 'PT2 8YF1I01.BA2B.00-1';
                Length	:= 0.450585;
                Valid := 1;
            16#F7C3:	
                Type	:= '8F1I01.AA66.0000-1';
                Length	:= 0.660;
                Valid := 1;
            16#F7CA:	
                Type	:= '8F1I01.BB4B.0000-1 invalid for diverter!';
                Length	:= 0.240;
                Error := 1;
                ErrorID := ERR_INVALID_SEG_TYPE;
            16#F7CB:	
                Type	:= '8F1I01.AB2B.0000-1';
                Length	:= 0.450585;
                Valid := 1;
            16#F7CC:	
                Type	:= '8F1I01.BA2B.0000-1';
                Length	:= 0.450585;
                Valid := 1;
            ELSE		
                Type	:= 'unknown';
                Length	:= 0.0;
                Error := 1;
                ErrorID := ERR_INVALID_SEG_TYPE;
        END_CASE
    ELSE
        Error := 0;
        ErrorID := ERR_OK;
        Valid := 0;
        Type := '';
        Length := 0.0;
    END_IF
    
END_FUNCTION_BLOCK
