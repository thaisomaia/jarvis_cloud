import os
from datetime import datetime, time, timedelta
from caldav import DAVClient
from dotenv import load_dotenv

load_dotenv()

def obter_eventos_do_dia(email: str, senha_app: str) -> str:
    url = os.getenv("APPLE_CALENDAR_URL")
    if not url:
        raise Exception("URL do Apple Calendar não encontrada no .env")

    client = DAVClient(url, username=email, password=senha_app)
    principal = client.principal()
    calendars = principal.calendars()

    if not calendars:
        return "Nenhum calendário encontrado."

    hoje = datetime.now().date()
    inicio_dia = datetime.combine(hoje, time.min)
    fim_dia = datetime.combine(hoje, time.max)

    eventos_do_dia = []

    for calendario in calendars:
        eventos = calendario.date_search(start=inicio_dia, end=fim_dia)
        for evento in eventos:
            try:
                eventos_do_dia.append(evento.vobject_instance.vevent.summary.value)
            except Exception:
                continue

    if eventos_do_dia:
        return "Eventos de hoje: " + ", ".join(eventos_do_dia)
    else:
        return "Você não tem eventos marcados para hoje."
