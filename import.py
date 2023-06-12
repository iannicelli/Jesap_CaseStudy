import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate('reneud-80109-firebase-adminsdk-qvjw8-a1a4d6315a.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

excel_file = pd.ExcelFile('CASESTUDY_2.xlsx')

printed_sheet_names = set()  # Insieme per tenere traccia dei nomi dei fogli già stampati


for sheet_name in excel_file.sheet_names:
    if sheet_name not in printed_sheet_names:
        printed_sheet_names.add(sheet_name)
    
for sheet_name in printed_sheet_names:
    print(sheet_name)
    dataframe = excel_file.parse(sheet_name)
    data_json = dataframe.to_dict(orient='records')
    
    x = 0

    for data in data_json: 
       doc_ref = db.collection(sheet_name).document()  # Imposta un ID casuale per il documento
       doc_ref.set(data)
       x += 1
        
        
    print(f'Caricati {x} documenti in {sheet_name}')