import streamlit as st
import pandas as pd

st.title('My first app')

label = pd.DataFrame({"colonna 1": [1, 2, 3, 4], "colonna 2": [10, 20, 30, 40]})
st.table(label)
st.dataframe(label)