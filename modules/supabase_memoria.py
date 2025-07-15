import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

load_dotenv(dotenv_path=".env.local")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def salvar_memoria(usuario: str, entrada: str, resposta: str = None, origem: str = "sistema"):
    try:
        data = {
            "usuario": usuario,
            "entrada": entrada,
            "resposta": resposta if resposta else "",
            "origem": origem,
            "timestamp": datetime.utcnow().isoformat()
        }
        supabase.table("memorias").insert(data).execute()
    except Exception as e:
        print("Erro ao salvar memória:", e)

def buscar_memorias_por_palavra(usuario: str, palavra: str):
    try:
        if not palavra:
            return []
        resultado = (
            supabase.table("memorias")
            .select("*")
            .ilike("entrada", f"%{palavra}%")
            .eq("usuario", usuario)
            .order("timestamp", desc=True)
            .execute()
        )
        return resultado.data
    except Exception as e:
        return {"erro": str(e)}

def buscar_memorias_por_data(usuario: str, data_str: str):
    try:
        data_obj = datetime.strptime(data_str, "%d/%m/%Y")
        data_formatada = data_obj.strftime("%Y-%m-%d")
        resultado = (
            supabase.table("memorias")
            .select("*")
            .eq("usuario", usuario)
            .gte("timestamp", f"{data_formatada}T00:00:00")
            .lte("timestamp", f"{data_formatada}T23:59:59")
            .order("timestamp", desc=True)
            .execute()
        )
        return resultado.data
    except Exception as e:
        return {"erro": str(e)}
