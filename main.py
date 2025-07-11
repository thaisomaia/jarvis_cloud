from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
import json
from datetime import datetime
from firestore_memoria import salvar_memoria, buscar_memorias_por_palavra, buscar_memorias_por_data
import base64

app = FastAPI()

# Carregar chave do Firebase a partir da variável de ambiente base64
chave_base64 = os.getenv("FIREBASE_KEY_BASE64")
if chave_base64:
    caminho_chave = "firebase_key.json"
    with open(caminho_chave, "wb") as f:
        f.write(base64.b64decode(chave_base64))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = caminho_chave

# Chave da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class RequisicaoPergunta(BaseModel):
    texto: str

class RequisicaoMemoria(BaseModel):
    usuario: str
    palavra: str

class RequisicaoData(BaseModel):
    usuario: str
    data: str  # Ex: "2025-07-10"

@app.post("/responder")
async def responder(req: RequisicaoPergunta):
    pergunta = req.texto.strip()
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente pessoal inteligente."},
            {"role": "user", "content": pergunta}
        ]
    )["choices"][0]["message"]["content"]

    salvar_memoria(pergunta, resposta, usuario="thais")
    return {"resposta": resposta}

@app.post("/memoria")
async def memoria(req: RequisicaoMemoria):
    resultados = buscar_memorias_por_palavra(req.palavra, req.usuario)
    return resultados

@app.post("/memoria_por_data")
async def memoria_por_data(req: RequisicaoData):
    try:
        data = datetime.strptime(req.data, "%Y-%m-%d").date()
        resultados = buscar_memorias_por_data(data.isoformat(), req.usuario)
        return resultados
    except Exception as e:
        return {"erro": f"Erro ao interpretar data: {str(e)}"}
