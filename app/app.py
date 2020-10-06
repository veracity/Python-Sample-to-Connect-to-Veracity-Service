"""

Example script for connecting to IoT HUB API to query data.
Uses client credentials configured in config.json (should be stored elsewhere
in a production solution)

__author__ = "DNV GL Digital Solutions"
__copyright__ = "Copyright 2020 (c) DNV GL"
__version__ = "1.0"

"""

# Import libraries we need
import json
import logging
from os import path
import requests
import sys

from msal import ConfidentialClientApplication

# Find the config file
config_file = ".\config.json"

# If there are arguments given to this script, we'll use the first as path to the config file
if len(sys.argv) > 1:
    config_file = sys.argv[1]

# Check if the config file exists
if not path.exists(config_file):
    print("Could not find configuration file '{0}'".format(config_file))
    print("Either add .\config.json or specify file as the first parameter to the script")
    quit()

# Parse the config file
try:
    config = json.load(open(config_file))
except json.decoder.JSONDecodeError as error_description:
    print("An JSON error occured in the config file({0}): {1}".format(config_file, error_description))
    quit()

# Build authority from tanenat
authority = "https://login.microsoftonline.com/{0}".format(config["tenant"])

# Setup the application with client id, client secret and tenant name
app = ConfidentialClientApplication(
    config["client_id"], authority=authority,
    client_credential=config["client_secret"]
    )

# Try to get token from memory cache, can be expanded to use a more
# permanent storage like redis
token_result = app.acquire_token_silent(config["scope"], account=None)


def GetAllAssets (workspaceId):
    # --------------- Example 1a- Get a list of assets from Asset API ---------------
    print("Making call to Asset API to get list of assets in the workspace: " + workspaceId) 

    api_response = requests.get(config["assetApiEndpoint"] + "Workspaces/" + workspaceId + "/assets",
                             headers={'Authorization': 'Bearer ' + token_result["access_token"],
                            'Ocp-Apim-Subscription-Key': config["apiSubscriptionKey"]})

    if api_response.status_code >= 300:
        # API call failed with wrong status code
        print("Call returned with Status Code " + str(api_response.status_code))
    else:
        # API call successfull, decode response to JSON and print data to console
        try:
            print("API call Status Code {0}:".format(str(api_response.status_code)))
            data = api_response.json()
            print(json.dumps(data, indent=2))
        except json.decoder.JSONDecodeError as error_description:
            print("JSON Decode Error " + str(error_description))
    return


def MyAssets_FromTimeSeriesApi ():
    # --------------- Example 1b - Get a list of assets from Time Series API ---------------
    # - alternative method to get all assets visible to user (not constrainted to single workspace)

    print("Making call to Time Series API to get list of assets") 
    api_response = requests.get(config["timeSeriesApiEndpoint"] + "Assets",
                             headers={'Authorization': 'Bearer ' + token_result["access_token"],
                            'Ocp-Apim-Subscription-Key': config["apiSubscriptionKey"]})

    if api_response.status_code >= 300:
        # API call failed with wrong status code
        print("Call returned with Status Code " + str(api_response.status_code))
    else:
        # API call successfull, decode response to JSON and print data to console
        try:
            print("API call Status Code {0}:".format(str(api_response.status_code)))
            data = api_response.json()
            print(json.dumps(data, indent=2))
        except json.decoder.JSONDecodeError as error_description:
            print("JSON Decode Error " + str(error_description))
    return

def GetAsset(assetId):
  # --------------- Example 2 - The the static data for an asset ---------------
    print("Making call to Asset API to get asset static data for 1 asset") 
    api_response = requests.get(config["assetApiEndpoint"] + "Assets/" + assetId,
                            headers={'Authorization': 'Bearer ' + token_result["access_token"],
                            'Ocp-Apim-Subscription-Key': config["apiSubscriptionKey"]})

    if api_response.status_code >= 300:
        # API call failed with wrong status code
        print("Call returned with Status Code " + str(api_response.status_code))
    else:
        # API call successfull, decode response to JSON and print data to console
        try:
            print("API call Status Code {0}:".format(str(api_response.status_code)))
            data = api_response.json()
            print(json.dumps(data, indent=2))
        except json.decoder.JSONDecodeError as error_description:
            print("JSON Decode Error " + str(error_description))
    return


