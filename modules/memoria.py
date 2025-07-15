import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis do .env.local
load_dotenv(dotenv_path=".env.local")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def salvar_na_memoria(mensagem: str, origem: str = "usuário"):
    url = f"{SUPABASE_URL}/rest/v1/memorias"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    data = {
        "mensagem": mensagem,
        "origem": origem,
        "data": datetime.utcnow().isoformat()
    }
    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        raise Exception(f"Erro ao salvar memória: {response.text}")

def buscar_memorias_por_palavra(palavra: str):
    url = f"{SUPABASE_URL}/rest/v1/memorias?mensagem=ilike.*{palavra}*&select=*"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        raise Exception(f"Erro ao buscar memórias: {response.text}")
    return response.json()
