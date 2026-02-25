import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from tools import calcular
from tools import criar_arquivo
from tools import pegar_hora

load_dotenv()

tools = [
    {
        "type": "function",
        "function": {
            "name": "pegar_hora",
            "description": "Retorna a hora atual do sistema",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular",
            "description": "Calcula uma expressão matemática",
            "parameters": {
                "type": "object",
                "properties": {
                    "expressao": {
                        "type": "string",
                        "description": "Expressão matemática ex: 2+2"
                    }
                },
                "required": ["expressao"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "criar_arquivo",
            "description": "Cria um arquivo no sistema",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {
                        "type": "string",
                        "description": "Nome do arquivo"
                    },
                    "conteudo": {
                        "type": "string",
                        "description": "Conteúdo do arquivo"
                    }
                },
                "required": ["nome", "conteudo"]
            }
        }
    }
]

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

st.title("🤖 Sou a CidinhIA, sua assistente jurídica")


def adicionarNoHistorico(mensagem):
    if "historico" not in st.session_state:
        st.session_state.historico = []
    st.session_state.historico.append(mensagem)


# Memória inicial da conversa
if "historico" not in st.session_state:
    adicionarNoHistorico({
    "role": "system",
    "content": """
        Você é cidinhIA.
        Sempre use a ferramenta calcular quando algum cálculo for necessária. 
        Nunca faça cálculos por conta própria.
        Sempre que usar uma ferramenta, responda APENAS com o resultado retornado, de uma maneira que o usuário entenda.
        Nunca explique que usou ferramenta.
        Nunca mencione o nome da função.
        Nunca descreva o processo.
    """
    })


# Mostrar mensagens antigas
for msg in st.session_state.historico:
    if msg["role"] != "system" and msg["role"] != "tool":
        with st.chat_message(msg["role"]):
            if "content" in msg and msg["content"]:
                st.write(msg["content"])


# Campo de input
if prompt := st.chat_input("Digite sua mensagem..."):

    # Mostra mensagem do usuário
    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.historico.append({
        "role": "user",
        "content": prompt
    })

    MAX_ITER = 5
    iteracao = 0

    while iteracao < MAX_ITER:
        iteracao += 1

        print(st.session_state.historico)

        resposta = client.chat.completions.create(
            model="qwen3:4b",
            messages=st.session_state.historico,
            tools=tools,
        )

        mensagem = resposta.choices[0].message

        # 🔥 montar mensagem corretamente
        msg_dict = {
            "role": mensagem.role
        }

        if mensagem.content:
            msg_dict["content"] = mensagem.content

        if mensagem.tool_calls:
            msg_dict["tool_calls"] = mensagem.tool_calls

        adicionarNoHistorico(msg_dict)

        # Se NÃO pediu tool → resposta final
        if not mensagem.tool_calls:
            print('SAIU DO LOOP')
            texto = mensagem.content
            break

        # Se pediu tool → executar
        for tool_call in mensagem.tool_calls:
            nome_funcao = tool_call.function.name

            # ⚠️ às vezes arguments vem como "null"
            argumentos = {}
            if tool_call.function.arguments and tool_call.function.arguments != "null":
                argumentos = json.loads(tool_call.function.arguments)

            if nome_funcao == "pegar_hora":
                print("========= TOOL DE PEGAR HORA CHAMADA ================")
                resultado = pegar_hora()
                print("Resultado:")
                print(resultado)
                print("======================================================")

            elif nome_funcao == "calcular":
                print("========= TOOL DE CÁLCULO FOI CHAMADA ================")
                print(argumentos["expressao"])
                resultado = calcular(argumentos["expressao"])
                print("Resultado:")
                print(resultado)
                print("========================================================")

            elif nome_funcao == "criar_arquivo":
                resultado = criar_arquivo(
                    argumentos["nome"],
                    argumentos["conteudo"]
                )

            adicionarNoHistorico({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(resultado)
            })
    # Mostra resposta
    with st.chat_message("assistant"):
        st.write(texto)