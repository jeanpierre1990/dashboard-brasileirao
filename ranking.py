import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import base64

# ============================
# CONFIG PÁGINA
# ============================
st.set_page_config(
    page_title="Dashboard Brasileirão",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Dashboard Interativo – Brasileirão Série A")

# ============================
# FUNÇÃO PARA CARREGAR IMAGEM COMO BASE64
# ============================
@st.cache_data
def load_image_as_base64(url):
    try:
        import requests
        response = requests.get(url)
        return base64.b64encode(response.content).decode()
    except:
        return None

# ============================
# CARREGAR DADOS
# ============================
df = pd.read_csv("brasileirao_serie_a.csv")
df["data"] = pd.to_datetime(df["data"], errors="coerce")

# ============================
# TRANSFORMAR EM FORMATO LONGO
# ============================
df_mandante = df[[
    "ano_campeonato", "data", "rodada", "estadio",
    "time_mandante", "tecnico_mandante",
    "gols_mandante", "gols_visitante",
    "chutes_mandante", "chutes_fora_mandante",
    "escanteios_mandante", "faltas_mandante",
    "defesas_mandante", "impedimentos_mandante"
]].rename(columns={
    "time_mandante": "clube",
    "tecnico_mandante": "tecnico",
    "gols_mandante": "gols_pro",
    "gols_visitante": "gols_contra",
    "chutes_mandante": "chutes",
    "chutes_fora_mandante": "chutes_fora",
    "escanteios_mandante": "escanteios",
    "faltas_mandante": "faltas",
    "defesas_mandante": "defesas",
    "impedimentos_mandante": "impedimentos"
})
df_mandante["local"] = "Mandante"

df_visitante = df[[
    "ano_campeonato", "data", "rodada", "estadio",
    "time_visitante", "tecnico_visitante",
    "gols_visitante", "gols_mandante",
    "chutes_visitante", "chutes_fora_visitante",
    "escanteios_visitante", "faltas_visitante",
    "defesas_visitante", "impedimentos_visitante"
]].rename(columns={
    "time_visitante": "clube",
    "tecnico_visitante": "tecnico",
    "gols_visitante": "gols_pro",
    "gols_mandante": "gols_contra",
    "chutes_visitante": "chutes",
    "chutes_fora_visitante": "chutes_fora",
    "escanteios_visitante": "escanteios",
    "faltas_visitante": "faltas",
    "defesas_visitante": "defesas",
    "impedimentos_visitante": "impedimentos"
})
df_visitante["local"] = "Visitante"

df_long = pd.concat([df_mandante, df_visitante], ignore_index=True)

num_cols = ["gols_pro", "gols_contra", "chutes", "chutes_fora",
            "escanteios", "faltas", "defesas", "impedimentos"]
for col in num_cols:
    df_long[col] = pd.to_numeric(df_long[col], errors="coerce")

# ============================
# DICIONÁRIOS (CORRIGIDOS)
# ============================
escudos = {
    "Brasiliense-DF": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Brasiliense_Futebol_Clube.png",
    "Figueirense FC": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Figueirense_FC.png",
    "Chapecoense": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Associa%C3%A7%C3%A3o_Chapecoense_de_Futebol_%28logo%29.png",
    "Grêmio": "https://upload.wikimedia.org/wikipedia/commons/5/5b/Gremio_logo.svg",
    "Santa Cruz": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Santa_Cruz_Futebol_Clube_%28PE%29.png",
    "América-MG": "https://upload.wikimedia.org/wikipedia/commons/3/3c/America_Mineiro_logo.svg",
    "EC Vitória": "https://upload.wikimedia.org/wikipedia/commons/9/9a/EC_Vitoria_logo.svg",
    "Sport Recife": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Sport_Club_do_Recife.png",
    "Guarani": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Guarani_FC_logo.svg",
    "EC Bahia": "https://upload.wikimedia.org/wikipedia/commons/9/90/EC_Bahia_logo.svg",
    "Criciúma EC": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Criciuma_EC.png",
    "Avaí FC": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Avai_FC_logo.svg",
    "Joinville-SC": "https://upload.wikimedia.org/wikipedia/commons/3/3a/JoinvilleEsporteClube.png",
    "Náutico": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Clube_Nautico_Capibaribe.png",
    "Portuguesa": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Associa%C3%A7%C3%A3o_Portuguesa_de_Desportos.png",
    "Cuiabá-MT": "https://upload.wikimedia.org/wikipedia/commons/6/6c/Cuiab%C3%A1_Esporte_Clube_logo.png",
    "Athletico-PR": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Athletico_Paranaense_2019_logo.svg",
    "Atlético-GO": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Atletico_Goianiense_logo.svg",
    "RB Bragantino": "https://upload.wikimedia.org/wikipedia/en/5/5e/RedBullBragantino.png",
    "Goiás": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Goias_EC_logo.svg",
    "Santos": "https://upload.wikimedia.org/wikipedia/commons/3/35/Santos_logo.svg",
    "Ceará SC": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Ceara_SC_logo.svg",
    "Barueri": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Gr%C3%AAmio_Barueri_logo.png",
    "Santo André": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Esporte_Clube_Santo_Andre.png",
    "Ipatinga FC": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Ipatinga_Futebol_Clube.png",
    "CSA": "https://upload.wikimedia.org/wikipedia/commons/4/4e/CSA_logo.svg",
    "América-RN": "https://upload.wikimedia.org/wikipedia/commons/4/4e/America_de_Natal.png"
    # Adicione mais escudos conforme necessário
}

coords_estadios = {
    "Estádio Durival Britto e Silva": {"lat": -25.4483, "lon": -49.2479},
    "Estádio Olímpico Nilton Santos": {"lat": -22.9133, "lon": -43.2942},
    "Estádio Governador Magalhães Pinto": {"lat": -19.8658, "lon": -43.9711},
    "Estádio Jornalista Mário Filho": {"lat": -22.9122, "lon": -43.2302},
    "Estádio Governador Plácido Castelo": {"lat": -3.7931, "lon": -38.5220},
    "Estádio de Hailé Pinheiro": {"lat": -16.6867, "lon": -49.2648},
    "Estádio Alfredo Jaconi": {"lat": -29.1680, "lon": -51.1790},
    "Allianz Parque": {"lat": -23.5273, "lon": -46.6784},
    "Estádio Urbano Caldeira": {"lat": -23.9535, "lon": -46.3336},
    "Estádio Cícero Pompeu de Toledo": {"lat": -23.5980, "lon": -46.7194},
    "Neo Química Arena": {"lat": -23.5453, "lon": -46.4740},
    "Estádio Major Antônio Couto Pereira": {"lat": -25.4050, "lon": -49.2470},
    "Estádio Estadual Jornalista Edgar Augusto Proença": {"lat": -1.3645, "lon": -48.4446},
    "Estádio Moisés Lucarelli": {"lat": -22.9070, "lon": -47.0607},
    "Estádio Raimundo Sampaio": {"lat": -19.8650, "lon": -43.9260},
    "Arena da Baixada": {"lat": -25.4481, "lon": -49.2769},
    "Estádio Municipal Anacleto Campanella": {"lat": -23.6536, "lon": -46.5653},
    "Estádio Beira-Rio": {"lat": -30.0650, "lon": -51.2350},
    "Estádio São Januário": {"lat": -22.8894, "lon": -43.2280},
    "Estádio Elmo Serejo Farias": {"lat": -15.8140, "lon": -47.9130},
    "Estádio Orlando Scarpelli": {"lat": -27.5945, "lon": -48.6035},
    "Estádio Estadual Kléber José de Andrade": {"lat": -20.3183, "lon": -40.2878},
    "Estádio Municipal Paulo Machado de Carvalho": {"lat": -23.5453, "lon": -46.6658},
    "Estádio General Sílvio Raulino de Oliveira": {"lat": -22.5200, "lon": -44.1040},
    "Arena Condá": {"lat": -27.1000, "lon": -52.6150},
    "Arena do Grêmio": {"lat": -29.9730, "lon": -51.1940},
    "Estádio Municipal Radialista Mário Helênio": {"lat": -21.8070, "lon": -43.3720},
    "Estádio Luso Brasileiro": {"lat": -22.8750, "lon": -43.2800},
    "Estádio Nacional de Brasília Mané Garrincha": {"lat": -15.7836, "lon": -47.8992},
    "Estádio Doutor Adhemar de Barros": {"lat": -22.0120, "lon": -47.8910},
    "Arena Pantanal": {"lat": -15.6010, "lon": -56.0970},
    "Estádio José do Rego Maciel": {"lat": -8.0620, "lon": -34.9010},
    "Estádio Manoel Barradas": {"lat": -12.9490, "lon": -38.4350},
    "Estádio Adelmar da Costa Carvalho": {"lat": -8.0628, "lon": -34.9030},
    "Maracanã": {"lat": -22.912, "lon": -43.230}
}

# ============================
# FILTROS GLOBAIS
# ============================
st.sidebar.header("Filtros globais")

anos = sorted(df_long["ano_campeonato"].dropna().unique())
ano = st.sidebar.selectbox("Ano", anos, key="f_ano")

local_sel = st.sidebar.radio("Local", ["Todos", "Mandante", "Visitante"], key="f_local")

clubes = sorted(df_long["clube"].unique())
clubes_sel = st.sidebar.multiselect("Clubes", clubes, key="f_clubes")

tecnicos = sorted(df_long["tecnico"].dropna().unique())
tecnico_sel = st.sidebar.multiselect("Técnicos", tecnicos, key="f_tecnicos")

estadios = sorted(df_long["estadio"].dropna().unique())
estadio_sel = st.sidebar.multiselect("Estádios", estadios, key="f_estadios")

df_f = df_long[df_long["ano_campeonato"] == ano]

if local_sel != "Todos":
    df_f = df_f[df_f["local"] == local_sel]
if clubes_sel:
    df_f = df_f[df_f["clube"].isin(clubes_sel)]
if tecnico_sel:
    df_f = df_f[df_f["tecnico"].isin(tecnico_sel)]
if estadio_sel:
    df_f = df_f[df_f["estadio"].isin(estadio_sel)]

# ============================
# TABS
# ============================
tab_rank, tab_clubes, tab_estadios, tab_tecnicos, tab_timeline, tab_heat = st.tabs(
    ["🏆 Ranking", "🏟️ Clubes", "📍 Estádios", "🧑‍🏫 Técnicos", "📈 Linha do tempo", "🔥 Heatmap"]
)

# ============================
# TAB RANKING - COM ESCUDOS
# ============================
with tab_rank:
    st.subheader("🏆 Ranking de clubes")

    ranking = df_f.groupby("clube").agg(
        jogos=("clube", "count"),
        gols_pro=("gols_pro", "sum"),
        gols_contra=("gols_contra", "sum"),
        chutes=("chutes", "sum"),
        escanteios=("escanteios", "sum"),
        faltas=("faltas", "sum"),
        defesas=("defesas", "sum"),
        impedimentos=("impedimentos", "sum")
    )

    if ranking.empty:
        st.info("Nenhum dado para os filtros atuais.")
    else:
        ranking["saldo_gols"] = ranking["gols_pro"] - ranking["gols_contra"]
        ranking = ranking.sort_values("saldo_gols", ascending=False)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de jogos", int(ranking["jogos"].sum()))
        col2.metric("Total de gols pró", int(ranking["gols_pro"].sum()))
        col3.metric("Total de gols contra", int(ranking["gols_contra"].sum()))

        # DataFrame com escudos
        def create_escudo_column(row):
            clube = row.name
            escudo_url = escudos.get(clube)
            if escudo_url:
                img_b64 = load_image_as_base64(escudo_url)
                if img_b64:
                    return f'<img src="data:image/png;base64,{img_b64}" width="30" height="30"> {clube}'
            return clube

        ranking_display = ranking.copy()
        ranking_display["clube"] = [create_escudo_column(row) for _, row in ranking.iterrows()]
        
        st.markdown(ranking_display[["clube", "jogos", "gols_pro", "gols_contra", "saldo_gols"]].style.background_gradient(cmap="Blues").to_html(), unsafe_allow_html=True)

        st.subheader("Saldo de gols por clube")
        fig_bar = px.bar(
            ranking,
            x=ranking.index,
            y="saldo_gols",
            color="saldo_gols",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Radar mantido igual
        st.subheader("Radar de estatísticas por clube")
        clube_radar = st.selectbox(
            "Selecione um clube",
            ranking.index.tolist(),
            key="rank_radar_clube"
        )
        met_cols = ["gols_pro", "gols_contra", "chutes", "escanteios", "faltas", "defesas", "impedimentos"]
        vals = ranking.loc[clube_radar, met_cols].values
        categorias = met_cols + [met_cols[0]]
        vals = list(vals) + [vals[0]]

        fig_radar = go.Figure(
            data=go.Scatterpolar(
                r=vals,
                theta=categorias,
                fill="toself",
                name=clube_radar
            )
        )
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)

# ============================
# TAB CLUBES - COM ESCUDOS NA COMPARAÇÃO
# ============================
with tab_clubes:
    st.subheader("Comparação entre clubes")

    ranking = df_f.groupby("clube").agg(
        jogos=("clube", "count"),
        gols_pro=("gols_pro", "sum"),
        gols_contra=("gols_contra", "sum"),
        chutes=("chutes", "sum"),
        escanteios=("escanteios", "sum"),
        faltas=("faltas", "sum"),
        defesas=("defesas", "sum"),
        impedimentos=("impedimentos", "sum")
    )

    if ranking.empty:
        st.info("Nenhum dado para os filtros atuais.")
    else:
        ranking["saldo_gols"] = ranking["gols_pro"] - ranking["gols_contra"]
        clubes_disp = ranking.index.tolist()

        c1, c2 = st.columns(2)
        clube_a = c1.selectbox("Clube A", clubes_disp, key="clubes_comp_a")
        clube_b = c2.selectbox("Clube B", clubes_disp, key="clubes_comp_b")

        # Mostrar escudos nos clubes selecionados
        col_img1, col_img2 = st.columns(2)
        escudo_a = escudos.get(clube_a)
        escudo_b = escudos.get(clube_b)
        
        if escudo_a:
            col_img1.image(escudo_a, width=80, caption=clube_a)
        else:
            col_img1.write(f"🏟️ **{clube_a}**")
            
        if escudo_b:
            col_img2.image(escudo_b, width=80, caption=clube_b)
        else:
            col_img2.write(f"🏟️ **{clube_b}**")

        comp = ranking.loc[[clube_a, clube_b], ["gols_pro", "gols_contra", "chutes", "escanteios", "faltas", "defesas", "impedimentos"]]
        comp["saldo_gols"] = comp["gols_pro"] - comp["gols_contra"]