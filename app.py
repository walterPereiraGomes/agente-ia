import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from tools import calcular
from tools import criar_arquivo
from tools import pegar_hora
from tools import pegar_consumo_veiculo
from tools import pegar_preco_atual_gasolina
from explicacao_tools import get_explicacao_tools

from mcp_client import call_mcp_tool


load_dotenv()

# tenho uma viagem de 400km pra fazer, geralmente viajo a 80km/h, se eu sair de casa agora, que horas chego ao meu destino, e quanto gasto?

tools = get_explicacao_tools()

servidor = "https://api.groq.com/openai/v1"
key=os.getenv("GROQ_API_KEY")
modelo="openai/gpt-oss-120b"

client = OpenAI(
    api_key=key,
    base_url=servidor
)

st.title("🧃 Sou Dollynho, seu assistente IA")

prompt_inicial = {
    "role": "system",
    "content": """
        Você é o Dollynho.
        Sempre use a ferramenta calcular quando algum cálculo for necessária. 
        Nunca faça cálculos por conta própria.
        Sempre que usar uma ferramenta, responda APENAS com o resultado retornado, de uma maneira que o usuário entenda.
        Nunca explique que usou ferramenta.
        Nunca mencione o nome da função.
        Nunca descreva o processo.
        Sempre que o usuário quiser criar um perfil, devemos buscar todas as roles e todos os módulos para conseguir montar a requisição de criar_perfil com os dados vindos das apis.
        Se atente para nao chamar o método de criar perfil duas vezes.
    """
    }

def adicionarNoHistorico(mensagem, onde_add="ambos"):
    if "historico" not in st.session_state:
        st.session_state.historico = []
    if "historico_ui" not in st.session_state:
        st.session_state.historico_ui = []

    if len(st.session_state.historico) >= 500 and (onde_add == "ambos" or onde_add == "chat"):
        pedido_resumo = {
            "role": "system",
            "content": "Resuma a conversa acima de forma curta e objetiva, mantendo apenas informações importantes."
        }
        st.session_state.historico.append(pedido_resumo)
        resposta_resumo = client.chat.completions.create(
            model=modelo,
            messages=st.session_state.historico,
            tools=tools,
        )

        st.session_state.historico = []
        st.session_state.historico.append(prompt_inicial)
        mensagem = {
            "role": "system",
            "content": resposta_resumo.choices[0].message.content or ""
        }

    if onde_add in ("chat", "ambos"):
        st.session_state.historico.append(mensagem)
    if onde_add in ("ui", "ambos") and mensagem["role"] not in ["system", "tool"]:
        st.session_state.historico_ui.append(mensagem)


# Memória inicial da conversa
if "historico" not in st.session_state:
    adicionarNoHistorico(prompt_inicial)


# Mostrar mensagens antigas
for msg in st.session_state.historico_ui:
    if msg["role"] != "system" and msg["role"] != "tool":
        with st.chat_message(msg["role"]):
            if "content" in msg and msg["content"] and msg["content"] != "":
                st.write(msg["content"])


