import os
from datetime import datetime, timedelta
from caldav import DAVClient
from dotenv import load_dotenv

load_dotenv()

def obter_eventos_do_dia(email, senha_app):
    url = os.getenv("APPLE_CALENDAR_URL")

    if not url:
        return {"erro": "URL do Apple Calendar não encontrada no .env"}

    try:
        client = DAVClient(
            url,
            username=email,
            password=senha_app
        )
        principal = client.principal()
        calendars = principal.calendars()

        if not calendars:
            return {"eventos": "Nenhum calendário encontrado."}

        hoje = datetime.utcnow()
        inicio = datetime(hoje.year, hoje.month, hoje.day)
        fim = inicio + timedelta(days=1)

        eventos_do_dia = []

        for calendario in calendars:
            eventos = calendario.date_search(inicio, fim)
            for evento in eventos:
                try:
                    eventos_do_dia.append(evento.vobject_instance.vevent.summary.value)
                except Exception:
                    continue

        if eventos_do_dia:
            return {"eventos": "Eventos de hoje: " + ", ".join(eventos_do_dia)}
        else:
            return {"eventos": "Você não tem eventos marcados para hoje."}

    except Exception as e:
        return {"erro": str(e)}
