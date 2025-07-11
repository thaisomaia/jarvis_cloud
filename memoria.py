from datetime import datetime

from google.cloud import firestore
from firestore_memoria import db

def salvar_na_memoria(pergunta: str, resposta: str, data_formatada: str):
    try:
        doc = {
            "texto": resposta,
            "pergunta_original": pergunta,
            "data_formatada": data_formatada,
            "timestamp": datetime.now()
        }
        db.collection("memorias").add(doc)
        print(f"💾 Memória salva com sucesso: {doc}")
    except Exception as e:
        print(f"Erro ao salvar memória: {e}")

def interpretar_comando_memoria(texto: str):
    texto = texto.lower()

    # Busca por data no formato: "o que eu fiz em 25/06/2025"
    if "em " in texto and "/" in texto:
        partes = texto.split("em ")
        if len(partes) > 1:
            data = partes[-1].strip().split()[0]
            return data, "data"

    # Busca genérica por palavra
    if "lembra" in texto or "memória" in texto or "memorias" in texto:
        palavras = texto.split()
        for palavra in palavras:
            if len(palavra) > 3 and palavra.isalpha():
                return palavra, "palavra"

    return None, None
