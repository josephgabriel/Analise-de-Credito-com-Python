# Análise de Crédito - CP2 Soluções Financeiras

Projeto desenvolvido para classificação automática de eventos relevantes em operações de crédito estruturado (CRI/CRA), com geração de indicadores de risco por CETIP.

## Funcionalidades

- Leitura da base de fatos relevantes em Excel
- Identificação automática de eventos financeiros
- Classificação dos eventos em:
  - Positivo
  - Neutro
  - Negativo
  - Não Classificado
- Cálculo de pontuação por ativo
- Cálculo de índice de risco
- Exportação dos resultados para Excel
- Exibição de métricas de cobertura da classificação

## Estrutura do Projeto

```text
Analise_Credito/
│
├── cp2.py
├── README.md
├── .gitignore
│
└── data/
    ├── Case C2P.xlsx
    └── Resultado.xlsx
```

## Instalação

Clone o repositório:

```bash
git clone "https://github.com/josephgabriel/Analise-de-Credito-com-Python.git"
cd Analise_Credito
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Coloque o arquivo `Case C2P.xlsx` dentro da pasta `data` e execute:

```bash
python cp2.py
```

O arquivo de saída será gerado em:

```text
data/Resultados.xlsx
```

## Tecnologias Utilizadas

- Python
- Pandas
- OpenPyXL

## Autor

José Gabriel Soares dos Santos
