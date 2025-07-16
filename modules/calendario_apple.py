import os
from datetime import date
from caldav import DAVClient
from dotenv import load_dotenv

load_dotenv()

def obter_eventos_do_dia(email: str, senha_app: str):
    url = os.getenv("APPLE_CALENDAR_URL")

    if not url:
        raise Exception("URL do Apple Calendar não encontrada no .env")

    # 🔁 Substitui webcal:// por https://
    url = url.replace("webcal://", "https://")

    try:
        client = DAVClient(url, username=email, password=senha_app)
        principal = client.principal()
        calendars = principal.calendars()

        if not calendars:
            return {"eventos": "Nenhum calendário encontrado."}

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
            return {"eventos": "Eventos de hoje: " + ", ".join(eventos_do_dia)}
        else:
            return {"eventos": "Você não tem eventos marcados para hoje."}
    except Exception as e:
        return {"erro": str(e)}
