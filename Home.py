import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



# Use the application default credentials
if not firebase_admin._apps:
    cred = credentials.Certificate('reneud-80109-firebase-adminsdk-qvjw8-a1a4d6315a.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()


st.set_page_config(page_title='CaseStudy', layout = 'wide', page_icon = "", initial_sidebar_state = 'auto')
hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if True:
    def add_bg_from_url():
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("https://www.repstatic.it/content/contenthub/img/2021/10/26/171500172-86fa9df4-be9b-4bbe-afab-87ed67b6de0f.jpg");
                    background-attachment: fixed;
                    background-size: cover
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

    add_bg_from_url()



st.markdown('''
    <div style="display: flex; justify-content: center; width:245vh; height: 100vh;">
        <h1 style="color: 	#8b4513;">RenEUd</h1>
    </div>
''', unsafe_allow_html=True)
