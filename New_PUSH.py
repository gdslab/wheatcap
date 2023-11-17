import requests
import pandas as pd
import glob
from getpass import getpass

# Base URL for the API
api_base_url = "https://wheatcap.triticeaetoolbox.org"

# Prompt for auth key, username, and password
auth_key = getpass("Enter your auth key: ")
username = input("Enter your username: ")
password = getpass("Enter your password: ")

# Obtain an access token from the T3 system
endpoint_path = f"/brapi/v2/token?username={username}&password={password}"
endpoint = f"{api_base_url}{endpoint_path}"
headers = {
    'Authorization': f'Token {auth_key}',
    'Content-Type': 'application/json'
}
response = requests.post(endpoint, headers=headers)

if response.ok:
    access_token = response.json()['access_token']
    print("Access Token:", access_token)  # Print the access token for debugging
else:
    print("Error:", response.status_code, response.text)
    response.raise_for_status()


# List of CSV file names to process
csv_files = glob.glob('data_push_all_corn.csv')

for file in csv_files:
    # Read the input data from the CSV file
    df = pd.read_csv(file)
    plot_ids = df.iloc[:, 0]
    trait_ids = df.iloc[:, 1::2]
    values = df.iloc[:, 2::2]

    # Create a list of observations to be pushed to the T3
    observations = []
    for i in range(len(plot_ids)):
        trait_value_pairs = zip(trait_ids.iloc[i], values.iloc[i])
        for trait, value in trait_value_pairs:
            observation = {
                "observationUnitDbId": str(plot_ids[i]),
                "observationVariableDbId": str(trait),
                "value": str(value)
            }
            observations.append(observation)

# Send a POST request to push the observations to the T3 
endpoint_path = "/brapi/v2/observations"
endpoint = f"{api_base_url}{endpoint_path}"
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.post(endpoint, json=observations, headers=headers)

if response.ok:
    status_code = response.status_code
else:
    print("Error:", response.status_code, response.text)
    response.raise_for_status()
