import sounddevice as sd
import numpy as np
import wave
import time
import os

def gravar_audio_inteligente():
    fs = 44100
    segundos_silencio = 6.0  # Aumentado para permitir frases mais longas com pausas
    limite_silencio = 20     # Mais sensível para captar voz com variações
    nome_arquivo = "entrada.wav"
    caminho_completo = os.path.expanduser(f"~/Desktop/{nome_arquivo}")

    print("\n🎤 Fale agora... (gravação será encerrada automaticamente ao detectar silêncio por 6 segundos)")

    audio_total = []
    tempo_ultimo_audio = time.time()

    def callback(indata, frames, time_info, status):
        nonlocal tempo_ultimo_audio, audio_total

        volume = np.linalg.norm(indata) * 10
        print(f"Nível de áudio: {volume:.2f}")

        if volume > limite_silencio:
            tempo_ultimo_audio = time.time()
            audio_total.extend(indata.copy())
        elif time.time() - tempo_ultimo_audio < segundos_silencio:
            audio_total.extend(indata.copy())

    try:
        with sd.InputStream(samplerate=fs, channels=1, callback=callback):
            while True:
                if time.time() - tempo_ultimo_audio > segundos_silencio and len(audio_total) > 0:
                    print("⏹ Silêncio detectado, finalizando gravação.")
                    break
                time.sleep(0.1)
    except Exception as e:
        print(f"❌ Erro durante a gravação: {e}")
        return None

    if not audio_total:
        print("❌ Nenhum som foi capturado.")
        return None

    audio_np = np.array(audio_total)

    try:
        with wave.open(caminho_completo, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes((audio_np * 32767).astype(np.int16).tobytes())
    except Exception as e:
        print(f"❌ Erro ao salvar o áudio: {e}")
        return None

    print("✅ Áudio gravado.")
    return caminho_completo
