import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

historico = [
    {"role": "system", "content": "Você é um agente util, focado em direito societário, um advogado jurídico de elite"},
    {"role": "system", "content": "Responda somente assuntos jurídicos e pegue dados pessoais caso o usuário informe, mas seu foco é realmente somente ajudar em questões jurídicas"},
    {"role": "system", "content": "se recuse a responder questões pessoais ou de outros assuntos que nao forem jurídicos"}
]

def agente(pergunta):
    historico.append({"role": "user", "content": pergunta})
    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",

        messages=historico
    )
    historico.append({"role": "assistant", "content": resposta.choices[0].message.content})
    return resposta.choices[0].message.content


print("🤖 Agente iniciado! Digite 'sair' para encerrar.\n")


while True:
    pergunta = input("Você: ")

    if pergunta.lower() == "sair":
        break

    resposta = agente(pergunta)
    print("Agente:", resposta, "\n")