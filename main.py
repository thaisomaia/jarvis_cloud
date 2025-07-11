from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Event(BaseModel):
    titulo: str
    data: str
    hora: str

@app.get("/")
def home():
    return {"mensagem": "Jarvis Cloud API rodando!"}

@app.post("/criar_evento")
def criar_evento(event: Event):
    # Aqui futuramente chamaremos funções reais
    return {
        "mensagem": f"Evento '{event.titulo}' criado para {event.data} às {event.hora}."
    }