# Campo de input
if prompt := st.chat_input("Digite sua mensagem..."):

    # Mostra mensagem do usuário
    with st.chat_message("user"):
        st.write(prompt)

    adicionarNoHistorico({
        "role": "user",
        "content": prompt
    })

    MAX_ITER = 10
    iteracao = 0

    print("==== PERGUNTA DO USUÁRIO =======")
    print(prompt)
    print("=================================")

    while iteracao < MAX_ITER:
        iteracao += 1

        resposta = client.chat.completions.create(
            model=modelo,
            messages=st.session_state.historico,
            tools=tools,
        )

        mensagem = resposta.choices[0].message

        # 🔥 montar mensagem corretamente
        msg_dict = {
            "role": mensagem.role,
            "content": mensagem.content or ""
        }

        if mensagem.tool_calls:
            msg_dict["tool_calls"] = mensagem.tool_calls

        adicionarNoHistorico(msg_dict, "chat")

        # Se NÃO pediu tool → resposta final
        if not mensagem.tool_calls:
            adicionarNoHistorico(msg_dict, "ui")
            print('SAIU DO LOOP - DEVOLVENDO RESPOSTA AO USUÁRIO')
            print(f"Resposta final: {mensagem.content}")
            texto = mensagem.content
            # print(st.session_state.historico_ui)
            break

        # Se pediu tool → executar
        for tool_call in mensagem.tool_calls:
            nome_funcao = tool_call.function.name

            argumentos = {}
            if tool_call.function.arguments and tool_call.function.arguments != "null":
                argumentos = json.loads(tool_call.function.arguments)

            if nome_funcao == "pegar_hora":
                print("========= TOOL DE PEGAR HORA CHAMADA ================")
                resultado = pegar_hora()
                print(f"Resultado: {resultado}")
                print("======================================================")

            if nome_funcao == "pegar_consumo_veiculo":
                print("========= TOOL DE PEGAR CONSUMO DO VEÍCULO CHAMADA ================")
                resultado = f"O carro faz {pegar_consumo_veiculo()}km/l"
                print("Resultado:")
                print(resultado)
                print("======================================================")

            if nome_funcao == "pegar_preco_atual_gasolina":
                print("========= TOOL DE PEGAR PRECO ATUAL GASOLINA CHAMADA ================")
                resultado = f"preço atual da gasoline é de R${pegar_preco_atual_gasolina()}"
                print("Resultado:")
                print(resultado)
                print("======================================================")

            elif nome_funcao == "calcular":
                print("========= TOOL DE CÁLCULO FOI CHAMADA ================")
                print(f"Expressão utilizada: {argumentos["expressao"]}")
                resultado = calcular(argumentos["expressao"])
                print(f"Resultado: {resultado}")
                print("========================================================")

            elif nome_funcao == "criar_arquivo":
                resultado = criar_arquivo(
                    argumentos["nome"],
                    argumentos["conteudo"]
                )
            elif nome_funcao == "buscar_setores":
                print("========= TOOL MCP buscar_setores CHAMADA ================")

                resultado_mcp = call_mcp_tool("listar_setores", argumentos)
                resultado = resultado_mcp.content
                
                print("Resultado MCP:")
                print(resultado)
                print("===========================================================")

            elif nome_funcao == "buscar_perfis":
                print("========= TOOL MCP buscar_perfis CHAMADA ================")

                resultado_mcp = call_mcp_tool("listar_perfis", argumentos)
                resultado = resultado_mcp.content
                
                print("Resultado MCP:")
                print(resultado)
                print("===========================================================")

            elif nome_funcao == "buscar_modulos":
                print("========= TOOL MCP buscar_modulos CHAMADA ================")

                resultado_mcp = call_mcp_tool("listar_modulos", argumentos)
                resultado = resultado_mcp.content
                
                print("Resultado MCP:")
                print(resultado)
                print("===========================================================")
            elif nome_funcao == "buscar_roles":
                print("========= TOOL MCP buscar_roles CHAMADA ================")

                resultado_mcp = call_mcp_tool("listar_roles", argumentos)
                resultado = resultado_mcp.content
                
                print("Resultado MCP:")
                print(resultado)
                print("===========================================================")

            elif nome_funcao == "criar_perfil":
                print("========= TOOL MCP criar_perfil CHAMADA ================")
                # crie um perfil com o nome teste-mcp, com acesso a todas as roles e ao modulo Regularização Fundiária
                resultado_mcp = call_mcp_tool("criar_perfil", argumentos)
                resultado = resultado_mcp.content
                
                print("Resultado MCP:")
                print(resultado)
                print("===========================================================")

            adicionarNoHistorico({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(resultado)
            })
    # Mostra resposta
    with st.chat_message("assistant"):
        st.write(texto or "")