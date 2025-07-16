from fastapi import FastAPI
from pydantic import BaseModel
from modules.memoria import salvar_na_memoria
from modules.clima import obter_clima
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Pergunta(BaseModel):
    pergunta: str

@app.post("/responder")
async def responder(pergunta: Pergunta):
    texto = pergunta.pergunta.lower()

    # 🌤️ Caso 1: Clima
    if "clima" in texto or "tempo" in texto:
        resposta_clima = obter_clima()
        salvar_na_memoria(texto, resposta_clima)
        return {"resposta": resposta_clima}

    # 🤖 Caso 2: GPT com memória
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            stream=True,
            messages=[
                {"role": "system", "content": "Você é o Jarvis, um assistente pessoal inteligente."},
                {"role": "user", "content": texto}
            ]
        )

        resposta = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                resposta += chunk.choices[0].delta.content

        resposta = resposta.strip()
    except Exception as e:
        resposta = f"Erro ao acessar o modelo: {str(e)}"

    salvar_na_memoria(texto, resposta)
    return {"resposta": resposta}
