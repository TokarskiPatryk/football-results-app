from operator import not_
import os
import psycopg2
import pandas as pd 
from PIL import Image
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
import json 

matches = pd.read_json('matches.json')

with open('football_table_standings.json') as f:
    matches_completed = json.load(f)

completed = pd.json_normalize(matches_completed, record_path=['scores'], meta = ['commence_time'] , errors='ignore')

not_completed = matches[matches['completed'] == False]

# Set the page configuration of the app
st.set_page_config(
    page_title   =  "Ekstraklasa - nadchodzące mecze",
    page_icon    =  "⚽",
    layout       =  "wide"
)

# Read image into app
# prem_league_logo_filepath  =  "/assets/premier_league_logo.png"
# prem_league_logo_image     =  Image.open(prem_league_logo_filepath)


# Create columns for the layout and display the image through the 2nd one
col1, col2 = st.columns([4, 1])
# col2.image(prem_league_logo_image)

st.title("⚽🏆 Ekstraklasa - nadchodzące mecze ⚽🏆")

show_completed = st.sidebar.radio('Pozakać nadchodzące, czy niedawno ukończone mecze?', ('Nadchodzące', 'Niedawno ukończone'))


if show_completed == 'Niedawno ukończone':
    st.dataframe(completed)
    st.write("")
else:
    st.dataframe(not_completed)



# Display instructions
st.sidebar.title('Instructions 📖')
st.sidebar.write("""
The table showcases the current Premier League standings for the 2023/24 season. Toggle the visualization options to gain deeper insights!
""")