def GetAssetDataChannelList(assetId):
   # --------------- Example 3 - Retrieve Meta data for an Asset from Time Series API ---------------
    print("Making call to Time Series API to get list of assets") 
    api_response = requests.get(config["timeSeriesApiEndpoint"] + "DataChannelList/" + assetId ,
                             headers={'Authorization': 'Bearer ' + token_result["access_token"],
                            'Ocp-Apim-Subscription-Key': config["apiSubscriptionKey"]})

    if api_response.status_code >= 300:
        # API call failed with wrong status code
        print("Call returned with Status Code " + str(api_response.status_code))
    else:
        # API call successfull, decode response to JSON and print data to console
        try:
            print("API call Status Code {0}:".format(str(api_response.status_code)))
            data = api_response.json()
            print(json.dumps(data, indent=2))
        except json.decoder.JSONDecodeError as error_description:
            print("JSON Decode Error " + str(error_description))
    return


def GetTimeSeriesData(assetId, dataChannelIds, start, end, downScaleInt, limit):

     # --------------- Example 4 - Retrieve DATA from the Time Series API ---------------
    print("Making call to Time Series API to get some data :)") 

    queryPayload = {
        "downScaleInt": downScaleInt,
        "start": start,
        "end": end,
        "limit": limit,
        "assetIds": assetId,
        "dataChannelIds": dataChannelIds,
        "dataChannelIdType": "ShortId",
        "typeOption": "Data"
    }

    api_response = requests.post(config["timeSeriesApiEndpoint"] + "TimeSeriesData/.getTimeSeriesData",
                             headers={'Authorization': 'Bearer ' + token_result["access_token"],
                            'Ocp-Apim-Subscription-Key': config["apiSubscriptionKey"]}, json=queryPayload)

    if api_response.status_code >= 300:
        # API call failed with wrong status code
        print("Call returned with Status Code " + str(api_response.status_code))
    else:
        # API call successfull, decode response to JSON and print data to console
        try:
            print("API call Status Code {0}:".format(str(api_response.status_code)))
            data = api_response.json()
            print(json.dumps(data, indent=2))
        except json.decoder.JSONDecodeError as error_description:
            print("JSON Decode Error " + str(error_description))

    return

def Get_LastestTimeSeriesData(assetId, dataChannelIds, limit):

     # --------------- Example 5 - Retrieve Latest N DATA from the Time Series API ---------------
    print("Making call to Time Series API to get some data :)") 

    queryPayload = {
        "latestNValues": limit,
        "assetIds": assetId,
        "dataChannelIds": dataChannelIds,
        "dataChannelIdType": "ShortId",
        "typeOption": "Data"
    }

    api_response = requests.post(config["timeSeriesApiEndpoint"] + "TimeSeriesData/.latest",
                             headers={'Authorization': 'Bearer ' + token_result["access_token"],
                            'Ocp-Apim-Subscription-Key': config["apiSubscriptionKey"]}, json=queryPayload)

    if api_response.status_code >= 300:
        # API call failed with wrong status code
        print("Call returned with Status Code " + str(api_response.status_code))
    else:
        # API call successfull, decode response to JSON and print data to console
        try:
            print("API call Status Code {0}:".format(str(api_response.status_code)))
            data = api_response.json()
            print(json.dumps(data, indent=2))
        except json.decoder.JSONDecodeError as error_description:
            print("JSON Decode Error " + str(error_description))

    return


if not token_result:
    # No token in cache, let's get a new one
    token_result = app.acquire_token_for_client(scopes=config["scope"])

# Check for token
if "access_token" in token_result:

    # Make a request to the api
    print("Acquired token successfully") 

    # Get all assets and their static data (limited to selected worksapce)
    GetAllAssets(config["workSpaceId"])

    # alternative method to get all IoT assets and static data (globally)
    #MyAssets_FromTimeSeriesApi()

    myAssetId = "4000c0e0-0b16-4c78-ae07-a39749c052e2"

    # get static data for an individual asset
    #GetAsset(myAssetId)

    # get data channel list for an asset
    #GetAssetDataChannelList(myAssetId)

    # Get data (downsampled)
    #GetTimeSeriesData([myAssetId], ["IL1", "IL2"], "2018-01-01","2020-01-05", "PT60M", 9999)

    # get data (raw)
    #GetTimeSeriesData([myAssetId], ["IL1", "IL2"], "2018-01-01","2020-01-05", None, 9999)
    
    # find out latest data point datetime and value
    #Get_LastestTimeSeriesData([myAssetId], ["IL1", "IL2"], 1)

else:
    # Token error
    print(token_result.get("error"))
    print(token_result.get("error_description"))
    print(token_result.get("correlation_id"))
