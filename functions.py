import pandas as pd
import streamlit as st


# Funzione per aggiungere un nuovo prodotto
def add_product(df, new_product):
    new_id = df['ID'].max() + 1 if 'ID' in df.columns else 1
    new_row = pd.DataFrame([[new_id] + new_product], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    return df


# Funzione per caricare i dati da un file Excel
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

