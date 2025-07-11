from fastapi import FastAPI, File, UploadFile
import tempfile
import openai
import os
from dotenv import load_dotenv
from memoria import salvar_memoria

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/responder_audio")
async def responder_audio(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
            temp.write(await file.read())
            temp_path = temp.name

        audio_file = open(temp_path, "rb")
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        texto = transcript.text.strip()
        print("📝 Texto transcrito:", texto)

        resposta = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é o Jarvis, um assistente pessoal inteligente."},
                {"role": "user", "content": texto}
            ]
        )
        conteudo = resposta.choices[0].message.content.strip()

        salvar_memoria("thais", texto, conteudo)

        return {"texto": texto, "resposta": conteudo}

    except Exception as e:
        return {"erro": str(e)}
