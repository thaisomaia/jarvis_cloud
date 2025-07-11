from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class ComandoEntrada(BaseModel):
    texto: str

@app.get("/")
def raiz():
    return {"mensagem": "Jarvis Cloud API rodando!"}

@app.post("/comando")
def interpretar_comando(entrada: ComandoEntrada):
    texto = entrada.texto.lower()
    
    if "adicion" in texto or "crie" in texto or "marque" in texto:
        return {"tipo": "evento", "acao": "criar", "resposta": "🔧 Criar evento"}
    
    if "compromisso" in texto or "agenda" in texto or "reuni" in texto:
        return {"tipo": "evento", "acao": "consultar", "resposta": "📅 Consultar compromissos"}
    
    return {"tipo": "desconhecido", "resposta": "🤖 Comando não reconhecido"}
