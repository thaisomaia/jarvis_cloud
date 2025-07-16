from datetime import date
from caldav import DAVClient

def obter_eventos_do_dia(email, senha_app):
    url = "https://caldav.icloud.com/"

    client = DAVClient(url, username=email, password=senha_app)
    principal = client.principal()
    calendars = principal.calendars()

    if not calendars:
        return "Nenhum calendário encontrado."

    hoje = date.today()
    eventos_do_dia = []

    for calendario in calendars:
        try:
            eventos = calendario.date_search(hoje)
            for evento in eventos:
                try:
                    eventos_do_dia.append(evento.vobject_instance.vevent.summary.value)
                except Exception:
                    continue
        except Exception:
            continue

    if eventos_do_dia:
        return "Eventos de hoje: " + ", ".join(eventos_do_dia)
    else:
        return "Você não tem eventos marcados para hoje."
