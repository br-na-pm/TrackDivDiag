# Diverter Diagnostic Test Tool

With Acopos Trak diverting applications, upon commissioning and assembly it is a requirement to validate the "virtual" defined diverter offsets in the assembly configuration file with the "physical" real world actual offsets. This validation is important to ensure proper alignment and proper functionality for an Acopos Trak application. 

Generally, users must manually move shuttles to each divert zone, preform a position reading on the two segments and calculate the differences to know the physical real world offset. These values must then be compared to those inside the assembly configuration file and updated where needed.

With this Diverter Diagnostic Test Tool, this process is simplified. The tool takes an existing AcoposTrak layout and with minimal user input generates a test program that will allow for an automated testing process. The process includes:

- Parsing an assembly file to determine all known diverts
- Generating a test routine for a shuttle to be commanded to move through each divert automatically
- Test in each divert is run to automatically pull the positions and calculate the correct diverter offsets
- Automatically generated pdf report with the results of the test for evaluation and documentation

This test can be run on a command whenever it is required to re-validate the mechanical alignment of diverts on an AcoposTrak layout.

## Requirements:

- Diverter Diagnostic Test Technology Solution
- Singular shuttle on the trak
- No physical obstructions for a shuttle to move through the entire trak layout



## Using the Import Tool:

The first step in using the tool is to navigate to File -> Import Project. From there you can navigate to the root folder of your project you would like to import.

![image-20210526073650989](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210526073650989.png)

Once selected, a popup will appear asking you to specify the configuration you'd like to import. 

![image-20210526073717957](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210526073717957.png)

Once your configuration is selected, the tool will parse the AcpTrak assembly file for diverts and import them into the tool. The tool will scan in both the "Relative to One" and "Relative to Two" divert references types. The information will be parsed and then displayed in the tool table.

![image-20210526073750470](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210526073750470.png)

### "Base" vs "Spur" segments:

