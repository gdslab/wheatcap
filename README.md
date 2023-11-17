# wheatcap

## Steps to Pull Plot Map Data from T3 using BrAPI

To download plot map data from T3, update the trial_ids variable in the script:
- trial_ids = [9325, 9326, 9358, 9427]  # Replace with your desired trial IDs



After running the script with the specified trial IDs, you will receive four spreadsheet files:

- Test 1: Contains data with headers - Name, PLOTID, studyDBId, studyName, Column, Row, PLOT_NO, and TrialType.
- Test 2: Contains data with headers - PLOT_ID, Column, Row, and PLOT_NO.
- Test 3: Contains the plot map.
- Test 4: Contains data with headers - PLOT_NO and PLOT_ID.


## Steps to PUSH Phenotypic data to T3 using BrAPI

Each User must enter the following:
- Auth code:
- Username:
- Password:

To upload the processed phenotypic data to T3 Breedbase database. 
- Note:- The data should be in CSV format and arranged in the form:
- ObservationUnitDbId | ObservationVariableDbId | Value

