import streamlit as st
from datetime import date, timedelta
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

today = date.today()
yesterday = today - timedelta(days = 1)
yester2day = yesterday - timedelta(days = 1)
monthago = today - timedelta(days = 30)

def dateToString(date: date):
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

    checkin_submitted = st.form_submit_button("Submit")
    if checkin_submitted:
        conn.table('checkin').insert({
            "date": dateToString(today),
            "rating": mental_health
        }).execute()

with st.form(key="gym"):
    gym_activity = st.radio("What did you do today?", [
        "Stuck to The Plan",
        "Active, but not in line with The Plan",
        "Nothing"
    ])

    gym_minutes = st.number_input("Number of active minutes", step=1)
    gym_caloriesBurned = st.number_input("Number of Calories burned", step=1)
    gym_caloriesConsumed = st.number_input("Number of Calories consumed", step=1)

    gym_submitted = st.form_submit_button("Submit")
    if gym_submitted:
        conn.table('gym').insert({
            "date": dateToString(today),
            "activity": gym_activity,
            "minutes": gym_minutes,
            "caloriesBurned": gym_caloriesBurned,
            "caloriesConsumed": gym_caloriesConsumed
        }).execute()
        pointsCalculation()

#TODO: make so this only comes up when there's an expense
        #ALT: just do calc and display on landing page
with st.form(key="finances"):
    ft = conn.table('finances')
    data = conn.table('finances').select('*').execute().data
    st.write(data)
    st.write(dateToString(today))
    st.write(dateToString(yesterday))
    data = conn.table('finances').select('*').eq('date', dateToString(yesterday)).execute().data
    st.write(data)
    fyester = data[0]

    st.write("Have any of these changed?")
    usgensp = st.number_input("U.S. Bank General Spending", value=fyester['usgensp'], step=0.01)
    usfunsp = st.number_input("U.S. Bank Fun Spending", value=fyester['usfunsp'], step=0.01)
    ussav = st.number_input("U.S. Bank Savings", value=fyester['ussav'], step=0.01)
    acorns = st.number_input("Acorns", value=fyester['acorns'], step=0.01)
    

    #TODO: code to prompt for loans balance and IRA from army

    fin_submitted = st.form_submit_button("Submit")
    if fin_submitted:
        st.write("Accessable Funds: $" + str(round(usgensp+usfunsp+ussav+acorns, 2)))


with st.form(key="purge_day"):
    purge_submitted = st.form_submit_button("Purge Today")
    if purge_submitted:
        for table in ["checkin", "goodboypoints", "gym"]:
            conn.table(table).delete().eq("date", dateToString(today)).execute()
