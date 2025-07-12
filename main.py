import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from responder import responder_com_gpt
from memoria import salvar_na_memoria, interpretar_comando_memoria
from firestore_memoria import buscar_memorias_por_palavra, buscar_memorias_por_data

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequisicaoTexto(BaseModel):
    texto: str

@app.post("/responder")
async def responder(request: RequisicaoTexto):
    texto = request.texto
    print(f"🧠 Pergunta recebida: {texto}")

    # Verifica se é um comando de busca por memória
    chave, tipo_busca = interpretar_comando_memoria(texto)

    if tipo_busca == "data":
        memorias = buscar_memorias_por_data(chave)
        if memorias:
            resposta = "\n".join([m["texto"] for m in memorias])
            print("📚 Resposta da memória (por data):", resposta)
            return {"resposta": resposta}
    elif tipo_busca == "palavra":
        memorias = buscar_memorias_por_palavra(chave)
        if memorias:
            resposta = "\n".join([m["texto"] for m in memorias])
            print("📚 Resposta da memória (por palavra):", resposta)
            return {"resposta": resposta}

    # Não encontrou → chama o GPT
    resposta_gpt = responder_com_gpt(texto)
    print("🤖 Resposta do GPT:", resposta_gpt)

    # Gera timestamp completo em UTC
    agora = datetime.now(timezone.utc)
    timestamp = agora.isoformat()

    # Salva na memória (Firestore)
    salvar_na_memoria(texto, resposta_gpt, timestamp)

    return {"resposta": resposta_gpt}
