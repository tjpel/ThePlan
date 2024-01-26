import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
from helperfunctions2 import *

key_dict = json.loads(st.secrets['textkey'])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

gbp = 0

with st.form(key='daily_checkin'):
    mental_health = st.slider("How was your mental health today?", 1, 5, value=3)

    gym_activity = st.radio("What did you do to workout today?", [
        "Stuck to The Plan",
        "Active, but not in line with The Plan",
        "Nothing"
    ])

    gym_minutes = st.number_input("Number of active minutes", step=1)
    gym_caloriesBurned = st.number_input("Number of Calories burned", step=1)
    gym_caloriesLeft = st.number_input("Number of Calories left", step=1)

    #TODO: code to prompt for loans balance and IRA from army
    checkin_submitted = st.form_submit_button("Submit")
    if checkin_submitted:
        db.collection('checkin').add({
            "date": dateToString(today),
            "rating": mental_health
        })
        db.collection('gym').add({
            'date': dateToString(today),
            'minutes': gym_minutes,
            'caloriesBurned': gym_caloriesBurned,
            'caloriesLeft': gym_caloriesLeft,
            'activity': gym_activity
        })

with st.form(key='expenses'):
    exp_category = st.selectbox(
        "What category did your expense fall under?",
        ('Rent', 'Loans', 'Groceries', 'Car', 'Fun', 'Emergency', 'Health', 'Clothes', 'Other')
    )

    exp_cc = st.checkbox("Did you use your credit card?")

    exp_amt = st.number_input("How much did you spend?", 0.0, step=0.01)

    exp_notes = st.text_input("Any notes?")

    exp_submitted = st.form_submit_button("Submit")
    if exp_submitted:
        gbp += subtractExpenses(db, exp_cc, exp_category, exp_amt, exp_notes)

with st.form(key='gbp'):
    gbp_submitted = st.form_submit_button("Tally Good Boy Points!")
    if gbp_submitted:
        gbp = pointsCalculation(db, gbp, gym_activity, mental_health)
        st.write(f"You got {gbp} good boy points today!")

with st.form(key="purge_day"):
    purge_submitted = st.form_submit_button("Purge Today")
    if purge_submitted:
        for table in ["checkin", "goodboypoints", "gym", "finances", "expenses"]:
            data = db.collection(table).where('date', '==', dateToString(today)).get()
            for row in data:
                row._reference.delete()
