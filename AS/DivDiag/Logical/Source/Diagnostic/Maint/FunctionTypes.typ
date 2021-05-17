(*Get Segment Offsets*)

TYPE
	GetSegmentOffsetsConfigType : 	STRUCT  (*Configuration result*)
		Seg1Name : STRING[32]; (*Segment 1 name*)
		Seg2Name : STRING[32]; (*Segment 2 name*)
		Seg1Type : STRING[80]; (*track segment 1 type*)
		Seg2Type : STRING[80]; (*segment 2 type*)
		Deviation : REAL; (*result CmdCheckConfigDeviation:
measured deviation of diverter segment mounting to assembly-track-configuration [m]*)
		Seg1PosRelToStart : REAL; (*result CmdCheckConfigDeviation: 
suggested value to enter in assembly-track-configuration for  track segment 1 "Position" if "Position relative to = Start of segment" [m]*)
		Seg1PosRelToEnd : REAL; (*result CmdCheckConfigDeviation: 
suggested value to enter in assembly-track-configuration for track segment 1 "Position" if "Position relative to = End of segment" [m]*)
		Seg2PosRelToStart : REAL; (*result CmdCheckConfigDeviation:
suggested value to enter in assembly-track-configuration for track segment 2 "Position" if "Position relative to = Start of segment" [m]*)
		Seg2PosRelToEnd : REAL; (*result CmdCheckConfigDeviation:
suggested value to enter in assembly-track-configuration for  track segment 2 "Position" if "Position relative to = End of segment" [m]*)
	END_STRUCT;
	GetSegmentOffsetsInternalType : 	STRUCT  (*Internal Data*)
		State : GetSegmentOffsetsStateEnum; (*State of execution*)
		Status1 : DINT; (*Return status 1*)
		Status2 : DINT; (*Return status 2*)
		Seg1Ref : UDINT; (*Segment 1 reference*)
		Seg1Len : UDINT; (*Segment 1 data length*)
		Seg2Ref : UDINT; (*Segment 2 reference*)
		Seg2Len : UDINT; (*Segment 2 data length*)
		ProductCode1 : UDINT; (*Segment 1 read product code*)
		ProductCode2 : UDINT; (*Segment 2 read product code*)
		PosAct1 : DINT; (*Segment 1 read actual position*)
		PosAct2 : DINT; (*Segment 2 read actual position*)
		Position1 : REAL; (*Position on the segment*)
		Position2 : REAL; (*Position on the segment*)
		LagError1 : REAL; (*Segment 1 read lag error*)
		LagError2 : REAL; (*Segment 2 read lag error*)
		SegProcessParID1 : MC_BR_SegProcessParID_AcpTrak; (*Process segment 1 parameters*)
		ParId1 : ARRAY[0..2]OF McAcpTrakSegProcessParIDType; (*Segment 1 parameters*)
		SegProcessParID2 : MC_BR_SegProcessParID_AcpTrak; (*Process segment 2 parameters*)
		ParId2 : ARRAY[0..2]OF McAcpTrakSegProcessParIDType; (*Segment 2 parameters*)
		SegType1 : GetSegType; (*Get segment 1 type*)
		SegType2 : GetSegType; (*Get segment 2 type*)
	END_STRUCT;
	GetSegmentOffsetsStateEnum : 
		( (*State of execution*)
		GET_OFFSET_STATE_IDLE, (*Idle state*)
		GET_OFFSET_STATE_GET_SEG, (*Get segment addresses from PV names*)
		GET_OFFSET_STATE_GET_VALUES, (*Get values from segments*)
		GET_OFFSET_STATE_GET_TYPE, (*Get segment type*)
		GET_OFFSET_STATE_DONE, (*Offsets found*)
		GET_OFFSET_STATE_RESET_FB, (*Reset function blocks*)
		GET_OFFSET_STATE_WAIT_NOT_BUSY, (*Wait for function blocks to report not busy*)
		GET_OFFSET_STATE_ERROR (*An error occurred*)
		);
END_TYPE

(*Send To Return*)

