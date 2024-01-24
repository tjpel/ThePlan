import streamlit as st
from datetime import datetime, timedelta, timezone
#from supabase import create_client, Client
from st_supabase_connection import SupabaseConnection
#import os

#TODO: make one big form?
#TODO: change yesterdays to last entry, will break if no entry for yesterday
#load_dotenv(".env")
#SUPABASE_URL = os.environ['sb_url']
#SUPABASE_KEY = os.environ['sb_key']

#supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
conn = st.connection("supabase", type=SupabaseConnection)

today = datetime.now(tz=timezone(-timedelta(hours=6)))
yesterday = today - timedelta(days = 1)
yester2day = today - timedelta(days = 2)
monthago = today - timedelta(days = 30)

def dateToString(date: datetime):
    return date.strftime(r"%Y/%m/%d")  

def checkPreviousMH(level:int, max: int):
    data = conn.table('checkin').select('rating').lt('date', dateToString(today)).gt('date', dateToString(monthago)).eq('rating', level).execute().data
    print(len(data))
    return len(data) < max


def pointsCalculation():
    points = 0

    if gym_activity == "Stuck to The Plan":
        points += 3
    elif gym_activity == "Active, but not in line with The Plan":
        points += 1
    else:
        points += -2

    #check if bad mental health day
    if points < 0:
        if mental_health == 1 and checkPreviousMH(1, 1):
            points = 0
        elif mental_health == 2 and checkPreviousMH(2, 4):
            points = points // 2

    goodboytable = conn.table('goodboypoints')

    gbtYester = goodboytable.select('*').eq('date', dateToString(yesterday)).execute().data
    goodboytable.insert({
        "date": dateToString(today),
        "todaysPoints": points,
        "culmPoints": gbtYester[0]['culmPoints'] + points
        }).execute()


st.title("Daily Check-in!")
st.subheader("Today's Date is: " + dateToString(today))

with st.form(key='daily_checkin'):
    mental_health = st.slider("How was your mental health today?", 1, 5, value=3)

    gym_activity = st.radio("What did you do today?", [
        "Stuck to The Plan",
        "Active, but not in line with The Plan",
        "Nothing"
    ])

    gym_minutes = st.number_input("Number of active minutes", step=1)
    gym_caloriesBurned = st.number_input("Number of Calories burned", step=1)
    gym_caloriesConsumed = st.number_input("Number of Calories consumed", step=1)

    """
    st.write("Have any of these changed?")
    usgensp = st.number_input("U.S. Bank General Spending", value=fyester['usgensp'], step=0.01)
    usfunsp = st.number_input("U.S. Bank Fun Spending", value=fyester['usfunsp'], step=0.01)
    ussav = st.number_input("U.S. Bank Savings", value=fyester['ussav'], step=0.01)
    acorns = st.number_input("Acorns", value=fyester['acorns'], step=0.01)
    """

    #TODO: code to prompt for loans balance and IRA from army

    checkin_submitted = st.form_submit_button("Submit")
    if checkin_submitted:
        conn.table('checkin').insert({
            "date": dateToString(today),
            "rating": mental_health
        }).execute()

data = conn.table('finances').select('*').eq('date', dateToString(yesterday)).execute().data
#st.write(data)
fyester = data[0]
with st.form(key='expenses'):
    exp_category = st.selectbox(
        "What category did your expense fall under?",
        ('Rent', 'Groceries', 'Fun', 'Loans')
    )

    exp_submitted = st.form_submit_button("Submit")
    if exp_submitted:
        pass


with st.form(key="purge_day"):
    purge_submitted = st.form_submit_button("Purge Today")
    if purge_submitted:
        for table in ["checkin", "goodboypoints", "gym"]:
            conn.table(table).delete().eq("date", dateToString(today)).execute()

    
