//This file was automatically generated using the Diverter Diagnostic program. Verify that the segment names and assembly name match your project values correctly
PROGRAM _INIT
	DivertTestOffsets.ShSourceSector := ADR(gDivSector_0);
	
	DivertTestOffsets.Sectors[0] := gDivSector_0;	//SEG_D_10:TrackSegmentType.AB SegRelTo.FromStart at 0.0 connected to SEG_A_39:TrackSegmentType.AA SegRelTo.FromEnd at 0.000621 type DivReferenceType.RelToOne
	DivertTestOffsets.Sectors[1] := gDivSector_1;	//SEG_E_16:TrackSegmentType.AA SegRelTo.FromEnd at 0.0 connected to SEG_D_15:TrackSegmentType.AA SegRelTo.FromEnd at 0.104015 type DivReferenceType.RelToOne
	DivertTestOffsets.Sectors[2] := gDivSector_2;	//SEG_F_30:TrackSegmentType.AA SegRelTo.FromStart at 0.0 connected to SEG_E_24:TrackSegmentType.AA SegRelTo.FromStart at 0.0 type DivReferenceType.RelToTwo
	DivertTestOffsets.Sectors[3] := gDivSector_3;	//SEG_F_35:TrackSegmentType.BA SegRelTo.FromStart at 0.0 connected to SEG_A_35:TrackSegmentType.AA SegRelTo.FromStart at 0.0 type DivReferenceType.RelToTwo
	DivertTestOffsets.Sectors[4] := gDivSector_4;	//SEG_J_42:TrackSegmentType.AB SegRelTo.FromStart at 0.0 connected to SEG_D_13:TrackSegmentType.AA SegRelTo.FromStart at 0.254651 type DivReferenceType.RelToOne
	DivertTestOffsets.Sectors[5] := gDivSector_5;	//SEG_H_16:TrackSegmentType.AA SegRelTo.FromEnd at 0.0 connected to SEG_G_15:TrackSegmentType.AA SegRelTo.FromEnd at 0.106253 type DivReferenceType.RelToOne
	DivertTestOffsets.Sectors[6] := gDivSector_6;	//SEG_I_30:TrackSegmentType.AA SegRelTo.FromStart at 0.0 connected to SEG_H_24:TrackSegmentType.AA SegRelTo.FromStart at 0.0 type DivReferenceType.RelToTwo
	DivertTestOffsets.Sectors[7] := gDivSector_7;	//SEG_I_35:TrackSegmentType.BA SegRelTo.FromStart at 0.0 connected to SEG_A_30:TrackSegmentType.AA SegRelTo.FromStart at 0.0 type DivReferenceType.RelToTwo
	DivertTestOffsets.Sectors[8] := gDivSector_8;	//SEG_K_42:TrackSegmentType.AB SegRelTo.FromStart at 0 connected to SEG_G_13:TrackSegmentType.AA SegRelTo.FromStart at 0.25575255 type DivReferenceType.RelToOne
	DivertTestOffsets.Sectors[9] := gDivSector_9;	//SEG_I_32:TrackSegmentType.AA SegRelTo.FromStart at 0.0 connected to SEG_K_36:TrackSegmentType.BA SegRelTo.FromStart at 0.0 type DivReferenceType.RelToOne
	DivertTestOffsets.Sectors[10] := gDivSector_10;	//SEG_G_10:TrackSegmentType.AB SegRelTo.FromStart at 0.0 connected to SEG_A_34:TrackSegmentType.AA SegRelTo.FromStart at 0.0 type DivReferenceType.RelToOne
	DivertTestOffsets.Sectors[11] := gDivSector_11;	//SEG_F_32:TrackSegmentType.AA SegRelTo.FromStart at 0.0 connected to SEG_J_36:TrackSegmentType.BA SegRelTo.FromStart at 0.0 type DivReferenceType.RelToOne

	
	DivertTestOffsets.SegmentName1[0] := 'SEG_D_10';
	DivertTestOffsets.SegmentName2[0] := 'SEG_A_39';
	DivertTestOffsetsPar.Positions[0] := 0.045;
	DivertTestOffsets.SegmentName1[1] := 'SEG_E_16';
	DivertTestOffsets.SegmentName2[1] := 'SEG_D_15';
	DivertTestOffsetsPar.Positions[1] := 0.045;
	DivertTestOffsets.SegmentName1[2] := 'SEG_F_30';
	DivertTestOffsets.SegmentName2[2] := 'SEG_E_24';
	DivertTestOffsetsPar.Positions[2] := 0.045;
	DivertTestOffsets.SegmentName1[3] := 'SEG_F_35';
	DivertTestOffsets.SegmentName2[3] := 'SEG_A_35';
	DivertTestOffsetsPar.Positions[3] := 0.045;
	DivertTestOffsets.SegmentName1[4] := 'SEG_J_42';
	DivertTestOffsets.SegmentName2[4] := 'SEG_D_13';
	DivertTestOffsetsPar.Positions[4] := 0.045;
	DivertTestOffsets.SegmentName1[5] := 'SEG_H_16';
	DivertTestOffsets.SegmentName2[5] := 'SEG_G_15';
	DivertTestOffsetsPar.Positions[5] := 0.045;
	DivertTestOffsets.SegmentName1[6] := 'SEG_I_30';
	DivertTestOffsets.SegmentName2[6] := 'SEG_H_24';
	DivertTestOffsetsPar.Positions[6] := 0.045;
	DivertTestOffsets.SegmentName1[7] := 'SEG_I_35';
	DivertTestOffsets.SegmentName2[7] := 'SEG_A_30';
	DivertTestOffsetsPar.Positions[7] := 0.045;
	DivertTestOffsets.SegmentName1[8] := 'SEG_K_42';
	DivertTestOffsets.SegmentName2[8] := 'SEG_G_13';
	DivertTestOffsetsPar.Positions[8] := 0.045;
	DivertTestOffsets.SegmentName1[9] := 'SEG_I_32';
	DivertTestOffsets.SegmentName2[9] := 'SEG_K_36';
	DivertTestOffsetsPar.Positions[9] := 0.045;
	DivertTestOffsets.SegmentName1[10] := 'SEG_G_10';
	DivertTestOffsets.SegmentName2[10] := 'SEG_A_34';
	DivertTestOffsetsPar.Positions[10] := 0.045;
	DivertTestOffsets.SegmentName1[11] := 'SEG_F_32';
	DivertTestOffsets.SegmentName2[11] := 'SEG_J_36';
	DivertTestOffsetsPar.Positions[11] := 0.045;

	DivertTestOffsets.Parameters := ADR(DivertTestOffsetsPar);
	DivertTestOffsetsPar.Velocity := 1.0;
	DivertTestOffsetsPar.Acceleration := 20.0;
	DivertTestOffsetsPar.Deceleration := 20.0;
	DivertTestOffsetsPar.SettleTime := T#5s;
END_PROGRAM
