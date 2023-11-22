import pandas as pd 
import streamlit as st
import json 
import main

# Load data
completed, upcoming = main.run()

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
#col1, col2 = st.columns([4, 1])
# col2.image(prem_league_logo_image)

# st.title("⚽🏆 Ekstraklasa - nadchodzące mecze ⚽🏆")

show_completed = st.sidebar.radio('Pokazać nadchodzące, czy niedawno ukończone mecze?', ('Nadchodzące', 'Niedawno ukończone'))

st.title("⚽🏆 Ekstraklasa ⚽🏆")

if show_completed == 'Niedawno ukończone':
    st.title("Niedawno ukończone mecze")
    if(completed is not None):
        st.dataframe(completed)
    else:
        st.write("Brak niedawno ukończonych meczów")
    st.write("")
else:
    st.title("Nadchodzące mecze")
    st.dataframe(upcoming, hide_index=True)
