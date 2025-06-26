TIPOS_REFEICAO = {
    0: "Café da Manhã",
    1: "Almoço", 
    2: "Lanche da Tarde",
    3: "Jantar",
    4: "Ceia"
}

def obter_nome_tipo(tipo):
    return TIPOS_REFEICAO.get(tipo, f"Tipo {tipo}")

def obter_tipos_disponiveis():
    return list(TIPOS_REFEICAO.items())