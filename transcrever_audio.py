import openai

def transcrever_audio(caminho_arquivo):
    try:
        with open(caminho_arquivo, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return transcript.text
    except Exception as e:
        print(f"Erro na transcrição: {e}")
        return ""
