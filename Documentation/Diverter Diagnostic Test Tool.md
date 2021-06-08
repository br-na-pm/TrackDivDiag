# Diverter Diagnostic Test Tool

With Acopos Trak diverting applications, upon commissioning and assembly it is a requirement to validate the "virtual" defined diverter offsets in the assembly configuration file with the "physical" real world actual offsets. This validation is important to ensure proper alignment and ensure the proper functionality on the machine. 

Generally, users must manually move shuttles to each divert zone, preform a position reading on the two segments and calculate the differences to know the physical real world offset. These values must then be compared to those inside the assembly configuration file and updated where needed.

With this Diverter Diagnostic Test Tool, this process is simplified. The tool takes an existing ACPTrak layout and with minimal user input generates a test program that will allow for an automated testing process. The process includes:

- Parsing an assembly file to determine all known diverts
- Generating a test routine for a shuttle to be commanded to move through each divert automatically
- Test in each divert is run to automatically pull the positions and calculate the correct diverter offsets
- Automatically generated pdf report with the results of the test for evaluation and documentation

This test can be run on a command whenever it is required to re-validate the mechanical alignment of diverts on an AcpTrak layout.

## Requirements:

- Diverter Diagnostic Test Technology Solution
- Singular shuttle on the track
- No physical obstructions for a shuttle to move through the entire trak layout



## Steps for usage:

- Start with a Automation Studio Project with a working AcpTrak layout
- Add the Diverter Diagnostic Test Technology Solution
- Open the Diverter Diagnostic Test Tool Importer program
- Select the root directory of your project
- Select the configuration you would like to work from
- Verify that all Relative to Two diverts are defined correctly (see additional documentation for details)
- Add any "Implicit Diverts" to the tool
- Export the files to the project using the built in export tool
- Verify the export data
- Verify "Shuttle Start Sector" is correct
- Verify MpReport FileDevice created
- Compile and Transfer to system
- Verify shuttle in "Shuttle Start Sector"
- Ensure no physical 
- Power on AcpTrak assembly
- Set "RunTest" value to true
- Upon completion, a PDF report will be generated, validate the results

## Using the Import Tool:

The first step in using the tool is to navigate to File -> Import Project. From there you can navigate to the root folder of your project you would like to import.

![image-20210526073650989](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210526073650989.png)

Once selected, a popup will appear asking you to specify the configuration you'd like to import. 

![image-20210526073717957](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210526073717957.png)

Once your configuration is selected, the tool will parse the AcpTrak assembly file for diverts and import them into the tool. The tool will scan in both the "Relative to One" and "Relative to Two" divert references types. The information will be parsed and then displayed in the tool table.

![image-20210526073750470](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210526073750470.png)

### "Base" vs "Spur" segments:

![img](file:///C:/Users/trostelc/AppData/Local/Temp/SNAGHTML3368e3.PNG)

The base and spur terminology can be correlated back the Automation Studio assembly file. The "Spur" segment, is the segment of the track the reference is attached to. The "base" segment is the segment of existing already defined track that you'd like to reference against. In the above example, the Base Segment A_39 was defined in Track 1 with a absolute position and the D_10 segment is being given a position relative to that.

The rest of the table can be used to validate the import from your assembly file. This information will be used to generate sectors automatically that are used for the test application. The only two columns that are editable are the "Divert Ref Segment" and the "Relative To". For more information on those columns reference the "Sectors Export Section"

### "Relative To One" vs "Relative to Two" vs "Implicit" 

There are 3 different type of diverts in Acp Trak system. The names used to describe them refer to how the divert is established in the configuration. The first two, Relative to One and Relative to Two directly correlate directly to the track assembly configuration position reference values. These diverts are explictely defined by the user inside the trak assembly configuration. The user has direct control over the offsets that are used.

 The third, implicit, is used to describe diverts that are created due to the existing geometry defined in the layout. These definitions do not exist inside the trak assembly configuration and are created "implicitly" by the system. With these diverts, the user has no direct influence on setting the divert offset. The offsets are determined as a byproduct of the definition of the rest of the system. However, it is important to validate that the physical offset matches what the automatically calculated virtual offset.  More on that in the "Evaluating the Report" section.

### Adding "Implicit Diverts":

To add implicit diverts, navigate to the Edit -> Add Implicit Divert

![image-20210526081712518](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210526081712518.png)

A popup dialog will appear where you can select two segments to add to the system as a divert. The list of segments contains only possible divertible segments (Ie - AA, AB and BA segments) that exist currently in the project.

![image-20210526081942144](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210526081942144.png)

After selecting the two segments and pressing "add" the segments will appear in the table.

### Divert Ref Segment and Relative To Columns

These two columns on the table are the only two editable columns in the table. This data is used to automatically create the sector on the divert to send the shuttles to. The tool attempts to figure guess at the most likely segment to use as a refence and the best starting location (for example, if a divert has a BA segment and an AA segment, it makes sense to use the BA segment from the end as that's the only valid location on the BA segment to preform the divert)

![image-20210601084949606](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210601084949606.png)

These two columns represent this data. If there is a need, the reference segment and Relative to column can be changed for a divert. 

## Adding and Using the Diverter Test Task

## Evaluating The Report

For each divert, a position measurement is taken. This measurement is used to calculate the relative offset from the two segments. Additionally the lag error between the two segments is used to determine the deviation from the virtual definition to the real world measurement.

![image-20210601090457202](C:\Users\trostelc\AppData\Roaming\Typora\typora-user-images\image-20210601090457202.png)

All measurement values are in meters to match the assembly

For each segment in the divert, two measurements exist for convenience, a "Relative to start of segment" and "Relative to end of segment" these are the same value just relative to the side of the segment as suggested in the title. The information means the exact same just is a variance in how the relationship is defined.

The final piece of information for each divert is the Measured Configuration Mismatch. This is in reference to the error in the virtual offset defined via the assembly and the real world offsets that exist between the two segments. Values above 1-2mm are of concern generally speaking. You should aim to have this value below 1mm ideally.

Implicit offset evaluation.

For implicit diverts, despite that there is no 

