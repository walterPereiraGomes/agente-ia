def get_explicacao_tools():
    return [
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
            "name": "pegar_consumo_veiculo",
            "description": "Retorna o consumo do veículo, quantos quilometros ele faz por litro",
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
            "name": "pegar_preco_atual_gasolina",
            "description": "Retorna o preço atual do litro da gasolina",
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
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_setores",
            "description": "Lista os setores disponíveis no sistema",
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
            "name": "buscar_perfis",
            "description": "Lista os perfis disponíveis no sistema",
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
            "name": "buscar_modulos",
            "description": "Lista os modulos disponíveis no sistema",
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
            "name": "buscar_roles",
            "description": "Lista as roles disponíveis no sistema",
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
            "name": "criar_perfil",
            "description": "Cria um novo perfil com roles e módulos",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "roles": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "modules": {
                        "type": "array",
                        "items": {"type": "object"}
                    }
                },
                "required": ["name", "roles", "modules"]
            }
        }
    }
]