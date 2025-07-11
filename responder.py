import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def responder_com_gpt(pergunta: str) -> str:
    try:
        resposta = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente pessoal inteligente."},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao consultar GPT: {e}")
        return "Desculpe, não consegui responder agora."
