import os
from supabase import create_client
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def salvar_na_memoria(mensagem, origem="sistema", usuario="thais"):
    try:
        data = datetime.utcnow().isoformat()
        payload = {
            "mensagem": mensagem,
            "origem": origem,
            "usuario": usuario,
            "data": data
        }
        response = supabase.table("memorias").insert(payload).execute()
        print("✅ Memória salva:", response)
    except Exception as e:
        print("❌ Erro ao salvar no Supabase:", e)
