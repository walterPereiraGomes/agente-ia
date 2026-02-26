from datetime import datetime


def pegar_hora():
    print("pegar_hora foi chamado")
    return f"Horário atual {datetime.now().strftime('%H:%M')}"



def calcular(expressao: str):
    try:
        return str(eval(expressao))
    except:
        return "Erro ao calcular."

def criar_arquivo(nome: str, conteudo: str):
    with open(nome, "w") as f:
        f.write(conteudo)
    return f"Arquivo {nome} criado com sucesso."

def pegar_consumo_veiculo():
    return 14

def pegar_preco_atual_gasolina():
    return 6.80