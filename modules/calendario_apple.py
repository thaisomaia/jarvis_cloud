import caldav
from caldav.elements import dav, cdav
from datetime import datetime, timedelta

APPLE_ID = "thaismaia00@gmail.com"
APPLE_APP_PASSWORD = "qfeh-bjum-oyvb-xbee"

def obter_eventos_proximos(dias=7):
    try:
        client = caldav.DAVClient(
            url="https://caldav.icloud.com/",
            username=APPLE_ID,
            password=APPLE_APP_PASSWORD
        )

        principal = client.principal()
        calendars = principal.calendars()

        if not calendars:
            return "Nenhum calendário encontrado."

        calendario = calendars[0]  # Usa o primeiro por enquanto

        agora = datetime.now()
        futuro = agora + timedelta(days=dias)

        eventos = calendario.date_search(start=agora, end=futuro)

        if not eventos:
            return "Nenhum evento nos próximos dias."

        resposta = "📅 Próximos eventos:\n"
        for evento in eventos:
            evento_data = evento.vobject_instance.vevent.dtstart.value
            evento_titulo = evento.vobject_instance.vevent.summary.value
            resposta += f"- {evento_titulo} em {evento_data}\n"

        return resposta.strip()

    except Exception as e:
        return f"Erro ao buscar eventos: {str(e)}"
