import os
import json
import base64
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# ✅ Carrega .env.local para garantir acesso à variável
load_dotenv(dotenv_path=".env.local")

# 🔐 Recupera chave codificada
chave_base64 = os.getenv("CHAVE_FIREBASE_BASE64")
if not chave_base64:
    raise ValueError("CHAVE_FIREBASE_BASE64 não encontrada")

# 🔓 Decodifica e inicializa Firebase
chave_json = json.loads(base64.b64decode(chave_base64).decode("utf-8"))

if not firebase_admin._apps:
    cred = credentials.Certificate(chave_json)
    firebase_admin.initialize_app(cred)

# 🔁 Exporta o client do Firestore
db = firestore.client()
