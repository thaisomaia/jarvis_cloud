import requests

def obter_clima(latitude=-23.5505, longitude=-46.6333):  # São Paulo por padrão
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current_weather=true"
        )
        resposta = requests.get(url)
        dados = resposta.json()

        if "current_weather" in dados:
            clima = dados["current_weather"]
            temperatura = clima["temperature"]
            vento = clima["windspeed"]
            condicao = clima.get("weathercode", "indefinida")

            return (
                f"A temperatura atual é {temperatura}°C com ventos de {vento} km/h. "
                f"O código do tempo é {condicao}."
            )
        else:
            return "Não consegui obter os dados do clima no momento."

    except Exception as e:
        return f"Erro ao obter clima: {str(e)}"
