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
st.markdown('# <span style="color: #8b4513;">Prodotti</span>', unsafe_allow_html=True)
st.markdown('<style type="text/css">body { font-family: Arial, sans-serif; }</style>', unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" type="text/css" href="../styles.css">', unsafe_allow_html=True)


prodotti_ref = db.collection('Prodotti')

options = ["Nessun filtro", "Prezzo", "Categoria", "Id prodotto", "Nome prodotto"]

filtri = st.multiselect("Seleziona filtro", options)
filtro_categoria = ''
filtro_prezzo = ''
filtro_id=''
filtro_nome=''

data = []
headers = ["ID", "Nome prodotto", "Descrizione", "Prezzo", "Categoria", "Quantità"]
prodotti = prodotti_ref.get()
magazzino_ref = db.collection('Magazzino')

if filtri==["Nessun filtro"]:
    
    for prodotto in prodotti:
        prodotto_data = prodotto.to_dict()
        id_prodotto = prodotto_data['ID']
        query = magazzino_ref.where('IDProdotto', '==', id_prodotto)
        magazzino = query.get()
        if not magazzino: 
            quantita = 0
        else:
            giusto = magazzino[0]
            giusto_data = giusto.to_dict()
            quantita = giusto_data['Quantity']


        prodotto_data = prodotto.to_dict()
        data.append([
            prodotto_data['ID'],
            prodotto_data['Nomeprodotto'],
            prodotto_data['Descrizione'],
            prodotto_data['Prezzo'],
            prodotto_data['Categoria'],
            quantita
        ])
        

if "Categoria" in filtri:
    categoria_array = []
    for prodotto in prodotti:
        valore = prodotto.to_dict()
        if valore['Categoria'] not in categoria_array:
            categoria_array.append(valore['Categoria'])
    filtro_categoria = st.selectbox("Seleziona la categoria", categoria_array)

    query1 = prodotti_ref.where('Categoria', '==', filtro_categoria.strip())
    elenco = query1.get()

    for prodotto in elenco:
        prodotto_data = prodotto.to_dict()
        id_prodotto = prodotto_data['ID']
        query = magazzino_ref.where('IDProdotto', '==', id_prodotto)
        magazzino = query.get()
        if not magazzino: 
            quantita = 0
        else:
            giusto = magazzino[0]
            giusto_data = giusto.to_dict()
            quantita = giusto_data['Quantity']

        prodotto_data = prodotto.to_dict()
        data.append([
            prodotto_data['ID'],
            prodotto_data['Nomeprodotto'],
            prodotto_data['Descrizione'],
            prodotto_data['Prezzo'],
            prodotto_data['Categoria'],
            quantita
        ])


if "Prezzo" in filtri:
    prezzi_array = []
    for prodotto in prodotti:
        valore = prodotto.to_dict()
        if valore['Prezzo'] not in prezzi_array:
            prezzi_array.append(valore['Prezzo'])
    filtro_prezzo = st.selectbox("Seleziona il prezzo", prezzi_array)

    query1 = prodotti_ref.where('Prezzo', '==', filtro_prezzo)
    elenco = query1.get()
            
    for prodotto in elenco:
        prodotto_data = prodotto.to_dict()
        id_prodotto = prodotto_data['ID']
        query = magazzino_ref.where('IDProdotto', '==', id_prodotto)
        magazzino = query.get()
        if not magazzino: 
            quantita = 0
        else:
            giusto = magazzino[0]
            giusto_data = giusto.to_dict()
            quantita = giusto_data['Quantity']

        prodotto_data = prodotto.to_dict()
        data.append([
            prodotto_data['ID'],
            prodotto_data['Nomeprodotto'],
            prodotto_data['Descrizione'],
            prodotto_data['Prezzo'],
            prodotto_data['Categoria'],
            quantita
        ])


if "Nome prodotto" in filtri:
    nome_array = []
    for prodotto in prodotti:
        valore = prodotto.to_dict()
        if valore['Nomeprodotto'] not in nome_array:
            nome_array.append(valore['Nomeprodotto'])
    filtro_nome = st.selectbox("Seleziona il nome del prodotto", nome_array)

    query1 = prodotti_ref.where('Nomeprodotto', '==', filtro_nome)
    elenco = query1.get()
            
    for prodotto in elenco:
        prodotto_data = prodotto.to_dict()
        id_prodotto = prodotto_data['ID']
        query = magazzino_ref.where('IDProdotto', '==', id_prodotto)
        magazzino = query.get()
        if not magazzino: 
            quantita = 0
        else:
            giusto = magazzino[0]
            giusto_data = giusto.to_dict()
            quantita = giusto_data['Quantity']

        prodotto_data = prodotto.to_dict()
        data.append([
            prodotto_data['ID'],
            prodotto_data['Nomeprodotto'],
            prodotto_data['Descrizione'],
            prodotto_data['Prezzo'],
            prodotto_data['Categoria'],
            quantita
        ])



if "Id prodotto" in filtri:
    id_array = []
    for prodotto in prodotti:
        valore = prodotto.to_dict()
        if valore['ID'] not in id_array:
            id_array.append(valore['ID'])
    filtro_id = st.selectbox("Seleziona ID prodotto", id_array)

    query1 = prodotti_ref.where('ID', '==', filtro_id)
    elenco = query1.get()

    for prodotto in elenco:
        prodotto_data = prodotto.to_dict()
        id_prodotto = prodotto_data['ID']
        query = magazzino_ref.where('IDProdotto', '==', id_prodotto)
        magazzino = query.get()
        if not magazzino: 
            quantita = 0
        else:
            giusto = magazzino[0]
            giusto_data = giusto.to_dict()
            quantita = giusto_data['Quantity']

        prodotto_data = prodotto.to_dict()
        data.append([
            prodotto_data['ID'],
            prodotto_data['Nomeprodotto'],
            prodotto_data['Descrizione'],
            prodotto_data['Prezzo'],
            prodotto_data['Categoria'],
            quantita
        ])


            
if not filtri:
    st.info('Selezionare i filtri desiderati. Se si desidera visualizzare tutti i prodotti selezionare "Nessun filtro"', icon="ℹ️")
else:
    filtered_data = []
    for element in data:
        if filtro_prezzo != '' and element[3] != filtro_prezzo:
            print("")
        elif filtro_categoria != '' and element[4] != filtro_categoria:
            print("")
        elif filtro_id != '' and element[0] != filtro_id:
            print("")
        elif filtro_nome != '' and element[1] != filtro_nome:
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
