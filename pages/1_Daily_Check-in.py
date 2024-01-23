import streamlit as st
import pandas
from datetime import date

st.title("Daily Check-in!")
today = date.today().strftime("%d/%m/%Y")
st.subheader("Today's Date is: " + today)

with st.form(key='daily_checkin'):
    mental_health = st.slider("How was your mental health today?")
    st.text("Any Expenses Today?")

    checkin_submitted = st.form_submit_button("Submit")
    if checkin_submitted:
        pass

with st.form(key="gym"):
    gym_withProgram = st.checkbox("Went to gym and did all of expected routine")
    gym_noProgram = st.checkbox("I did something to work out today but not what the plan was")
    gym_minutes = st.number_input("Number of active minutes")
    gym_caloriesBurned = st.number_input("Number of Calories burned")
    gym_caloriesConsumed = st.number_input("Number of Calories consumed")

    gym_submitted = st.form_submit_button("Submit")
    if gym_submitted:
        pass