from transcrever_audio import obter_ultimo_arquivo_audio, transcrever_com_whisper
from responder import responder_com_gpt
from memoria import salvar_na_memoria
from datetime import datetime

# 🎧 Obtém o último arquivo gravado
arquivo = obter_ultimo_arquivo_audio()

if not arquivo:
    print("❌ Nenhum áudio para transcrever. Encerrando.")
    exit()

# 📝 Transcreve o áudio
transcricao = transcrever_com_whisper(arquivo)

# 🚀 Envia para o GPT
print("🚀 Enviando transcrição para o Jarvis...")
resposta = responder_com_gpt(transcricao)

# 💾 Salva na memória com a data atual
data_formatada = datetime.now().strftime("%d/%m/%Y")
salvar_na_memoria(transcricao, resposta, data_formatada)

# 🤖 Imprime a resposta final
print(f"🤖 Resposta do Jarvis: {resposta}")
