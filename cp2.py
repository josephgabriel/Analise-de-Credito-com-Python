import pandas as pd
import unicodedata

ARQUIVO = "data/Case C2P.xlsx"

fatos_df = pd.read_excel(
    ARQUIVO,
    sheet_name= "Fatos Relevantes"
    )

total_eventos = len(fatos_df)

classificacao_eventos = {
    "Waiver de Não Pagamento de Juros/Amortização": "Negativo",
    "Carência de Pagamento de Juros/Amortização": "Negativo",
    "Aditamento com repactuação do fluxo de pagamento": "Negativo",
    "Waiver de Descumprimento de Índices Financeiros": "Negativo",
    "Recomposição de Fundo de reserva/Liquidez": "Positivo",
    "Descumprimento de Índice de Cobertura": "Negativo",
    "Aprovado declaração de vencimento antecipado": "Negativo",
    "Waiver para não declarar vencimento antecipado": "Neutro",
    "Descumprimento de razão de garantia": "Negativo",
    "Pedido de Recuperação Judicial/Extrajudicial": "Negativo",
    "Resgate/Recompra Antecipado Facultativo": "Positivo",
    "Resgate/Recompra Antecipado Obrigatório": "Positivo",
    "Waiver de entrega de demonstração financeira": "Negativo",
    "Prorrogação de vencimento": "Negativo",
    "Rebaixamento de Rating de Agência de Risco": "Negativo",
    "Melhora de Rating de Agência de Risco": "Positivo",
    "Manutenção de Rating de Agência de Risco": "Neutro",
    "Prestação de Garantias Adicionais": "Positivo",
    "Aprovação das demonstrações financeiras do patrimônio separado": "Positivo",
    "Não Classificado": "Não Classificado"
}

pesos = {
    "Positivo": 1,
    "Neutro": 0,
    "Negativo": -1,
    "Não Classificado": 0
}

def normalizar_texto(texto):
    texto = str(texto).lower()

    texto = unicodedata.normalize('NFKD', texto)

    texto = ''.join(
        c for c in texto
        if not unicodedata.combining(c)
    )

    return texto

def identificar_evento(texto):

    if pd.isna(texto):
        return "Não Classificado"

    texto = normalizar_texto(texto)

    # RECUPERAÇÃO JUDICIAL

    if any(x in texto for x in [
        "recuperacao judicial",
        "recuperacao extrajudicial"
    ]):
        return "Pedido de Recuperação Judicial/Extrajudicial"

    # REBAIXAMENTO DE RATING

    if "rating" in texto:
     if any(x in texto for x in [
         "rebaixado",
         "downgrade"
     ]):
         return "Rebaixamento de Rating de Agência de Risco"
 
     if any(x in texto for x in [
         "elevado",
         "upgrade"
     ]):
         return "Melhora de Rating de Agência de Risco"
 
     if any(x in texto for x in [
         "mantido",
         "afirmado"
     ]):
         return "Manutenção de Rating de Agência de Risco"

    # CARÊNCIA

    if any(x in texto for x in [
        "carencia"
    ]):
        return "Carência de Pagamento de Juros/Amortização"

    # PRORROGAÇÃO DE VENCIMENTO

    if any(x in texto for x in [
        "prorrogacao",
        "prorrogado o vencimento",
        "extensao de prazo"
    ]):
        return "Prorrogação de vencimento"

    # WAIVER NÃO PAGAMENTO

    if (
        "waiver" in texto
        and any(x in texto for x in [
            "nao pagamento",
            "juros",
            "amortizacao"
        ])
    ):
        return "Waiver de Não Pagamento de Juros/Amortização"

    # WAIVER ÍNDICES FINANCEIROS

    if (
        "waiver" in texto
        and any(x in texto for x in [
            "indice financeiro",
            "covenant",
            "indices financeiros"
        ])
    ):
        return "Waiver de Descumprimento de Índices Financeiros"

    # WAIVER VENCIMENTO ANTECIPADO

    if (
        "waiver" in texto
        and any(x in texto for x in [
            "vencimento antecipado",
            "declaracao de vencimento antecipado"
        ])
    ):
        return "Waiver para não declarar vencimento antecipado"

    # DESCUMPRIMENTO DE COBERTURA

    if any(x in texto for x in [
        "descumprimento de indice de cobertura",
        "desenquadramento do indice de cobertura"
    ]):
        return "Descumprimento de Índice de Cobertura"
    
    # DESCUMPRIMENTO DE GARANTIA

    if any(x in texto for x in [
        "descumprimento de garantia",
        "descumprimento da garantia",
        "razao de garantia"
    ]):
        return "Descumprimento de razão de garantia"

    # GARANTIAS ADICIONAIS

    if any(x in texto for x in [
        "garantia adicional",
        "garantias adicionais",
        "cessao fiduciaria",
        "reforço de garantia",
        "reforco de garantia"
    ]):
        return "Prestação de Garantias Adicionais"

    # RECOMPOSIÇÃO DE FUNDO

    if any(x in texto for x in [
        "recomposicao do fundo de reserva",
        "recomposicao de fundo de liquidez"
    ]):
        return "Recomposição de Fundo de reserva/Liquidez"

    # RESGATE FACULTATIVO

    if any(x in texto for x in [
        "resgate antecipado facultativo",
        "recompra antecipada facultativa"
    ]):
        return "Resgate/Recompra Antecipado Facultativo"

    # RESGATE OBRIGATÓRIO

    if any(x in texto for x in [
        "resgate antecipado obrigatorio",
        "recompra antecipada obrigatoria"
    ]):
        return "Resgate/Recompra Antecipado Obrigatório"

    # ADITAMENTO / REPACTUAÇÃO

    if any(x in texto for x in [
       "aditamento",
       "alteracao do cronograma de amortizacao",
       "alteracao de vencimento",
       "repactuacao",
       "renegociacao"

    ]):
        return "Aditamento com repactuação do fluxo de pagamento"

    # APROVAÇÃO DAS DEMONSTRAÇÕES

    if any(x in texto for x in [
        "aprovacao das demonstracoes financeiras",
        "aprovacao das demonstracoes",
        "adimplente",
        "suficiencia de lastro",
        "sem pendencias"
    ]):
        return "Aprovação das demonstrações financeiras do patrimônio separado"

    # ENTREGA DE DFs

    if (
        "waiver" in texto
        and any(x in texto for x in [
            "demonstracao financeira",
            "nao pagamento"
        ])
    ):
        return "Waiver de entrega de demonstração financeira"

    # VENCIMENTO ANTECIPADO

    if any(x in texto for x in [
        "vencimento antecipado",
        "declarado vencimento antecipado"
    ]):
        return "Aprovado declaração de vencimento antecipado"
    
   # EVENTO INFORMATIVO

    if any(x in texto for x in [
        "assembleia",
        "convocacao",
        "comunicado ao mercado",
        "fato relevante"
    ]):
       return "Evento Informativo"

    # ERROS / NÃO CLASSIFICADOS

    if any(x in texto for x in [
        "erro ao processar",
        "documento vazio",
        "validationexception"
    ]):
        return "Não Classificado"

    return "Não Classificado"

