from datetime import datetime
import os
import json

CAMINHO_MEMORIA = os.path.expanduser("~/jarvis_local/memoria_jarvis.json")

def salvar_memoria(pergunta: str, resposta: str):
    nova_entrada = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pergunta": pergunta,
        "resposta": resposta
    }

    if os.path.exists(CAMINHO_MEMORIA):
        with open(CAMINHO_MEMORIA, "r") as f:
            memoria = json.load(f)
    else:
        memoria = []

    memoria.append(nova_entrada)

    with open(CAMINHO_MEMORIA, "w") as f:
        json.dump(memoria, f, indent=2)
