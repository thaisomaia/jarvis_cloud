from fastapi import FastAPI, Request
from pydantic import BaseModel
from modules.memoria import salvar_na_memoria
from modules.clima import obter_clima
from modules.calendario_apple import obter_eventos_do_dia
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Ativa CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique ["http://localhost:3000"] se quiser restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Pergunta(BaseModel):
    pergunta: str

class DadosCalendario(BaseModel):
    email: str
    senha_app: str

@app.post("/responder")
async def responder(pergunta: Pergunta):
    texto = pergunta.pergunta.lower()

    # Caso 1: Clima
    if "clima" in texto or "tempo" in texto:
        resposta_clima = obter_clima()
        try:
            salvar_na_memoria(texto, resposta_clima)
        except Exception as e:
            print(f"[Erro ao salvar memória]: {e}")
        return {"resposta": resposta_clima}

    # Caso 2: GPT
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é o Jarvis, um assistente pessoal inteligente."},
                {"role": "user", "content": texto}
            ]
        )
        resposta = completion.choices[0].message.content.strip()
    except Exception as e:
        resposta = f"Erro ao acessar o modelo: {str(e)}"

    try:
        salvar_na_memoria(texto, resposta)
    except Exception as e:
        print(f"[Erro ao salvar memória]: {e}")

    return {"resposta": resposta}

@app.post("/eventos")
async def eventos(dados: DadosCalendario):
    try:
        eventos_texto = obter_eventos_do_dia(dados.email, dados.senha_app)
        return {"eventos": eventos_texto}  # <-- Corrigido: retorna a string diretamente
    except Exception as e:
        return {"erro": str(e)}
