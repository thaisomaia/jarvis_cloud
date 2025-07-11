from fastapi import File, UploadFile
import tempfile
import requests

@app.post("/responder_audio")
async def responder_audio(file: UploadFile = File(...)):
    try:
        # Salva o arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
            temp.write(await file.read())
            temp_path = temp.name

        # Transcreve com a API Whisper da OpenAI
        audio_file = open(temp_path, "rb")
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        texto = transcript.text.strip()
        print("📝 Texto transcrito:", texto)

        # Gera resposta com GPT-4
        resposta = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é o Jarvis, um assistente pessoal inteligente."},
                {"role": "user", "content": texto}
            ]
        )
        conteudo = resposta.choices[0].message.content.strip()

        # Salva na memória
        salvar_memoria("thais", texto, conteudo)

        return {"texto": texto, "resposta": conteudo}
    except Exception as e:
        return {"erro": str(e)}
