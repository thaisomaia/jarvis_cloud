from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os
from firestore_memoria import salvar_memoria, buscar_memorias_por_palavra, buscar_memorias_por_data

load_dotenv()

app = FastAPI()

# Inicializa API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class Pergunta(BaseModel):
    texto: str

class ConsultaPorPalavra(BaseModel):
    usuario: str
    palavra: str

class ConsultaPorData(BaseModel):
    usuario: str
    data: str  # formato: YYYY-MM-DD

@app.get("/")
def root():
    return {"mensagem": "Jarvis Cloud API rodando!"}

@app.post("/responder")
async def responder(pergunta: Pergunta):
    try:
        resposta = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é o Jarvis, um assistente pessoal inteligente."},
                {"role": "user", "content": pergunta.texto}
            ]
        )
        conteudo = resposta.choices[0].message.content.strip()

        salvar_memoria("thais", pergunta.texto, conteudo)

        return {"resposta": conteudo}
    except Exception as e:
        return {"erro": str(e)}

@app.post("/memoria")
async def memoria(consulta: ConsultaPorPalavra):
    try:
        resultados = buscar_memorias_por_palavra(consulta.usuario, consulta.palavra)
        return resultados
    except Exception as e:
        return {"erro": str(e)}

@app.post("/memoria_por_data")
async def memoria_por_data(consulta: ConsultaPorData):
    try:
        resultados = buscar_memorias_por_data(consulta.usuario, consulta.data)
        return resultados
    except Exception as e:
        return {"erro": str(e)}
