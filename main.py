from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os
import tempfile
import base64

from firestore_memoria import (
    salvar_memoria,
    buscar_memorias_por_palavra,
    buscar_memorias_por_data
)

from modules.transcrever_audio import transcrever_audio
from modules.comunicacao_nuvem import falar_resposta
from modules.gravar_audio import gravar_audio_inteligente

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

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

@app.post("/ativar")
async def ativar_jarvis():
    print("🎙️ Iniciando gravação...")
    caminho_arquivo = gravar_audio_inteligente()
    print("✅ Áudio gravado.")

    print("🧠 Transcrevendo...")
    texto = transcrever_audio(caminho_arquivo)
    print(f"📝 Texto: {texto}")

    if not texto:
        return {"erro": "Nenhum áudio detectado"}

    print("💬 Enviando ao ChatGPT...")
    resposta = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é o Jarvis, um assistente pessoal inteligente."},
            {"role": "user", "content": texto}
        ]
    )
    conteudo = resposta.choices[0].message.content.strip()
    print(f"💡 Resposta: {conteudo}")

    salvar_memoria("thais", texto, conteudo)

    print("🔊 Gerando áudio da resposta...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        audio_response = openai.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            input=conteudo
        )
        audio_response.stream_to_file(temp_audio.name)

        with open(temp_audio.name, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

    print("✅ Jarvis concluído.")
    return {
        "texto": texto,
        "resposta": conteudo,
        "audio_base64": encoded
    }
