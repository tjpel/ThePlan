import streamlit as st
import pandas
from datetime import date

st.title("Daily Check-in!")
today = date.today().strftime("%d/%m/%Y")
st.subheader("Today's Date is: " + today)

with st.form(key='daily_checkin'):
    mental_health = st.slider("How was your mental health today?", 1, 5)

    checkin_submitted = st.form_submit_button("Submit")
    if checkin_submitted:
        pass

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
        pass