fatos_df["Evento"] = fatos_df["Resumo"].apply(
    identificar_evento
)

fatos_df["Classificacao"] = (
    fatos_df["Evento"]
    .map(classificacao_eventos)
)

fatos_df["Peso"] = (
    fatos_df["Classificacao"]
    .map(pesos)
)

resultado = (
    fatos_df.pivot_table(
        index = "CETIP",
        columns="Classificacao",
        values="Peso",
        aggfunc="count",
        fill_value=0
    )
    .reset_index()
)

for coluna in ["Positivo", "Neutro", "Negativo", "Não Classificado"]:
    if coluna not in resultado.columns:
        resultado[coluna] = 0

resultado["QtdEventos"] = (
    resultado["Positivo"] + resultado["Neutro"] + resultado["Negativo"] + resultado["Não Classificado"]
)

# adicional de pontuação

resultado["Pontuacao"] = (
    resultado["Positivo"] * 1 + resultado["Neutro"] * 0 + resultado["Negativo"] * (-1)
)

resultado["IndiceRisco"] = (
    resultado["Negativo"] / resultado["QtdEventos"].replace(0, 1)
)
# exportação

resultado.to_excel(
    "data/Resultados.xlsx",
    index=False
)

# Resumo no terminal

resumo = resultado[["Positivo", "Neutro", "Negativo"]].sum()

nao_classificados = (
    fatos_df["Evento"] == "Não Classificado"
).sum()

nao_classificados_df = fatos_df[
    fatos_df["Evento"] == "Não Classificado"
]

classificados = total_eventos - nao_classificados

cobertura = (classificados / total_eventos) * 100

print("\n" + "=" * 70)
print("ANÁLISE DE EVENTOS DE CRÉDITO - C2P")
print("=" * 70)

print(f"\nArquivo gerado: Resultados.xlsx")

print("\nRESUMO GERAL")
print("-" * 70)
print(f"Eventos Positivos ........: {resumo['Positivo']}")
print(f"Eventos Neutros .........: {resumo['Neutro']}")
print(f"Eventos Negativos .......: {resumo['Negativo']}")
print(f"Eventos Não Classificados: {nao_classificados}")

print("\nCOBERTURA DA CLASSIFICAÇÃO")
print("-" * 70)
print(f"Eventos Totais ..........: {total_eventos}")
print(f"Eventos Classificados ...: {classificados}")
print(f"Cobertura ...............: {cobertura:.2f}%")

print("\nTOP 10 CETIPs COM MAIOR RISCO")
print("-" * 70)

print(
    resultado
    .sort_values("Pontuacao")
    [
        [
            "CETIP",
            "Negativo",
            "Positivo",
            "Pontuacao",
            "IndiceRisco"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\nPRINCIPAIS EVENTOS NÃO CLASSIFICADOS")
print("-" * 70)

print(
    nao_classificados_df["Resumo"]
    .str.split(":")
    .str[0]
    .value_counts()
    .head(10)
    .to_string()
)

print("\nEXEMPLOS DE EVENTOS NÃO CLASSIFICADOS")
print("-" * 70)

for evento in nao_classificados_df["Resumo"].head(5):
    print(f"• {evento[:120]}...")

print("\n" + "=" * 70)
print("PROCESSAMENTO FINALIZADO COM SUCESSO")
print("=" * 70)