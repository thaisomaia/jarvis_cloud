from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Carrega a chave da API do OpenAI do ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def root():
    return {"mensagem": "Jarvis Cloud API rodando!"}

class Pergunta(BaseModel):
    texto: str

@app.post("/responder")
async def responder(pergunta: Pergunta):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é o Jarvis, um assistente pessoal inteligente."},
                {"role": "user", "content": pergunta.texto}
            ]
        )
        conteudo = resposta.choices[0].message["content"].strip()
        return {"resposta": conteudo}
    except Exception as e:
        return {"erro": str(e)}
