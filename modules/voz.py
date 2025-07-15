import os
import requests

def gerar_audio(resposta: str, nome_arquivo="resposta.mp3"):
    eleven_api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # voz padrão

    if not eleven_api_key:
        raise ValueError("Chave da ElevenLabs não encontrada")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": eleven_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": resposta,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with open(nome_arquivo, "wb") as f:
            f.write(response.content)
        return nome_arquivo
    else:
        raise Exception(f"Erro ao gerar áudio: {response.text}")
