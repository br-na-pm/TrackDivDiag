
TYPE
	UserVisTyp : 	STRUCT 
		Vis : {REDUND_UNREPLICABLE} McAcpTrakAssemblyVisData;
		Star1RotZ : REAL;
		Star2RotZ : REAL;
	END_STRUCT;
	gUserDataType : 	STRUCT  (*Shuttle User Data*)
		Color : gShuttleColorEnum; (*Shuttle color*)
	END_STRUCT;
	gShuttleColorEnum : 
		( (*Shuttle color*)
		SHUTTLE_COLOR_WHITE, (*White shuttles*)
		SHUTTLE_COLOR_BLACK, (*Black shuttles*)
		SHUTTLE_COLOR_GRAY, (*Gray shuttles*)
		SHUTTLE_COLOR_RED, (*Red shuttles*)
		SHUTTLE_COLOR_GREEN, (*Green shuttles*)
		SHUTTLE_COLOR_BLUE, (*Blue shuttles*)
		SHUTTLE_COLOR_YELLOW, (*Yellow shuttles*)
		SHUTTLE_COLOR_PINK, (*Pink shuttles*)
		SHUTTLE_COLOR_ORANGE, (*Orange shuttles*)
		SHUTTLE_COLOR_PURPLE (*Purple shuttles*)
		);
END_TYPE
