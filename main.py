import streamlit as st
import pandas as pd

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Use the application default credentials
if not firebase_admin._apps:
    cred = credentials.Certificate('casestudy-firebase.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

print("Firebase Initialized")