import os
import uuid
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def salvar_na_memoria(pergunta, resposta):
    try:
        dados = {
            "id": str(uuid.uuid4()),
            "mensagem": resposta,
            "origem": "usuário",
            "data": datetime.utcnow().isoformat()
        }
        response = supabase.table("memorias_jarvis").insert(dados).execute()
        if response.status_code != 201:
            raise Exception(f"Erro ao salvar memória: {response.text}")
    except Exception as e:
        raise Exception(f"Erro ao salvar memória: {str(e)}")
