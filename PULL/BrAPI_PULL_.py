
# ### Importing the libraries
import requests
import pandas as pd
import numpy as np

# --- Defining function
def returning_unit(name):
    for i in range(len(name)): 
        case = name[i:]
        if case.isnumeric():
            return int(case)

# Adjusted method to fetch paginated data
def fetch_paginated_data(endpoint):
    page_size = 500
    current_page = 0
    total_pages = 1
    all_data = []

    while current_page < total_pages:
        url = f"{endpoint}&pageSize={page_size}&page={current_page}"
        response = requests.get(url)
        data = response.json()
        all_data.extend(data["result"]["data"])

        # Update metadata for pagination
        current_page += 1
        total_pages = data["metadata"]["pagination"]["totalPages"]

    return all_data

# #### Input the Trial_ID
trial_ids = [9325,9326,9358,9427]

# --- Creating list with the initial results
all_dataframes_M = []

for trial_id in trial_ids:
    api_base_url = "https://wheatcap.triticeaetoolbox.org"
    
    try:
        # Fetching data from the studies endpoint
        endpoint_path_studies = f"/brapi/v2/studies?studyDbId={trial_id}"
        data_studies = fetch_paginated_data(f"{api_base_url}{endpoint_path_studies}")
        
        # Fetching data from the observationunits endpoint
        endpoint_path_observationunits = f"/brapi/v2/observationunits?studyDbId={trial_id}"
        data_observationunits = fetch_paginated_data(f"{api_base_url}{endpoint_path_observationunits}")
    except Exception as e:
        print(f"Error fetching data for trial ID {trial_id}: {e}")
        continue

    # --- Creating list with the initial results
    M = []

    # --- Defining list of variables of interest
    variables = ["germplasmDbId", "germplasmName", "locationDbId", "locationName", 
                 "observationUnitDbId", "observationUnitName", "programDbId", 
                 "programName", "studyDbId", "studyName", "trialDbId", "trialName"]
    variables2 = ["levelName", "levelCode", "levelOrder"]
    variables3 = ["positionCoordinateX", "positionCoordinateY"]

    for unit in data_observationunits:
        partial_list = []
        # --- Looping over variables
        for var in variables:
            # --- Adding element to the partial list
            partial_list.append(unit[var])
        # --- Looping over variables
        for var in variables2:
            # --- Adding elements
            partial_list.append(unit["observationUnitPosition"]["observationLevel"][var])
        # --- Looping over variables
        for var in variables3:
            # --- Adding elements
            partial_list.append(unit["observationUnitPosition"][var])
        M.append(partial_list)
    # --- Changing M_df to a dataframe
    M_df = pd.DataFrame(M, columns = variables + variables2 + variables3)
    all_dataframes_M.append(M_df)

    # Assuming all study data rows have the same "studyType", 
    # we can extract the first one and use it for all entries.
    study_type = data_studies[0]["studyType"]
    M_df["studyType"] = study_type
    
    # Extract plot numbers using the returning_unit function
    M_df["Plot"] = [returning_unit(var) for var in M_df["observationUnitName"]]
    M_df = M_df.sort_values(by="Plot").reset_index(drop=True)
    
    # Slicing the data
    Msliced = M_df[M_df["studyDbId"] == str(trial_id)].reset_index(drop=True)
    M_df.rename(columns={'germplasmName': 'Name', 
                      'observationUnitDbId': 'PLOT_ID', 
                      'positionCoordinateX': 'X', 
                      'positionCoordinateY': 'Y', 
                      'Plot': 'PLOT_NO'}, inplace=True)
    
    # Output 1 for Plots
    M2 = M_df[['Name', 'PLOT_ID', 'studyDbId', 'studyName', 'X', 'Y', 'PLOT_NO', 'studyType' ]]
    M2.rename(columns={'X': 'Column', 'Y': 'Row', 'studyType': 'TrialType'}, inplace=True)
    # --- Printing to check
    M2.to_csv("test1_id_%s.csv" % trial_id, index=False)
    M2
    
    # Output 2 for Plots
    M3 = M_df[['PLOT_ID', 'X', 'Y', 'PLOT_NO']]
    M3.rename(columns={'X': 'Column', 'Y': 'Row'}, inplace=True)
    # --- Saving file 
    M3.to_csv("test2_id_%s.csv" % trial_id, index=False)
    # --- Printing to check  
    M3
    
    # Spatial layout - Output 3
    # --- Extrating data
    rows = sorted(M3["Row"].unique())[-1: :-1]
    cols = sorted(M3["Column"].unique())
    
    # --- Creating dataframe
    D = np.zeros((max(rows), max(cols)))
    
    # --- Looping over the rows and cols
    for row in rows:
        for col in cols:
            # --- Slicing data
            d = M3[M3["Row"] == row]
            d = d[d["Column"] == col]
            if not d.empty:
                D[row-1,col-1] = d["PLOT_ID"]
    # --- Trasforming D in dataframe
    D = np.flipud(D)
    D = pd.DataFrame(D)
    D.index = rows
    D.columns = cols
    # --- Saving file 
    D.to_csv("test3_id_%s.csv" % trial_id, index=True)
    # --- Printing to check
    D
    
    
    
  
    
    # Output 5 - Only Plot IDs and NOs
    M4 = M_df[['PLOT_NO', 'PLOT_ID']]
    # --- Saving file 
    M4.to_csv("test4_id_%s.csv" % trial_id, index=False)
    # --- Printing to check
    M4

# Combine all dataframes
final_M = pd.concat(all_dataframes_M, ignore_index=True)

