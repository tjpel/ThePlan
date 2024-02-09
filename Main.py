import streamlit as st
import moneySplitter as ms
from google.cloud import firestore
from google.oauth2 import service_account
import json
from helperfunctions2 import *

key_dict = json.loads(st.secrets['textkey'])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

st.title(ms.splitIncome(db, 100))