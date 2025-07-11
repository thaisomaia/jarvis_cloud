import whisper
import os

# Carrega o modelo medium para melhor precisão no português
modelo = whisper.load_model("medium")

def transcrever_audio(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"❌ Arquivo não encontrado: {caminho_arquivo}")
        return ""

    print("🧠 Transcrevendo com Whisper...")

    # Transcreve com idioma forçado e temperatura 0 para reduzir erros aleatórios
    resultado = modelo.transcribe(caminho_arquivo, language="pt", temperature=0)
    
    texto = resultado["text"].strip()
    print(f"📝 Texto: {texto if texto else '[vazio]'}")
    
    return texto
