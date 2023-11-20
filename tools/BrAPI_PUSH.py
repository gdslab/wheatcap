import requests
import pandas as pd
import os
from getpass import getpass
import argparse
from tqdm import tqdm

def main(csv_file):
    """
    Main function to process the CSV file and push data to the T3 system.

    Args:
    csv_file (str): The path to the CSV file to be processed.

    This function performs the following steps:
    - Authenticates the user against the T3 system API.
    - Reads the CSV file and extracts the necessary data.
    - Constructs observations from the CSV data.
    - Sends the observations to the T3 system using a POST request.
    """    
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



    # Read the input data from the CSV file
    df = pd.read_csv(csv_file)
    plot_ids = df.iloc[:, 0]
    trait_ids = df.iloc[:, 1::2]
    values = df.iloc[:, 2::2]

    # Create a list of observations to be pushed to the T3 Breedbase DB
    observations = []
    for i in tqdm(range(len(plot_ids)), desc="Processing your request"):
        trait_value_pairs = zip(trait_ids.iloc[i], values.iloc[i])
        for trait, value in trait_value_pairs:
            observation = {
                "observationUnitDbId": str(plot_ids[i]),
                "observationVariableDbId": str(trait),
                "value": str(value)
            }
            observations.append(observation)
    print("Data processing is complete. Uploading data...")

    # Send a POST request to push the observations to the T3 
    endpoint_path = "/brapi/v2/observations"
    endpoint = f"{api_base_url}{endpoint_path}"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.post(endpoint, json=observations, headers=headers)

    if response.ok:
        print("Data Upload is complete.")
    else:
        print("Error, Try Again:", response.status_code, response.text)
        response.raise_for_status()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Push Phenotypic data to T3 Breedbase DB.')
    parser.add_argument('--cfg', type=str, help='Path to the file', required=True)

    args = parser.parse_args()
    csv_file = args.cfg

    if not os.path.isfile(csv_file):
        raise ValueError("The specified file does not exist")

    main(csv_file)
