"""
Regras do recusador de chamadas. Edite à vontade.

Como o número é comparado:
- Espaços, traços, parênteses e o "+" são ignorados (o "*" e o "#" ficam).
- O código do país (55) e o zero de longa distância na frente são
  descartados, então "+55 11 98765-4321", "011 98765-4321" e "11987654321"
  são o mesmo número. As regras abaixo passam pela mesma limpeza, então
  pode escrevê-las do jeito que aparecem no celular.
- PREFIXOS: recusa se o número começar com o prefixo.
- NUMEROS: recusa se o número for exatamente igual.
"""

# Prefixos que a Anatel reserva para telemarketing ativo. As operadoras
# (e outras empresas) são obrigadas a usá-los para ligar oferecendo
# produtos.
PREFIXOS = {
    "Telemarketing (0303)": ["0303"],
    "Telemarketing (0304)": ["0304"],
}

# Números conhecidos das operadoras. Confira e complete com os que ligam
# para você (veja no histórico do celular e copie aqui).
NUMEROS = {
    "Vivo": ["1058", "*8486", "10315"],
    "Claro": ["1052", "*525", "10621"],
    "TIM": ["1056", "*144", "10341"],
    "Oi": ["1057", "10331"],
}

# Arquivo de texto opcional, um número por linha (linhas com # são
# comentários). Bom para ir colando números novos sem mexer no código.
ARQUIVO_BLOQUEADOS = "bloqueados.txt"

# Números que NUNCA devem ser recusados, mesmo que caiam numa regra acima.
PERMITIDOS = [
    # "11999998888",
]

# Intervalo entre as checagens do celular, em segundos.
INTERVALO = 0.4

# Arquivo onde cada chamada recusada é registrada (CSV).
ARQUIVO_LOG = "recusadas.csv"