![img](file:///C:/Users/trostelc/AppData/Local/Temp/SNAGHTML3368e3.PNG)

The base and spur terminology can be correlated back the Automation Studio assembly file. The "Spur" segment, is the segment of the trak the reference is attached to. The "base" segment is the segment of existing already defined trak that you'd like to reference against. In the above example, the Base Segment A_39 was defined in trak 1 with a absolute position and the D_10 segment is being given a position relative to that. So Seg_A_39 is the base and Seg_D_10 is the spur.

The rest of the table can be used to validate the import from your assembly file. This information will be used to generate sectors automatically that are used for the test application. The only two columns that are editable are the "Divert Ref Segment" and the "Relative To". For more information on those columns reference the "Sectors Export Section"

*Note - the base vs spur for Implicit and "Relative to Two" diverts is chosen arbitrarily. It is possible the divert sector is created on the wrong end of a segment and therefore these values can be freely changed to correct the problem*

### "Relative To One" vs "Relative to Two" vs "Implicit" 

There are 3 different type of diverts in Acp Trak system. The names used to describe them refer to how the divert is established in the configuration. The first two, Relative to One and Relative to Two directly correlate directly to the trak assembly configuration position reference values. These diverts are explicitly defined by the user inside the trak assembly configuration. The user has direct control over the offsets that are used.

 The third, implicit, is used to describe diverts that are created due to the existing geometry defined in the layout. These definitions do not exist inside the trak assembly configuration and are created "implicitly" by the system. With these diverts, the user has no direct influence on setting the divert offset. The offsets are determined as a byproduct of the definition of the rest of the system. However, it is important to validate that the physical offset matches what the automatically calculated virtual offset.  More on that in the "Evaluating the Report" section.

### Adding "Implicit Diverts":

To add implicit diverts, navigate to the Edit -> Add Implicit Divert

![image-20210526081712518](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210526081712518.png)

A popup dialog will appear where you can select two segments to add to the system as a divert. The list of segments contains only possible divertible segments (Ie - AA, AB and BA segments) that exist currently in the project.

![image-20210526081942144](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210526081942144.png)

After selecting the two segments and pressing "add" the segments will appear in the table.

### Divert Ref Segment and Relative To Columns

![image-20210609080005346](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210609080005346.png)

These two columns on the table are the only two editable columns in the table. This data is used to automatically create the sector on the divert to send the shuttles to. The tool attempts to figure guess at the most likely segment to use as a refence and the best starting location (for example, if a divert has a BA segment and an AA segment, it makes sense to use the BA segment from the end as that's the only valid location on the BA segment to preform the divert)

![image-20210609075943211](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210609075943211.png)

These two columns represent this data. If there is a need, the reference segment and Relative to column can be changed for a divert. 

## Adding and Using the Diverter Test Task

The Divert Offset test is contained in a technology solution that you need to add to your project. The test itself lives inside the Maint Task under the Diagnostic package in the logical view. The test specifically takes a singular shuttle and routes it to a list of sectors

## Steps for usage:

- Start with a Automation Studio Project with a working AcoposTrak layout
- Add the Diverter Diagnostic Test Technology Solution
- If not already added, add MpServices to project
- Open the Diverter Diagnostic Test Tool Importer program
- Select the root directory of your project
- Select the configuration you would like to work from
- Verify that all Relative to Two diverts are defined correctly (see additional documentation for details)
- Add any "Implicit Diverts" to the tool
- Export the files to the project using the built in export tool
- Verify the export data inside the Automation Studio project
- Verify "Shuttle Start Sector" is correct
- Create a "Report" file device for MpReport (or change the FileDevice in the Maint cyclic task) if not created already
- Compile and Transfer to system
- Verify shuttle in "Shuttle Start Sector"
- Ensure no physical obstructions for a shuttle to navigate to all diverts on the system
- Power on AcpTrak assembly
- Set "RunTest" value to true
- Upon completion, a PDF report will be generated, validate the results

## Evaluating The Report

*Note - The test run in simulation will not actually record any positions. Don't be alarmed if in simulation the report appears to have missing data.*

For each divert, a position measurement is taken. This measurement is used to calculate the relative offset from the two segments. Additionally the lag error between the two segments is used to determine the deviation from the virtual definition to the real world measurement.

![image-20210601090457202](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210601090457202.png)

All measurement values are in meters to match the assembly

For each segment in the divert, two measurements exist for convenience, a "Relative to start of segment" and "Relative to end of segment" these are the same value just relative to the side of the segment as suggested in the title. The information means the exact same just is a variance in how the relationship is defined.

The final piece of information for each divert is the Measured Configuration Mismatch. This is in reference to the error in the virtual offset defined via the assembly and the real world offsets that exist between the two segments. Values above 1-2mm are of concern generally speaking. You should aim to have this value below 1mm ideally. The calculation of the measured configuration mismatch is the addition of the two lag errors of the segments. 

#### Implicit offset evaluation.

For implicit diverts, there of course is no configuration value in the assembly file for the offset. However, the MpMotion system still calculates where it thinks the divert should be based upon the geometry of the rest of the layout. It is therefore useful to evaluate this virtual expected offset and the actual real offset. With the implicit diverts one must look at the rest of the trak system to understand where the error is.

##### Consider the following track layout:

![img](file:///C:/Users/trostelc/AppData/Local/Temp/SNAGHTML234e3ce1.PNG)

| Divert          | Spur | Base | Type     |
| --------------- | ---- | ---- | -------- |
| 1 (A_3 and B_1) | B_1  | A_3  | Explicit |
| 2 (B_3 and C_9) | C_9  | B_3  | Explicit |
| 3 (C_1 and D_1) | D_1  | C_1  | Explicit |
| 4 (D_3 and A_1) | A_1  | D_3  | Implicit |

In this example, there are 3 explicit diverts and 1 implicit divert. The implicit diverts virtual and actual offsets are determined by the relative position of the rest of the preceding trak.

Lets imagine that the offset test is completed and the report comes back saying that divert 1 has an measured configured mismatch of 0.004 m. This would mean that segment B_1 is located 4mm to the right of where it's expected to be. Additionally, divert 4 reports back that it also has a configured mismatch of 0.004m

![img](file:///C:/Users/trostelc/AppData/Local/Temp/SNAGHTML23585b55.PNG)

The solution here is simple, the error in divert 4 is likely caused by the error in the explicit definition of divert 1. Fixing the defined virtual offset for divert 1 will fix the mismatch for both diverts.

A separate scenario is more likely to occur however in which the two offsets are not exactly equal. In the above example perhaps the divert 4 offset reports back as 2mm instead of 4. This means that 2 mm of alignment error exists in the mechanical assembly itself. The only solution for this is to validate the mechanical alignment and orientation of the physical segment chain from Seg_B_1 to Seg_D_3.

### Diverter Offsets Graph

The final section of the report gives an overview of all the offset mismatches for all diverts configured in the test. This can be used to get a quick overview of all of the diverts on the system and their configured measurement error.

![image-20210608090815554](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210608090815554.png)
