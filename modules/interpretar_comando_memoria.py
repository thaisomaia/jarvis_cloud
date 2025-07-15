from datetime import datetime, timedelta
from modules.supabase_memoria import buscar_memorias_por_data, buscar_memorias_por_palavra
from datetime import datetime
import re

def interpretar_comando_memoria(mensagem: str, usuario: str = "thais"):
    mensagem = mensagem.lower().strip()

    # Busca por data (ex: ontem, hoje, dia 14/07/2025)
    if "ontem" in mensagem:
        data = (datetime.utcnow() - timedelta(days=1)).strftime("%d/%m/%Y")
        return buscar_memorias_por_data(usuario, data)

    if "hoje" in mensagem:
        data = datetime.utcnow().strftime("%d/%m/%Y")
        return buscar_memorias_por_data(usuario, data)

    data_match = re.search(r"(\d{2}/\d{2}/\d{4})", mensagem)
    if data_match:
        return buscar_memorias_por_data(usuario, data_match.group(1))

    # Busca por palavra-chave
    palavras_chave = ["sobre", "que eu", "você lembra", "do que", "falou de", "mencionei", "disse", "comentei"]
    if any(p in mensagem for p in palavras_chave):
        palavras = mensagem.split()
        palavra_relevante = palavras[-1]
        return buscar_memorias_por_palavra(usuario, palavra_relevante)

    return {"erro": "Não consegui interpretar o comando."}
