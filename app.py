import pandas as pd 
import streamlit as st
import json 
import main

matches = pd.read_json('matches.json')

with open('football_table_standings.json') as f:
    matches_completed = json.load(f)

completed = pd.json_normalize(matches_completed, record_path=['scores'], meta = ['commence_time'] , errors='ignore')
completed = completed.pivot(index='commence_time', columns=('name'), values='score')

not_completed = matches[matches['completed'] == False]

# Set the page configuration of the app
st.set_page_config(
    page_title   =  "Ekstraklasa",
    page_icon    =  "⚽",
    layout       =  "wide"
)

# Read image into app
# prem_league_logo_filepath  =  "/assets/premier_league_logo.png"
# prem_league_logo_image     =  Image.open(prem_league_logo_filepath)


# Create columns for the layout and display the image through the 2nd one
col1, col2 = st.columns([4, 1])
# col2.image(prem_league_logo_image)

# st.title("⚽🏆 Ekstraklasa - nadchodzące mecze ⚽🏆")

show_completed = st.sidebar.radio('Pokazać nadchodzące, czy niedawno ukończone mecze?', ('Nadchodzące', 'Niedawno ukończone'))


if show_completed == 'Niedawno ukończone':
    st.title("⚽🏆 Ekstraklasa - niedawno ukończone mecze ⚽🏆")
    st.dataframe(completed)
    st.write("")
else:
    st.title("⚽🏆 Ekstraklasa - nadchodzące mecze ⚽🏆")
    st.dataframe(not_completed)

if st.button('Odśwież'):
    main.main()
    st.rerun()
# Display instructions
# st.sidebar.title('Instructions 📖')
# st.sidebar.write("""
# The table showcases the current Premier League standings for the 2023/24 season. Toggle the visualization options to gain deeper insights!
# """)
