from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# 🔐 Carrega as variáveis de ambiente
load_dotenv()

# 🧠 Inicializa o Firebase com base64
if not firebase_admin._apps:
    import base64
    import json
    base64_cred = os.getenv("FIREBASE_KEY_BASE64")
    cred_dict = json.loads(base64.b64decode(base64_cred).decode("utf-8"))
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# 🧠 Inicializa a OpenAI com nova sintaxe (>= 1.0.0)
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🛰️ Inicializa o FastAPI
app = FastAPI()

class Pergunta(BaseModel):
    texto: str

@app.post("/responder")
async def responder(pergunta: Pergunta):
    try:
        resposta = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é o assistente Jarvis."},
                {"role": "user", "content": pergunta.texto},
            ],
            model="gpt-4"
        )
        conteudo = resposta.choices[0].message.content

        # 🧠 Salva no Firestore
        doc_ref = db.collection("memorias").document()
        doc_ref.set({
            "pergunta": pergunta.texto,
            "resposta": conteudo
        })

        return {"resposta": conteudo}
    except Exception as e:
        return {"erro": str(e)}
