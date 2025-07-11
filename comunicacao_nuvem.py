import os
import requests
from datetime import datetime

BASE_URL = "https://jarvis-cloud-pey0.onrender.com"

def perguntar_para_nuvem(texto):
    payload = {"texto": texto}
    try:
        resposta = requests.post(f"{BASE_URL}/responder", json=payload)
        if resposta.status_code == 200:
            return resposta.json().get("resposta", "[Erro: resposta vazia]")
        else:
            return f"[Erro {resposta.status_code}] {resposta.text}"
    except Exception as e:
        return f"[Erro de conexão] {e}"

def buscar_memorias_por_palavra(usuario, palavra):
    payload = {"usuario": usuario, "palavra": palavra}
    try:
        resposta = requests.post(f"{BASE_URL}/memoria", json=payload)
        if resposta.status_code == 200:
            return resposta.json()
        else:
            return []
    except Exception as e:
        print(f"[Erro ao buscar memória por palavra] {e}")
        return []

def buscar_memorias_por_data(usuario, data_str):
    try:
        data_formatada = datetime.strptime(data_str, "%Y-%m-%d").date()
        payload = {"usuario": usuario, "data": str(data_formatada)}
        resposta = requests.post(f"{BASE_URL}/memoria_por_data", json=payload)
        if resposta.status_code == 200:
            return resposta.json()
        else:
            return []
    except Exception as e:
        print(f"[Erro ao buscar memória por data] {e}")
        return []

def enviar_para_nuvem(texto):
    resposta = perguntar_para_nuvem(texto)
    print("💬 Resposta:", resposta)
    return resposta

def falar_resposta(resposta):
    print("🗣️ Falando:", resposta)
    os.system(f'say "{resposta}"')
