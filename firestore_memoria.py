import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

# Caminho para a chave do Firebase
CAMINHO_CHAVE = "jarvis-memory-3eba0-firebase-adminsdk-fbsvc-33f25f1cfa.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(CAMINHO_CHAVE)
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
