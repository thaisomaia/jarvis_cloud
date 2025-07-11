from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
import firebase_admin
from firebase_admin import credentials, firestore
import base64
from firestore_memoria import salvar_memoria, buscar_memorias_por_palavra

app = FastAPI()

# === GPT Setup ===
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Firebase Setup via variável de ambiente ===
FIREBASE_KEY_BASE64 = os.getenv("FIREBASE_KEY_BASE64")
if FIREBASE_KEY_BASE64:
    key_json = base64.b64decode(FIREBASE_KEY_BASE64).decode("utf-8")
    if not firebase_admin._apps:
        cred = credentials.Certificate.from_json(key_json)
        firebase_admin.initialize_app(cred)
db = firestore.client()

# === Modelos ===
class Pergunta(BaseModel):
    texto: str

class ConsultaMemoria(BaseModel):
    usuario: str
    palavra: str

# === Endpoints ===

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

        # Salva na memória
        salvar_memoria("thais", pergunta.texto, conteudo)

        return {"resposta": conteudo}
    except Exception as e:
        return {"erro": str(e)}

@app.post("/memoria")
def memoria(consulta: ConsultaMemoria):
    try:
        resultados = buscar_memorias_por_palavra(consulta.usuario, consulta.palavra)
        return resultados
    except Exception as e:
        return {"erro": str(e)}
