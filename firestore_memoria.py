import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

# Caminho para a chave do Firebase (carregada da variável de ambiente em base64)
import base64
import json

chave_base64 = os.getenv("FIREBASE_KEY_BASE64")
chave_json = base64.b64decode(chave_base64).decode("utf-8")
chave_dict = json.loads(chave_json)

if not firebase_admin._apps:
    cred = credentials.Certificate(chave_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def salvar_memoria(usuario: str, pergunta: str, resposta: str):
    doc_ref = db.collection("memorias").document()
    doc_ref.set({
        "usuario": usuario,
        "pergunta": pergunta,
        "resposta": resposta,
        "timestamp": datetime.utcnow()
    })

def buscar_memorias_por_palavra(usuario: str, palavra: str):
    docs = db.collection("memorias") \
             .where("usuario", "==", usuario) \
             .stream()

    resultados = []
    for doc in docs:
        data = doc.to_dict()
        if palavra.lower() in data.get("pergunta", "").lower() or palavra.lower() in data.get("resposta", "").lower():
            resultados.append(data)
    return resultados

def buscar_memorias_por_data(usuario: str, data: str):
    data_dt = datetime.fromisoformat(data)
    docs = db.collection("memorias") \
             .where("usuario", "==", usuario) \
             .where("timestamp", ">=", data_dt) \
             .where("timestamp", "<", data_dt.replace(hour=23, minute=59, second=59)) \
             .stream()
    return [doc.to_dict() for doc in docs]
