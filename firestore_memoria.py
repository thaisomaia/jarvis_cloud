import os
import base64
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Lê a chave codificada do ambiente
firebase_key_base64 = os.getenv("FIREBASE_KEY_BASE64")

# Decodifica e salva temporariamente
caminho_temporario = "/tmp/firebase_key.json"
with open(caminho_temporario, "wb") as f:
    f.write(base64.b64decode(firebase_key_base64))

# Inicializa o Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(caminho_temporario)
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
