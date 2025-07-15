from gravar_audio import gravar_audio

if __name__ == "__main__":
    caminho = gravar_audio(duracao_segundos=5)
    if caminho:
        print(f"🎧 Arquivo de áudio salvo em: {caminho}")
    else:
        print("⚠️ Falha na gravação.")
