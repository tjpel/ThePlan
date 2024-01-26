import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

key_dict = json.loads(st.secrets['textkey'])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

checkin = db.collection('checkin')
for c in checkin.list_documents():
    print(c.get()._data)

query = checkin.where('test', '==', 'test').get()
for q in query:
    print(q._data)
