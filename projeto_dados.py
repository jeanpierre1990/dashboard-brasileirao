import pandas as pd

caminho = r"C:\Users\HP\Desktop\projeto de dados com panda\brasileirao_serie_a.csv"
df = pd.read_csv(caminho)

# Visão geral
print(df.shape)        # linhas, colunas
print(df.columns)      # nomes das colunas
print(df.head())       # primeiras linhas
print(df.info())       # tipos e nulos

# Converter data para datetime (se ainda não estiver)
df["data"] = pd.to_datetime(df["data"], errors="coerce")

# Garantir que ano_campeonato é numérico
df["ano_campeonato"] = pd.to_numeric(df["ano_campeonato"], errors="coerce")

# Contar nulos por coluna
nulos = df.isna().sum().sort_values(ascending=False)
print(nulos)

# Percentual de nulos
percent_nulos = (df.isna().mean() * 100).sort_values(ascending=False)
print(percent_nulos)

# Estatísticas numéricas gerais
print(df.describe().T)

# Estatísticas por ano
estat_por_ano = df.groupby("ano_campeonato")[[
    "gols_mandante", "gols_visitante",
    "chutes_mandante", "chutes_visitante"
]].mean()

print(estat_por_ano)

df_mandante = df[[
    "ano_campeonato", "data", "rodada",
    "time_mandante", "gols_mandante", "gols_visitante",
    "chutes_mandante", "chutes_fora_mandante",
    "escanteios_mandante", "faltas_mandante"
]].rename(columns={
    "time_mandante": "clube",
    "gols_mandante": "gols_pro",
    "gols_visitante": "gols_contra",
    "chutes_mandante": "chutes",
    "chutes_fora_mandante": "chutes_fora",
    "escanteios_mandante": "escanteios",
    "faltas_mandante": "faltas"
})

df_mandante["mandante_ou_visitante"] = "mandante"

print(df.columns.tolist())
