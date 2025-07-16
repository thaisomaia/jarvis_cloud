import os
from datetime import datetime, timedelta
from caldav import DAVClient
from dotenv import load_dotenv

load_dotenv()

def obter_eventos_do_dia(email: str, senha_app: str):
    url = os.getenv("APPLE_CALENDAR_URL")

    if not url:
        return {"erro": "URL do Apple Calendar não encontrada no .env"}

    print(f"Conectando com: {url}, usuário: {email}")

    try:
        client = DAVClient(url, username=email, password=senha_app)
        principal = client.principal()
        calendars = principal.calendars()
    except Exception as e:
        return {"erro": f"Erro ao conectar: {e}"}

    if not calendars:
        return {"erro": "Nenhum calendário encontrado."}

    hoje = datetime.now()
    inicio = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
    fim = hoje.replace(hour=23, minute=59, second=59, microsecond=999999)

    print(f"Procurando eventos entre: {inicio.isoformat()} e {fim.isoformat()}")

    eventos_do_dia = []

    for calendario in calendars:
        try:
            eventos = calendario.date_search(inicio, fim)
        except Exception as e:
            print(f"Erro ao buscar em {calendario.name}: {e}")
            continue

        for evento in eventos:
            try:
                vobj = evento.vobject_instance
                if vobj and hasattr(vobj, 'vevent'):
                    eventos_do_dia.append(vobj.vevent.summary.value)
            except Exception as e:
                print("Erro ao ler evento:", e)

    if eventos_do_dia:
        return {"eventos": "Eventos de hoje: " + ", ".join(eventos_do_dia)}
    else:
        return {"eventos": "Você não tem eventos marcados para hoje."}
