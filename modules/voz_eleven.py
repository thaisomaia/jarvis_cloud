import os
import requests
from dotenv import load_dotenv
from playsound import playsound

# Carrega variáveis do .env.local
load_dotenv(dotenv_path=".env.local")

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
voice_id = "CstacWqMhJQlnfLPxRG4"  # Voz em português BR

def falar_com_eleven(texto: str):
    try:
        # Melhora a entonação adicionando pausas com quebras de linha
        texto_formatado = (
            texto.replace(". ", ".\n")
                 .replace("! ", "!\n")
                 .replace("? ", "?\n")
        )

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?optimize_streaming_latency=0"

        headers = {
            "xi-api-key": ELEVEN_API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }

        data = {
            "text": texto_formatado,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.6,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            with open("resposta.mp3", "wb") as f:
                f.write(response.content)
            playsound("resposta.mp3")
        else:
            print("Erro ao gerar áudio:", response.text)

    except Exception as e:
        print("Erro geral ao gerar ou tocar áudio:", str(e))
