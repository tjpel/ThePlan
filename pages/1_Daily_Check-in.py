import streamlit as st
import pandas as pd
from datetime import date

CHECKIN_CSV_PATH = 'data/checkins.csv'

checkin_df = pd.read_csv(CHECKIN_CSV_PATH)

st.title("Daily Check-in!")
today = date.today().strftime("%d/%m/%Y")
st.subheader("Today's Date is: " + today)

with st.form(key='daily_checkin'):
    mental_health = st.slider("How was your mental health today?", 1, 5)

    checkin_submitted = st.form_submit_button("Submit")
    if checkin_submitted:
        checkin_df.loc[len(checkin_df.index)] = [today, mental_health]
        checkin_df.to_csv(CHECKIN_CSV_PATH, index=False)

with st.form(key="gym"):
    gym_activity = st.radio("What did you do today?", [
        "Stuck to The Plan",
        "Active, but not in line with The Plan",
        "Nothing"
    ])

    gym_minutes = st.number_input("Number of active minutes")
    gym_caloriesBurned = st.number_input("Number of Calories burned")
    gym_caloriesConsumed = st.number_input("Number of Calories consumed")

    gym_submitted = st.form_submit_button("Submit")
    if gym_submitted:
        gym_row = pd.DataFrame({'Date': [today]})