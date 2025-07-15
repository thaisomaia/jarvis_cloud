import sounddevice as sd
from scipy.io.wavfile import write
import os
from datetime import datetime

pasta_destino = "audios"
os.makedirs(pasta_destino, exist_ok=True)

fs = 44100  # Taxa de amostragem
duracao = 5  # Duração em segundos

print("🎙️ Gravando áudio por 5 segundos...")
gravacao = sd.rec(int(duracao * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nome_arquivo = f"{pasta_destino}/{timestamp}.wav"
write(nome_arquivo, fs, gravacao)

print(f"✅ Gravação finalizada. Salvando em {nome_arquivo}")
