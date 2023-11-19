# %%
import os
import logging 
import requests 
import psycopg2
import pandas as pd 
from dotenv import load_dotenv
from requests.exceptions import RequestException

#loading environment variables
load_dotenv()

API_KEY         =   os.getenv("API_KEY")
API_HOST        =   os.getenv("API_HOST")
LEAGUE_ID       =   os.getenv("LEAGUE_ID")
SEASON          =   os.getenv("SEASON")
DB_NAME         =   os.getenv("DB_NAME")
DB_USERNAME     =   os.getenv("DB_USERNAME")
DB_PASSWORD     =   os.getenv("DB_PASSWORD")
DB_HOST         =   os.getenv("DB_HOST")
DB_PORT         =   os.getenv("DB_PORT")

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

url = "https://odds.p.rapidapi.com/v4/sports/soccer_poland_ekstraklasa/scores"
headers       =   {"X-RapidAPI-Key": API_KEY, 
                   "X-RapidAPI-Host": API_HOST}

query_string  =   {"daysFrom":"3"}


# making a request to the API
try:
    api_response = requests.get(url, headers=headers, params=query_string, timeout=5)
    api_response.raise_for_status() 


except requests.HTTPError as http_err:
    logger.error(f'HTTP error occurred: {http_err}')


except requests.Timeout:
    logger.error('Request timed out after 15 seconds')


except RequestException as request_err:
    logger.error(f'Request error occurred: {request_err}')

# parse the api response
upcoming_matches = api_response.json()

# print api response
# logger.info(standings_data)


#4.4 step
# save response to file and read it via jq
with open('football_table_standings.json', 'w') as f:
    f.write(api_response.text)


# %%
# listing all sports
url = "https://odds.p.rapidapi.com/v4/sports"
headers       =   {"X-RapidAPI-Key": API_KEY, 
                   "X-RapidAPI-Host": API_HOST}

query_string  =   {"daysFrom":"3"}


# making a request to the API
try:
    api_response_sport = requests.get(url, headers=headers, timeout=5)
    api_response_sport.raise_for_status()
    #write sports list to file
    with open('sports_list.json', 'w') as f:
        f.write(api_response_sport.text)

        
except requests.HTTPError as http_err:
    logger.error(f'HTTP error occurred: {http_err}')


# %% [markdown]
# lista sportów
# jq .[].key ".\sports_list.json"

# %%
df = []
columns = ['time']

for matches in upcoming_matches:
    for key in matches.keys():
        if key not in columns:
            columns.append(key)
    df.append(matches)

matches_df = pd.DataFrame(df, columns=columns)
    

# %%
matches_df

# %%
selected_columns = ['commence_time', 'home_team', 'away_team', 'completed']
selected_df = matches_df[selected_columns]

# Convert commence_time to normal date format
selected_df['commence_time'] = pd.to_datetime(selected_df['commence_time'])

print(selected_df)