TYPE
	SendToReturnParType : 	STRUCT  (*Parameters*)
		SendDelay : TIME; (*Time to wait between sending shuttles*)
		CheckInterval : TIME; (*Time to wait between checking for completion*)
		PosRelativeTo : McAcpTrakRoutePosRelToEnum; (*Whether the position is relative to the start or end of the sector*)
		Position : LREAL; (*Position to send shuttles to*)
		Velocity : REAL; (*Move velocity*)
		Acceleration : REAL; (*Move acceleration*)
		Deceleration : REAL; (*Move deceleration*)
	END_STRUCT;
	SendToReturnInternalType : 	STRUCT  (*Internal Data*)
		State : SendToReturnStateEnum; (*State of execution*)
		AsmGetShuttle : MC_BR_AsmGetShuttle_AcpTrak; (*Get shuttles on the assembly*)
		RoutedMoveAbs : MC_BR_RoutedMoveAbs_AcpTrak; (*Send shuttles with a routed move absolute*)
		ShReadInfo : MC_BR_ShReadInfo_AcpTrak; (*Read shuttle information*)
		DelayTON : TON; (*Delay sending the next shuttle*)
		CheckTON : TON; (*Wait to check for completion*)
		OldRemainingCount : UDINT; (*Previously recorded value of the remaining count*)
	END_STRUCT;
	SendToReturnStateEnum : 
		( (*State of execution*)
		SEND_RETURN_STATE_IDLE, (*Idle state*)
		SEND_RETURN_STATE_GET_SH_SEND, (*Get shuttles for sending*)
		SEND_RETURN_STATE_SEND_SH, (*Send shuttle*)
		SEND_RETURN_STATE_DELAY, (*Delay sending the next shuttle*)
		SEND_RETURN_STATE_NEXT_SH_SEND, (*Get next shuttle for sending*)
		SEND_RETURN_STATE_WAIT_CHECK, (*Wait to check for shuttle move done*)
		SEND_RETURN_STATE_GET_SH_CHECK, (*Get shuttles for checking for completion*)
		SEND_RETURN_STATE_SH_INFO, (*Check if shuttle is stopped*)
		SEND_RETURN_STATE_NEXT_SH_CHECK, (*Get the next shuttle to check*)
		SEND_RETURN_STATE_DONE, (*All shuttles are on the return*)
		SEND_RETURN_STATE_RESET_FB, (*Reset function blocks*)
		SEND_RETURN_STATE_WAIT_NOT_BUSY, (*Wait for function blocks to report not busy*)
		SEND_RETURN_STATE_ERROR (*An error occurred*)
		);
END_TYPE

(*Test Offsets*)

TYPE
	TestOffsetsParType : 	STRUCT  (*Parameters*)
		Positions : ARRAY[0..mlMAX_DIVERT_IDX]OF LREAL; (*Positions on each divert sector*)
		PosRelativeTo : ARRAY[0..mlMAX_DIVERT_IDX]OF McAcpTrakRoutePosRelToEnum; (*Whether the position is relative to the start or end of the sector*)
		Velocity : REAL; (*Move velocity*)
		Acceleration : REAL; (*Move acceleration*)
		Deceleration : REAL; (*Move deceleration*)
		SettleTime : TIME; (*Time to wait before measuring position*)
	END_STRUCT;
	TestOffsetsInternalType : 	STRUCT  (*Internal Data*)
		State : TestOffsetsStateEnum; (*State of execution*)
		SecGetShuttle : MC_BR_SecGetShuttle_AcpTrak; (*Get shuttle for test*)
		RoutedMoveAbs : MC_BR_RoutedMoveAbs_AcpTrak; (*Send shuttle*)
		GetSegOffsets : GetSegmentOffsets; (*Get segment offsets*)
		SettleTON : TON; (*Timer*)
		DivertIndex : USINT; (*Current Divert index*)
	END_STRUCT;
	TestOffsetsStateEnum : 
		( (*State of execution*)
		TEST_OFFSETS_STATE_IDLE, (*Idle state*)
		TEST_OFFSETS_STATE_GET_SH, (*Get shuttle*)
		TEST_OFFSETS_STATE_SEND, (*Send shuttle*)
		TEST_OFFSETS_STATE_SETTLE, (*Wait for settling*)
		TEST_OFFSETS_STATE_GET_SEG, (*Get segments*)
		TEST_OFFSETS_STATE_DONE, (*Testing complete*)
		TEST_OFFSETS_STATE_RESET_FB, (*Reset function blocks*)
		TEST_OFFSETS_STATE_WAIT_NOT_BUSY, (*Wait for function blocks to report not busy*)
		TEST_OFFSETS_STATE_ERROR (*An error occurred*)
		);
END_TYPE
