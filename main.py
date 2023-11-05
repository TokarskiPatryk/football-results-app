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

url = "https://odds.p.rapidapi.com/v4/sports/americanfootball_nfl/scores"
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
standings_data = api_response.json()

# print api response
logger.info(standings_data)
