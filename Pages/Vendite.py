import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

if not firebase_admin._apps:
    cred = credentials.Certificate('reneud-80109-firebase-adminsdk-qvjw8-a1a4d6315a.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.set_page_config(page_title='CaseStudy', layout = 'wide', page_icon = "", initial_sidebar_state = 'auto')
st.markdown('# <span style="color: #8b4513;">Vendite</span>', unsafe_allow_html=True)
st.markdown('<style type="text/css">body { font-family: Arial, sans-serif; }</style>', unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" type="text/css" href="../styles.css">', unsafe_allow_html=True)

vendite_ref = db.collection('Vendite')

options = ["Nessun filtro", "ID vendita",  "ID negozio", "ID prodotto", "ID utente", "Data vendita", "Quantità venduta"]

filtri = st.multiselect("Seleziona filtro", options)
filtro_vendita = ''
filtro_negozio = ''
filtro_prodotto=''
filtro_utente=''
filtro_data=''
filtro_quantita=''

data = []
headers = ["ID vendita",  "ID negozio", "ID prodotto", "ID utente", "Data vendita", "Quantità venduta"]
vendite = vendite_ref.get()

if filtri==["Nessun filtro"]:
    
    for vendita in vendite:
        vendita_data = vendita.to_dict()
        id_vendita = vendita_data['ID']
    
        data.append([
            vendita_data['ID'],
            vendita_data['IDnegozio'],
            vendita_data['IDprodotto'],
            vendita_data['IDutente'],
            vendita_data['Datavendita'],
            vendita_data['Quantity']
            
        ])


if "ID vendita" in filtri:
    vendite_array = []
    for vendita in vendite:
        valore = vendita.to_dict()
        if valore['ID'] not in vendite_array:
            vendite_array.append(valore['ID'])
    filtro_vendita = st.selectbox("Seleziona l'ID della vendita", vendite_array)

    query1 = vendite_ref.where('ID', '==', filtro_vendita)
    elenco = query1.get()
          
    for vendita in elenco:
        vendita_data = vendita.to_dict()
        
        data.append([
            vendita_data['ID'],
            vendita_data['IDnegozio'],
            vendita_data['IDprodotto'],
            vendita_data['IDutente'],
            vendita_data['Datavendita'],
            vendita_data['Quantity']
        ])


if "ID negozio" in filtri:
    negozi_array = []
    for vendita in vendite:
        valore = vendita.to_dict()
        if valore['IDnegozio'] not in negozi_array:
            negozi_array.append(valore['IDnegozio'])
    filtro_negozio = st.selectbox("Seleziona l'ID del negozio", negozi_array)

    query1 = vendite_ref.where('IDnegozio', '==', filtro_negozio)
    elenco = query1.get()
          
    for vendita in elenco:
        vendita_data = vendita.to_dict()
        
        data.append([
            vendita_data['ID'],
            vendita_data['IDnegozio'],
            vendita_data['IDprodotto'],
            vendita_data['IDutente'],
            vendita_data['Datavendita'],
            vendita_data['Quantity']
        ])

if "ID prodotto" in filtri:
    prodotti_array = []
    for vendita in vendite:
        valore = vendita.to_dict()
        if valore['IDprodotto'] not in prodotti_array:
            prodotti_array.append(valore['IDprodotto'])
    filtro_prodotto = st.selectbox("Seleziona l'ID del prodotto", prodotti_array)

    query1 = vendite_ref.where('IDprodotto', '==', filtro_prodotto)
    elenco = query1.get()
          
    for vendita in elenco:
        vendita_data = vendita.to_dict()
        
        data.append([
            vendita_data['ID'],
            vendita_data['IDnegozio'],
            vendita_data['IDprodotto'],
            vendita_data['IDutente'],
            vendita_data['Datavendita'],
            vendita_data['Quantity']
        ])


if "ID utente" in filtri:
    utenti_array = []
    for vendita in vendite:
        valore = vendita.to_dict()
        if valore['IDutente'] not in utenti_array:
            utenti_array.append(valore['IDutente'])
    filtro_utente = st.selectbox("Seleziona l'ID del'utente", utenti_array)

    query1 = vendite_ref.where('IDutente', '==', filtro_utente)
    elenco = query1.get()
          
    for vendita in elenco:
        vendita_data = vendita.to_dict()
        
        data.append([
            vendita_data['ID'],
            vendita_data['IDnegozio'],
            vendita_data['IDprodotto'],
            vendita_data['IDutente'],
            vendita_data['Datavendita'],
            vendita_data['Quantity']
        ])


if "Data vendita" in filtri:
    data_array = []
    for vendita in vendite:
        valore = vendita.to_dict()
        if valore['Datavendita'] not in data_array:
            data_array.append(valore['Datavendita'])
    filtro_data = st.selectbox("Seleziona la data della vendita", data_array)

    query1 = vendite_ref.where('Datavendita', '==', filtro_data)
    elenco = query1.get()
          
    for vendita in elenco:
        vendita_data = vendita.to_dict()
        
        data.append([
            vendita_data['ID'],
            vendita_data['IDnegozio'],
            vendita_data['IDprodotto'],
            vendita_data['IDutente'],
            vendita_data['Datavendita'],
            vendita_data['Quantity']
        ])


if "Quantità venduta" in filtri:
    quantita_array = []
    for vendita in vendite:
        valore = vendita.to_dict()
        if valore['Quantity'] not in quantita_array:
            quantita_array.append(valore['Quantity'])
    filtro_quantita = st.selectbox("Seleziona la quantità di merce venduta", quantita_array)

    query1 = vendite_ref.where('Quantity', '==', filtro_quantita)
    elenco = query1.get()
          
    for vendita in elenco:
        vendita_data = vendita.to_dict()
        
        data.append([
            vendita_data['ID'],
            vendita_data['IDnegozio'],
            vendita_data['IDprodotto'],
            vendita_data['IDutente'],
            vendita_data['Datavendita'],
            vendita_data['Quantity']
        ])


if not filtri:
    st.info('Selezionare i filtri desiderati. Se si desidera visualizzare tutte le vendite selezionare "Nessun filtro"', icon="ℹ️")
else:
    filtered_data = []
    for element in data:
        if filtro_data != '' and element[4] != filtro_data:
            print("")
        elif filtro_vendita != '' and element[0] != filtro_vendita:
            print("")
        elif filtro_negozio != '' and element[1] != filtro_negozio:
            print("")
        elif filtro_prodotto != '' and element[2] != filtro_prodotto:
            print("")
        elif filtro_utente != '' and element[3] != filtro_utente:
            print("")
        elif filtro_quantita != '' and element[5] != filtro_quantita:
            print("")
        else:
            if element not in filtered_data:
                filtered_data.append(element)

    if filtered_data:
        st.write("Elenco dei prodotto:")
        df = pd.DataFrame(filtered_data, columns=headers)
        st.table(df)
    else:
        st.warning("Nessun prodotto corrisponde ai criteri di ricerca.")


