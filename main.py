from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Ajuste se for necessário restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

def stream_openai(pergunta):
    def generator():
        resposta = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": pergunta}],
            stream=True
        )
        for chunk in resposta:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    return generator()

@app.post("/responder")
async def responder_endpoint(dados: dict):
    pergunta = dados.get("pergunta")
    resposta_stream = stream_openai(pergunta)
    return StreamingResponse(resposta_stream, media_type="text/plain")
