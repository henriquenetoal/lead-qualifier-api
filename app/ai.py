import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

def qualify_lead(notes: str) -> dict:
    prompt = f"""Analise as notas de venda abaixo e diga qual a chance desse lead fechar negócio.

Notas: {notes}

Dê uma nota de 1 a 10 (1 = quase certo que não vai fechar, 10 = praticamente fechado) e escreva uma frase curta explicando o porquê da nota, baseado só no que está escrito nas notas.

Responda só com o JSON, nada de texto antes ou depois, nesse formato: {{"score": 8, "summary": "explicação aqui"}}"""

    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    data = json.loads(raw_text)
    return data