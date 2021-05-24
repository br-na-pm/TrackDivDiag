
TYPE
	StateEnum : 
		( (*State of execution*)
		DIV_TEST_STATE_IDLE, (*Wait for teach command*)
		DIV_TEST_STATE_TEST_OFFSETS, (*Test diverter offsets*)
		DIV_TEST_STATE_GENERATE_REPORT, (*Maintenance command is complete*)
		DIV_TEST_STATE_DONE (*Test Completed*)
		);
END_TYPE
