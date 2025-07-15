import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import sounddevice as sd
import whisper
import requests
import numpy as np
import scipy.io.wavfile as wavfile
from modules.voz_eleven import falar_com_eleven

# Configurações
DURACAO = 6  # duração da gravação em segundos
SAMPLE_RATE = 44100
USUARIO = "thais"
ENDPOINT = "http://127.0.0.1:8000/responder"

# Caminho temporário do arquivo de áudio
AUDIO_PATH = "entrada_voz.wav"

def gravar_audio():
    print("🎙️ Gravando... Fale agora.")
    audio = sd.rec(int(DURACAO * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()
    wavfile.write(AUDIO_PATH, SAMPLE_RATE, audio)
    print("✅ Gravação concluída.")

def transcrever_audio():
    print("🧠 Transcrevendo com Whisper (modelo medium)...")
    model = whisper.load_model("medium")  # Modelo com mais precisão
    result = model.transcribe(AUDIO_PATH, language="pt", fp16=False)
    texto = result["text"].strip()
    print(f"📝 Transcrição: {texto}")
    return texto

def enviar_para_jarvis(mensagem):
    print("🚀 Enviando para o Jarvis...")
    try:
        response = requests.post(ENDPOINT, json={"mensagem": mensagem})
        if response.status_code == 200:
            conteudo = response.json().get("resposta", "")
            print(f"🤖 Jarvis respondeu: {conteudo}")
            return conteudo
        else:
            print("❌ Erro ao enviar para o Jarvis:", response.text)
            return ""
    except Exception as e:
        print("❌ Erro de conexão com o Jarvis:", str(e))
        return ""

def executar_comando_voz():
    gravar_audio()
    texto = transcrever_audio()
    resposta = enviar_para_jarvis(texto)
    if resposta:
        falar_com_eleven(resposta)

if __name__ == "__main__":
    executar_comando_voz()
