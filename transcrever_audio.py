import os
import glob
import whisper

def obter_ultimo_arquivo_audio(pasta_audios="audios"):
    arquivos = sorted(
        glob.glob(os.path.join(pasta_audios, "*.wav")),
        key=os.path.getmtime,
        reverse=True,
    )

    if not arquivos:
        print("❌ Nenhum arquivo de áudio encontrado na pasta 'audios'.")
        return None

    print(f"🎧 Último arquivo encontrado: {arquivos[0]}")
    return arquivos[0]

def transcrever_com_whisper(caminho_arquivo):
    print("🔄 Carregando modelo Whisper (medium)...")
    model = whisper.load_model("medium")

    print("📝 Iniciando transcrição com Whisper...")
    resultado = model.transcribe(caminho_arquivo, language="pt")

    print(f"📄 Transcrição: {resultado['text']}")
    return resultado["text"]
