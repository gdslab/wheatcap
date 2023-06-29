#!/usr/bin/env python
# coding: utf-8

# ### Importing the libraries

# In[1]:


import requests
import pandas as pd
import numpy as np

# --- Defining function
def returning_unit(name):

    for i in range(len(name)): 
        case = name[i : ]
        if case.isnumeric():
            unit = int(case)
            return unit

# --- Stopping the code

# #### Input the Trial_ID

# In[2]:


#---Specifying the ID of the trial to collect from T3
trial_ids = [9325]


# In[3]:

for trial_id in trial_ids:
    #---Connecting to the T3 Breedbase using the endpoints

    api_base_url = "https://wheatcap.triticeaetoolbox.org"

    endpoint_path = f"/brapi/v2/observationunits?studyDbId={trial_id}&pageSize=1000" #--Page size was kept at 1000 because it is the max

    endpoint = f"{api_base_url}{endpoint_path}"


    #----The request
    r = requests.get(endpoint)  


    # #### The results from GET

# In[4]:


    #---Converting the obtained response to a text
    B = r.text

    # --- Getting data as a dictionary
    A = r.json()

    # --- Getting the result data
    R = A["result"]["data"]


# In[5]:


    # --- Creating list with the final results
    M = [] #---M is the big dictionary


# In[6]:


    # --- Defining list of variables of interest
    variables = ["germplasmDbId","germplasmName","locationDbId", "locationName", "observationUnitDbId", "observationUnitName", "programDbId", "programName","studyDbId","studyName","trialDbId","trialName"]
    variables2 = ["levelName", "levelCode", "levelOrder"]
    variables3 = ["positionCoordinateX", "positionCoordinateY"]


# In[7]:


    # --- Looping over the elements of the list
    for i in range(len(R)):
        # --- Selecting the element
        partial = R[i]
        
        # --- Defining partial list
        partial_list = []
        # --- Looping over variables 
        for var in variables:
            # --- Adding element to the partial list
            partial_list.append(partial[var])
            
        # --- Looping over variables
        for var in variables2:
            # --- Adding elements 
            partial_list.append(partial["observationUnitPosition"]["observationLevel"][var])
    
        # --- Looping over variables
        for var in variables3:
            # --- Adding elements
            partial_list.append(partial["observationUnitPosition"][var])
    
        # --- Adding to the final result file
        M.append(partial_list)
    # --- Changing M to a dataframe
    M = pd.DataFrame(M, columns = variables + variables2 + variables3)


# In[8]:

    #M["Plot"] = [int(var.split('-')[-1].split('_')[-1].strip('PLOT')) for var in M["observationUnitName"]]
    M["Plot"] = [returning_unit(var) for var in M["observationUnitName"]]
    M = M.sort_values(by = "Plot").reset_index(drop = True)
    
    # --- Slicing the data
    Msliced = M[M["studyDbId"] == str(trial_id)].reset_index(drop = True)
    M.rename(columns = {'germplasmName':'Name', 'observationUnitDbId':'PLOT_ID', 'positionCoordinateX':'X', 'positionCoordinateY':'Y', 'Plot':'PLOT_NO' }, inplace = True)
    
    
    # ### Output 1 for Plots 

# In[12]:


    # --- Geting a new dataframe
    M2 = M[['Name', 'PLOT_ID', 'studyDbId', 'studyName', 'X', 'Y', 'PLOT_NO']]
    
    M2.rename(columns = {'X':'Column', 'Y':'Row' }, inplace = True)
    # --- Saving file 
    M2.to_csv("test1_id_%s.csv" % trial_id, index = False) #---the first CSV
    # --- Printing to check
    M2
    
    
    # ### Output 2 for Plots

# In[10]:


    M3 = M[['PLOT_ID','X', 'Y', 'PLOT_NO']]
    # --- Saving file 
    M3.rename(columns = {'X':'Column', 'Y':'Row' }, inplace = True)
    # --- Printing to check
    M3.to_csv("test2_id_%s.csv" % trial_id, index = False) #---The second CSV
    M3
    
    
    # ### Spatial layout - Output 3

# In[13]:


    # --- Extrating data
    rows = sorted(M3["Row"].unique())[-1 :  : -1]
    cols = sorted(M3["Column"].unique())
    # --- Creating dataframe
    D = []
    # --- Looping over the rows
    for row in rows:
        # --- Slicing data
        d = M3[M3["Row"] == row].sort_values(by = "Column").reset_index(drop = True)
        # --- Appending the data
        D.append(list(d["PLOT_NO"]))
    # --- Trasforming D in dataframe
    D = pd.DataFrame(D)
    D.index = rows
    D.columns = cols
    # --- Printing to check
    D.to_csv("test3_id_%s.csv" % trial_id, index = True) #---The third CSV
    D



#### Output 4 - Only Plot IDS and NOs
    # In[ ]:
    M4 = M[['PLOT_NO', 'PLOT_ID']]
    # --- Saving file 
    M4.to_csv("test4_id_%s.csv" % trial_id, index = False) #---The second CSV
    M4



