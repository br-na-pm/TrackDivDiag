
TYPE
	StateEnum : 
		( (*State of execution*)
		STATE_IDLE, (*Wait for teach command*)
		STATE_MAINTENANCE_INIT, (*Initialize maintenance*)
		STATE_CLEAR_UPSTREAM, (*Clear upstream*)
		STATE_CLEAR_DOWNSTREAM, (*Clear downstream*)
		STATE_CLEAR_ALL, (*Clear all*)
		STATE_SEND_RETURN, (*Send shuttles to the return*)
		STATE_GET_OFFSET, (*Get divert offset commanded*)
		STATE_TEST_OFFSETS, (*Test diverter offsets*)
		STATE_DONE (*Maintenance command is complete*)
		);
END_TYPE
