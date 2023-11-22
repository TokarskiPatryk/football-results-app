import pandas as pd 
import streamlit as st
import json 
import main

# run a function from main to get completed matches
completed = main.get_completed_matches()

# run a function from main to get upcoming matches
upcoming = main.get_upcoming_matches()

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
    st.dataframe(upcoming)

if st.button('Odśwież'):
    main.rerun()
    st.rerun()
# Display instructions
# st.sidebar.title('Instructions 📖')
# st.sidebar.write("""
# The table showcases the current Premier League standings for the 2023/24 season. Toggle the visualization options to gain deeper insights!
# """)
