import streamlit as st
import pandas
from datetime import date

st.title("Daily Check-in!")
today = date.today().strftime("%d/%m/%Y")
print(today)
st.subheader("Today's Date is: " + today)