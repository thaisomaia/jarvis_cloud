import os
from datetime import date
from caldav import DAVClient
from dotenv import load_dotenv

load_dotenv()

def obter_eventos_do_dia():
    url = os.getenv("APPLE_CALENDAR_URL")
    usuario = os.getenv("APPLE_CALENDAR_USER")
    senha = os.getenv("APPLE_CALENDAR_PASSWORD")

    if not url or not usuario or not senha:
        raise Exception("Credenciais do Apple Calendar não encontradas no .env")

    client = DAVClient(url, username=usuario, password=senha)
    principal = client.principal()
    calendars = principal.calendars()

    if not calendars:
        return "Nenhum calendário encontrado."

    hoje = date.today()
    eventos_do_dia = []

    for calendario in calendars:
        eventos = calendario.date_search(hoje)
        for evento in eventos:
            try:
                eventos_do_dia.append(evento.vobject_instance.vevent.summary.value)
            except Exception:
                continue

    if eventos_do_dia:
        return "Eventos de hoje: " + ", ".join(eventos_do_dia)
    else:
        return "Você não tem eventos marcados para hoje."
