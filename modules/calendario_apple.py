import os
from datetime import date
from caldav import DAVClient
from dotenv import load_dotenv

load_dotenv()

def obter_eventos_do_dia(email, senha_app):
    try:
        url = os.getenv("APPLE_CALENDAR_URL")
        if not url:
            return {"erro": "URL do Apple Calendar não encontrada no .env"}

        print(f"Conectando com: {url}, usuário: {email}")

        client = DAVClient(url, username=email, password=senha_app)
        principal = client.principal()
        calendars = principal.calendars()

        if not calendars:
            print("Nenhum calendário retornado.")
            return {"eventos": "Nenhum calendário encontrado."}

        hoje = date.today()
        eventos_do_dia = []

        print(f"Procurando eventos na data: {hoje}")

        for calendario in calendars:
            eventos = calendario.date_search(hoje)
            print(f"[{calendario.name}] - {len(eventos)} eventos encontrados")
            for evento in eventos:
                try:
                    resumo = evento.vobject_instance.vevent.summary.value
                    print(f"→ Evento: {resumo}")
                    eventos_do_dia.append(resumo)
                except Exception as e:
                    print(f"Erro ao ler evento: {e}")
                    continue

        if eventos_do_dia:
            return {"eventos": "Eventos de hoje: " + ", ".join(eventos_do_dia)}
        else:
            return {"eventos": "Você não tem eventos marcados para hoje."}
    except Exception as e:
        print(f"Erro geral: {e}")
        return {"erro": str(e)}
