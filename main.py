from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

from firestore_memoria import salvar_memoria, buscar_memorias_por_palavra

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Pergunta(BaseModel):
    texto: str
    usuario: str = "padrao"

@app.post("/responder")
def responder(pergunta: Pergunta):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": pergunta.texto}]
        ).choices[0].message["content"]

        # Salva na memória do Firestore
        salvar_memoria(pergunta.usuario, pergunta.texto, resposta)

        return {"resposta": resposta}
    except Exception as e:
        return {"erro": str(e)}

@app.post("/memoria")
def memoria(pergunta: Pergunta):
    try:
        memorias = buscar_memorias_por_palavra(pergunta.usuario, pergunta.texto)
        return {"memorias": memorias}
    except Exception as e:
        return {"erro": str(e)}
