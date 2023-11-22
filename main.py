# %%
import os
import logging
import sys 
import requests 
import pandas as pd 
from pandas import json_normalize
from dotenv import load_dotenv
from requests.exceptions import RequestException

# TODO: Add tests for testing if the api response is valid
# TODO: add function/ find a way to format the data in a way that is easy to read on the site
# OR
# TODO: find a new data source that can show upcoming matches and current standings (maybe second api with current standings)
# TODO: add pictures to the site
# TODO: add a new navigation to the site instead of using the sidebar with radio buttons
# TODO: add github actions to run tests

#loading environment variables
load_dotenv()

API_KEY         =   os.getenv("API_KEY")
API_HOST        =   os.getenv("API_HOST")

#logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler (This handler writes messages to a log file on the system)
file_handler = logging.FileHandler('football_table_standings.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Create a console handler (This handler writes messages to console)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Instantiate the logger object (to use handlers we need to add them to the logger object)
logger = logging.getLogger()

# Add the file handler to the logger
logger.addHandler(file_handler)

# Add the console handler to the logger
logger.addHandler(console_handler)

# using logging is better than using print statements because we can control the level of logging

# %%
# Api request

def get_api_response(url, headers, query_string):
    """
    This function makes a request to the API and returns the response
    """
    try:
        api_response = requests.get(url, headers=headers, params=query_string, timeout=5)
        api_response.raise_for_status() 
        return api_response.json()

    except requests.HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')


    except requests.Timeout:
        logger.error('Request timed out after 15 seconds')


    except RequestException as request_err:
        logger.error(f'Request error occurred: {request_err}')

# %%
url = "https://odds.p.rapidapi.com/v4/sports/soccer_poland_ekstraklasa/scores"
headers       =   {"X-RapidAPI-Key": API_KEY, 
                "X-RapidAPI-Host": API_HOST}

query_string  =   {"daysFrom":"3"}


# parse the api response
upcoming_matches = get_api_response(url, headers, query_string)

# %%
# lista sportów
# jq .[].key ".\sports_list.json"
url = "https://odds.p.rapidapi.com/v4/sports"
headers       =   {"X-RapidAPI-Key": API_KEY, 
                   "X-RapidAPI-Host": API_HOST}
query_string  =   {"daysFrom":"3"}

all_sports = get_api_response(url, headers, query_string)

# %% 

def get_upcoming_matches():
    """
    Retrieves all matches from a data source and filters out completed matches.
    
    Returns:
        pandas.DataFrame: DataFrame containing upcoming matches with columns: 
        'commence_time', 'home_team', 'away_team', 'completed'.
    """
    columns = ['commence_time', 'home_team', 'away_team', 'completed']
    # TODO fix the error 'cannot access local variable 'upcoming_matches' where it is not defined'
    upcoming_matches2 = pd.json_normalize(upcoming_matches)[columns]
    upcoming_matches2 = upcoming_matches2[upcoming_matches2['completed'] == False]
    upcoming_matches2.drop(columns=['completed'], inplace=True)
    
    upcoming_matches2['commence_time'] = pd.to_datetime(upcoming_matches2['commence_time']).dt.strftime('%d-%m %H:%M')
    
    return upcoming_matches2


def get_completed_matches():
    """
    Retrieves all matches from a data source and filters out upcoming matches via json normalize using 'scores' as record path.

    Returns:
        pandas.DataFrame: DataFrame containing completed matches with columns: 
        'team', 'score', 'commence_time'. (two rows per match)
    """
    matches_list =pd.json_normalize(upcoming_matches,
                      record_path=['scores'],
                      meta = ['commence_time'] ,
                      errors='ignore')
    if not matches_list.empty:
        matches_list = matches_list.pivot(index='commence_time', 
                                          columns=('name'), 
                                          values='score')
        matches_list.reset_index(inplace=True)
        return matches_list
    
    
def run():
    #upcoming_matches = get_api_response(url, headers, query_string)
    completed = get_completed_matches()
    upcoming = get_upcoming_matches()
    return upcoming, completed




