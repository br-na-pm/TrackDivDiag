
FUNCTION_BLOCK GetSegmentOffsets (*Get segment offsets*)
	VAR_INPUT
		SegmentName1 : STRING[32]; (*Name of the first divert segment*)
		SegmentName2 : STRING[32]; (*Name of the second divert segment*)
		Execute : BOOL; (*Get offsets of the selected segments*)
	END_VAR
	VAR_OUTPUT
		Busy : BOOL; (*The function block is busy and must continue to be called*)
		Done : BOOL; (*The data has been captured*)
		Config : GetSegmentOffsetsConfigType; (*Suggested configuration*)
		Error : BOOL; (*An error occurred*)
		ErrorID : DINT; (*ID of the error that occurred*)
	END_VAR
	VAR
		Internal : GetSegmentOffsetsInternalType; (*Internal Data*)
	END_VAR
END_FUNCTION_BLOCK

FUNCTION_BLOCK TestOffsets (*Test Segment offsets*)
	VAR_INPUT
		ShSourceSector : REFERENCE TO McSectorType; (*Shuttle to pull from for test*)
		Parameters : REFERENCE TO TestOffsetsParType; (*Parameters*)
		SegmentName1 : ARRAY[0..mlMAX_DIVERT_IDX] OF STRING[32]; (*Name of the first divert segment*)
		SegmentName2 : ARRAY[0..mlMAX_DIVERT_IDX] OF STRING[32]; (*Name of the second divert segment*)
		Sectors : ARRAY[0..mlMAX_DIVERT_IDX] OF McSectorType; (*Sectors to use for sending to the divert*)
		Execute : BOOL; (*Test offsets*)
	END_VAR
	VAR_OUTPUT
		Busy : BOOL; (*The function block is busy and must continue to be called*)
		Done : BOOL; (*The data has been captured*)
		Config : ARRAY[0..mlMAX_DIVERT_IDX] OF GetSegmentOffsetsConfigType; (*Test results*)
		Error : BOOL; (*An error occurred*)
		ErrorID : DINT; (*ID of the error that occurred*)
	END_VAR
	VAR
		Internal : TestOffsetsInternalType; (*Internal Data*)
	END_VAR
END_FUNCTION_BLOCK

FUNCTION_BLOCK GetSegType (*Return data about the segment type*)
	VAR_INPUT
		ProductCode : UDINT; (*Segment product code*)
		Execute : BOOL; (*Return segment data*)
	END_VAR
	VAR_OUTPUT
		Valid : BOOL; (*If true, the output is valid*)
		Error : BOOL; (*An error occurred*)
		ErrorID : DINT; (*ID of the error that occurred*)
		Type : STRING[80]; (*Segment type*)
		Length : REAL; (*Segment length*)
	END_VAR
END_FUNCTION_BLOCK
