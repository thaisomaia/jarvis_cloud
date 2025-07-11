import os
import json
import base64
from google.cloud import firestore
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

# Carregar a variável base64 do .env
firebase_credentials_base64 = os.getenv("CHAVE_FIREBASE_BASE64")

if not firebase_credentials_base64:
    raise ValueError("CHAVE_FIREBASE_BASE64 não encontrada no .env")

# Decodifica e transforma em dicionário
firebase_credentials_json = json.loads(base64.b64decode(firebase_credentials_base64))

# Cria as credenciais
credentials = service_account.Credentials.from_service_account_info(firebase_credentials_json)

# Inicializa Firestore
db = firestore.Client(credentials=credentials, project=credentials.project_id)

# --- FUNÇÕES DE BUSCA ---

def buscar_memorias_por_data(data_formatada: str):
    """
    Retorna todas as memórias salvas para uma data específica no campo 'data_formatada'
    """
    try:
        docs = db.collection("memorias").where("data_formatada", "==", data_formatada).stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Erro ao buscar memórias por data: {e}")
        return []

def buscar_memorias_por_palavra(palavra: str):
    """
    Retorna todas as memórias que contenham a palavra no campo 'texto'
    """
    try:
        docs = db.collection("memorias").stream()
        resultados = []
        for doc in docs:
            d = doc.to_dict()
            if palavra.lower() in d.get("texto", "").lower():
                resultados.append(d)
        return resultados
    except Exception as e:
        print(f"Erro ao buscar memórias por palavra: {e}")
        return []
