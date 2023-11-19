# Data Download and Upload to/from the T3 Breedbase Database Using BrAPI

## Introduction
This document outlines a pipeline developed by the [*Geospatial Data Science Laboratory*](https://gdslab.org/) at Purdue University, West Lafayette, Indiana, for integrating UAS-Hub with the T3 Breedbase database. We have successfully established a connection between our UAS-Hub and the T3 Breedbase database, facilitated by a unique identifier linking the phenotypic and genotypic information within the UAS data uploaded by plant breeders to T3. We access plot-level data uploaded to the T3 Database by various breeding programs, using several breeding application programming interface (BrAPI) calls within a Python programming environment. After processing the data, we extract phenotypic information, which is then processed further and uploaded back to T3. On the UAS-Hub website, we implemented a **data pull** pipeline that allows users to input trial IDs of each field trial, facilitating the retrieval of plot map information for data visualization. Additionally, we developed a **data push** pipeline that enables the successful upload of processed phenotypic information back to the T3 Breedbase database. Our current setup involves a process that connects two database systems: the UAS-Hub and the T3 Breedbase databases. The first step in this process is pulling plot map information from the T3 database, a crucial parameter for UAS data processing. The second step involves preparing the processed data and uploading it back to T3 for further analysis. This upload is made possible using trait database IDs (trial_db ids) provided by the T3 database team. We extract these IDs for each piece of phenotypic information based on UAS flight dates. Our data upload pipeline, developed in Python, is then used to transfer the processed data back to T3.

![Illustrating the BrAPI Connection](/figures/BrAPI.png)


## Sample Results
### Results on Data PULL
The Data PULL results show the data downloaded from the T3 Breedbase Database after establishing a successful connection. The main data obtained include: Trial name, Plot ID, studyDBId, studyName, Column number, Row number, Plot number, Plot map, Trial type, etc. After running the script with the specified trial IDs, the user will receive four spreadsheet files such as ```test1_id_{trial_id}.csv```, ```test2_id_{trial_id}.csv```, ```test3_id_{trial_id}.csv```, and ```test4_id_{trial_id}.csv```. Below is a sample of the results:

- Test 1
| Name          | PLOT_ID | studyDbId |        studyName         | Column | Row |  PLOT_NO |    TrialType      |
|---------------|---------|-----------|--------------------------|--------|-----|----------|-------------------|
| KSTdGD30-8    | 1373887 | 9326      | 22_TdGD_Hays_Yield_Trials|   1    |  1  |    1     | phenotyping_trial | 
| KSTdGD80-134  | 1373536 | 9326      | 22_TdGD_Hays_Yield_Trials|   1    |  27 |    2     | phenotyping_trial | 
| KS061406LN~26 | 1376236 | 9326      | 22_TdGD_Hays_Yield_Trials|   21   |  3  |    3     | phenotyping_trial | 
| KSTdGD41-43   | 1374505 | 9326      | 22_TdGD_Hays_Yield_Trials|   21   |  29 |    4     | phenotyping_trial | 
| KSTdGD32-106  | 1374375 | 9326      | 22_TdGD_Hays_Yield_Trials|   21   |  5  |    5     | phenotyping_trial | 

- Test 2
| PLOT_ID |  Column |  Row  |  PLOT_NO |
|---------|---------|-------|----------|
| 1373887 |   1     |  1    |    1     | 
| 1373536 |   1     |  27   |    2     | 
| 1376236 |   21    |  3    |    3     | 
| 1374505 |   21    |  29   |    4     | 
| 1374375 |   21    |  5    |    5     |  

- Test 3
![Plot map ](/figures/Plotmap.png)

- Test 4
|  PLOT_NO | PLOT_ID |
|----------|---------|
|    1     | 1373887 |
|    2     | 1373536 |
|    3     | 1376236 |
|    4     | 1374505 |
|    5     | 1374375 | 


### Results on Data PUSH
The data uploaded on T3 Breedbase Database can be accessed on the [*WheatCAP production website*](https://wheatcap.triticeaetoolbox.org/breeders/trial/9316?format=) from the sections: Upload Data Files and Phenotype Summary Statistics.
![Upload Data Files ](/figures/upload.png)
![T3 Backend ](/figures/output.png)
![Histogram ](/figures/histo.png)


### Note:
- The data displayed are sample datasets for both the PULL and PUSH Processes.


## Environment
The code is developed using python 3.7 on Windows OS. No special computing power is required.

## Quick start
### Installation
1. Clone this repository, and we'll call the directory that you cloned ${POSE_ROOT}.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Data preparation
#### Data PULL
- All that is required here is the ```trial_ids```. The user can then get the desired results illustrated above. The user is at liberty to download multiple trials at a time from the T3 Breedbase database as long as the needed ```trial_ids``` are known.

#### Data PUSH
- This is required as per the requirements of the T3 Breedbase and the BrAPI used. After data processing, the extracted phenotypic information as processed by the Texas A & M team is shown below:
![TAMU Processed ](/figures/TAMU.png)

- There is a need to obtain the ```ObservationVariableDbId``` for each phenotype information according to the flight dates. This can only be obtained from the LookUp table spreadsheet provided by the T3 Team (check the data folder).
- The UAV flight dates are converted to Julian dates, and their equivalent ```trait_db_id``` are obtained and entered into the spreadsheet containing the values for each plot as shown below:
![PU Processed](/figures/PU.png)



### Executing the Code
#### Data PULL
- Run below code in your command line:

```
python tools/BrAPI_PULL.py

```
- This will prompt for the ```trial_ids```. Enter that, and you should get the CSV files as described in the sample result section above.

#### Data PUSH
- Ensure you have the final spreadsheet to upload in the folder ```data``` in .csv format.
- Then enter the following in your command line and input your file name accordingly:

```
python tools/BrAPI_PUSH.py --cfg data/cornell_data_2022.csv

```
- The script will prompt the user to enter the following:
    - Authentication code
    - Username
    - Password
- If all is correct and the user has submission priviledges, the script should work fine and you can confirm the upload just as shown in the sample result section.
- If you are not authorized and need authorization, please contact David Waring at djw64@cornell.edu

### Links
- BrAPI documentation can be accessed at: [*TAMU/T3 BrAPI*](https://notes.triticeaetoolbox.org/w39PW42OSTeDvDNX_WVhZg)
- Tutorials from the T3 Team at: [*2023 WheatCAP Workshop*](https://notes.triticeaetoolbox.org/s/L6d41SNKQ)


### Contact
If you use our code and/or need more information, please contact us at:
```
Prof. Jinha Jung, Purdue University at jinha@purdue.edu
Ismail Olaniyi, Purdue University at iolaniyi@purdue.edu
```
