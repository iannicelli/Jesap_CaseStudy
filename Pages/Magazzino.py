import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import time
import datetime
from functions import add_product, load_data



if not firebase_admin._apps:
    cred = credentials.Certificate('casestudy-firebase.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.set_page_config(page_title='CaseStudy', layout = 'wide', page_icon = "", initial_sidebar_state = 'auto')
st.markdown('# <span style="color: #8b4513;">Magazzino</span>', unsafe_allow_html=True)
st.markdown('<style type="text/css">body { font-family: Arial, sans-serif; }</style>', unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" type="text/css" href="../styles.css">', unsafe_allow_html=True)


choice = st.selectbox('Scegli che azione eseguire', ['','Inserisci prodotto', 'Aggiungi prodotto', 'Registra vendita', 'Elimina prodotto'])
if choice == '':
    st.info('Puoi scegliere se inserire un nuovo prodotto, aggiungere un prodotto ad una categoria, registrare una vendita o eliminare un prodotto dal magazzino', icon="ℹ️")

if choice == 'Inserisci prodotto':
    # --- Inserimento campi del prodotto ---
    new_name = st.text_input("Nome prodotto")
    new_description = st.text_input("Descrizione")
    new_price = st.number_input("Prezzo")
    new_category = st.selectbox("Categoria" ,("","Abbigliamento", "Abiti", "Accessori", "Accessori moda", "Audio portatile", "Bluse", "Camicie", "Cappotti", "Cardigan", "Felpe", "Giacche", "Giacche invernali", "Giubbotti", "Gonne", "Jeans", "Leggings", "Maglietta", "Pantaloni", "Maglioni", "Piumini", "Scarpe", "Scarpe sportive", "T-shirt", "Top", "Tute", "Vestiti", "altro" ))
    new_brand_id = st.text_input("ID Marchio")

    if st.button("Inserisci prodotto"):
        if new_name=='':
            st.warning('⚠️ Inserisci un nome valido')
        elif new_description=='':
            st.warning('⚠️ Inserisci una descrizione valida')
        elif new_price==0:
            st.warning('⚠️ Inserisci un prezzo valido')
        elif new_category=='':
            st.warning('⚠️ Inserisci una categoria valida')
        elif new_brand_id=='':
            st.warning('⚠️ Inserisci un ID marchio valido')
        else:
            prodotti_ref = db.collection('Prodotti').get()

            # Inizializza una lista per memorizzare gli id dei documenti
            ids = []

            # Estrai gli id dei documenti e aggiungili alla lista
            for doc in prodotti_ref:
                data = doc.to_dict()
                ids.append(data['ID'])

            # Calcola l'id successivo
            next_id = max(ids) + 1
            
            data = {
                'ID': next_id,
                'Nome prodotto': new_name,
                'Descrizione': new_description,
                'Prezzo': new_price,
                'Categoria': new_category,
                'ID Marchio': new_brand_id,
            }
            db.collection('Prodotti').add(data)

            # Inserisco nel magazzino il nuovo prodotto con id e quantità
            magazzino_ref = db.collection('Magazzino')
            nuovo_documento = {
                'ID Prodotto': next_id,
                'Quantità': 1
            }
            magazzino_ref.add(nuovo_documento)

            st.success("Prodotto aggiunto con successo!")

elif choice == 'Aggiungi prodotto':
    new_category = st.selectbox("Categoria", ("", "Abbigliamento", "Abiti", "Accessori", "Accessori moda", "Audio portatile", "Bluse", "Camicie", "Cappotti", "Cardigan", "Felpe", "Giacche", "Giacche invernali", "Giubbotti", "Gonne", "Jeans", "Leggings", "Maglietta", "Pantaloni", "Maglioni", "Piumini", "Scarpe", "Scarpe sportive", "T-shirt", "Top", "Tute", "Vestiti", "altro"))
    prodotti_ref = db.collection('Prodotti')
    query = prodotti_ref.where('Categoria', '==', new_category)
    prodotti = query.get()

    prodotti_array = [""]
    for prodotto in prodotti:
        prodotto_data = prodotto.to_dict()
        prodotti_array.append(prodotto_data['Nomeprodotto'])


    if new_category:
        new_product = st.selectbox("Seleziona il prodotto", prodotti_array)
        query_desc = prodotti_ref.where('Nomeprodotto', '==', new_product)
        nomi = query_desc.get()

        descr_array = [""]
        for nome in nomi:
            nome_data = nome.to_dict()
            descr_array.append(nome_data['Descrizione'])

        if new_product:
            new_description = st.selectbox("Seleziona la descrizione", descr_array)
            new_quantity = st.number_input("Quantità", min_value=1, value=1)

            if st.button("Aggiungi prodotto"):
                if new_description.strip() == '':
                    st.warning('⚠️ Selezionare una descrizione valida')
                else:
                    query1 = prodotti_ref.where('Descrizione', '==', new_description.strip()).where('Nomeprodotto', '==', new_product)
                    prodotti = query1.get()
                    for prodotto in prodotti:
                        prodotto_data = prodotto.to_dict()
                        prodotto_id = prodotto_data['ID']



                    magazzino_ref = db.collection('Magazzino')
                    query2 = magazzino_ref.where('IDProdotto', '==', prodotto_id)
                    prodotti = query2.get()
                    for prodotto in prodotti:
                        prodotto_data = prodotto.to_dict()
                        prodotto_id = prodotto.id
                        prodotto_quantità = prodotto_data['Quantity']

                        magazzino_ref.document(str(prodotto_id)).update({'Quantity': prodotto_quantità + new_quantity})

                    st.success("Prodotto aggiunto con successo!")

elif choice == 'Registra vendita':
    # Inserimento prodotto
    new_product = st.text_input("Inserire l'ID del prodotto")
    if new_product:
        prodotti_ref = db.collection('Prodotti')
        query = prodotti_ref.where('ID', '==', int(new_product))
        prodotti = query.get()
        
        data = []
        headers = ["ID", "Nome prodotto", "Descrizione", "Prezzo", "Categoria", "ID Marchio"]
        
        prodotto = prodotti[0]
        prodotto_data = prodotto.to_dict()
        data.append([
                new_product,
                prodotto_data['Nomeprodotto'],
                prodotto_data['Descrizione'],
                prodotto_data['Prezzo'],
                prodotto_data['Categoria'],
                prodotto_data['IDMarchio']
            ])
        
        if data:
            st.write("Caratteristiche del prodotto:")
            df = pd.DataFrame(data, columns=headers)
            st.table(df)
        else:
            st.warning("Prodotto non trovato.")

        # Inserimento utente
        new_user = st.text_input("Inserire l'ID dell'utente")
        if new_user:
            user_ref = db.collection('Utenti')
            query_user = user_ref.where('IDUtente', '==', int(new_user))
            users = query_user.get()

            data1 = []
            headers = ["ID Utente", "Nome", "Città", "E-mail"]

            user = users[0]
            user_data = user.to_dict()
            print(user_data)
            data1.append([
                new_user,
                user_data['Nome'],
                user_data['Città'],
                user_data['E-mail']
            ])

            if data1:
                st.write("Caratteristiche dell'utente:")
                df = pd.DataFrame(data1, columns=headers)
                st.table(df)
            else:
                st.warning("Utente non trovato.")
            
            # Inserimento negozio
            new_shop = st.text_input("Inserire l'ID del negozio")
            if new_shop:
                shops_ref = db.collection('Negozi')
                query_shops = shops_ref.where('ID', '==', int(new_shop))
                shops = query_shops.get()

                data2 = []
                headers = ["ID Negozio", "Nome", "Città", "Indirizzo"]

                shop = shops[0]
                shop_data = shop.to_dict()
                data2.append([
                    new_shop,
                    shop_data['NomeNegozio'],
                    shop_data['Città'],
                    shop_data['Indirizzo']
                ])

                if data2:
                    st.write("Caratteristiche de negozio:")
                    df = pd.DataFrame(data2, columns=headers)
                    st.table(df)
                else:
                    st.warning("Negozio non trovato.")

                # Info data e orario vendita
                sale_date = st.date_input("Data vendita")
                sale_time = st.time_input("Ora vendita")

                # Combinare data e ora
                combined_datetime = datetime.datetime.combine(sale_date, sale_time)

                # Convertire in timestamp Unix
                timestamp = datetime.datetime.timestamp(combined_datetime)
                
                if timestamp:
                    vendite_ref = db.collection('Vendite').get()

                    # Inizializza una lista per memorizzare gli id dei documenti
                    ids = []

                    # Estrai gli id dei documenti e aggiungili alla lista
                    for doc in vendite_ref:
                        data = doc.to_dict()
                        ids.append(data['ID'])

                    # Calcola l'id successivo
                    next_id = max(ids) + 1

                    new_quantity = st.number_input("Quantità", min_value=1, value=1)

                    if st.button("Registra vendita"):
                        data_vendita = {
                            'Datavendita': timestamp,
                            'ID': next_id,
                            'IDnegozio': new_shop,
                            'IDprodotto': new_product,
                            'IDutente': new_user,
                            'Quantità': new_quantity,
                        }
                        st.write(data_vendita)
                        db.collection('Vendite').add(data_vendita)

                        # Aggiorna la quantità del prodotto nel magazzino
                        magazzino_ref = db.collection('Magazzino')
                        query5 = magazzino_ref.where('IDProdotto', '==', new_product)
                        prodotti = query5.get()
                        for prodotto in prodotti:
                            prodotto_data = prodotto.to_dict()
                            prodotto_id = prodotto.id
                            prodotto_quantità = prodotto_data['Quantity']

                            magazzino_ref.document(str(prodotto_id)).update({'Quantity': prodotto_quantità - new_quantity})

                        st.success("Vendita aggiunta con successo!")



