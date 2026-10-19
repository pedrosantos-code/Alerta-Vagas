from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Alerta de Vagas & Analytics",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --page-padding: clamp(0.75rem, 2vw, 1.5rem);
            --card-padding: clamp(0.75rem, 2vw, 1.25rem);
        }

        .block-container {
            padding-top: 1rem !important;
            padding-left: var(--page-padding) !important;
            padding-right: var(--page-padding) !important;
            max-width: 100% !important;
        }

        div[data-testid="stMetricContainer"] {
            min-width: 0;
        }

        div[data-testid="stMetricValue"] {
            font-size: clamp(1.1rem, 2vw, 1.8rem) !important;
            white-space: normal !important;
        }

        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
            padding: 0.5rem 0.1rem !important;
        }

        .stDataFrame {
            overflow-x: auto;
        }

        @media (max-width: 768px) {
            .block-container {
                padding-top: 0.5rem !important;
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
            }

            h1 {
                font-size: clamp(1.7rem, 5vw, 2.4rem) !important;
            }

            h2, h3 {
                font-size: clamp(1.1rem, 4vw, 1.6rem) !important;
            }

            [data-testid="stSidebar"] {
                width: min(100vw, 18rem) !important;
            }

            div[data-testid="stHorizontalBlock"] {
                display: block !important;
            }

            div[data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                max-width: 100% !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💼 Alerta de Vagas & Analytics")
st.markdown(
    "Filtra, analisa e monitoriza as melhores oportunidades com disparo de"
    " alertas por e-mail."
)


# --- CARREGAR DADOS ---
@st.cache_data
def carregar_vagas():
  return pd.read_csv("data/Cleaned_DS_Jobs.csv")


try:
  df_vagas = carregar_vagas()
except Exception as e:
  st.error(
      "Não foi possível carregar o ficheiro 'data/Cleaned_DS_Jobs.csv'."
      f" Detalhe técnico: {e}"
  )
  st.stop()


# --- BARRA LATERAL SIMPLIFICADA ---
st.sidebar.header("🔍 Filtros & Preferências")

termo_busca = st.sidebar.text_input(
    "Cargo ou Palavra-Chave",
    key="termo_busca",
    placeholder="Ex: Data Scientist...",
)

# Identificação segura das colunas do dataset
col_titulo = "Job Title" if "Job Title" in df_vagas.columns else df_vagas.columns[0]
col_empresa = (
    "Company Name" if "Company Name" in df_vagas.columns else df_vagas.columns[1]
)
col_local = "Location" if "Location" in df_vagas.columns else df_vagas.columns[2]
col_desc = (
    "Job Description"
    if "Job Description" in df_vagas.columns
    else df_vagas.columns[-1]
)
col_estado = "job_state" if "job_state" in df_vagas.columns else None

# Filtro multi-seleção de Empresas
if col_empresa in df_vagas.columns:
  empresas_disponiveis = sorted(df_vagas[col_empresa].dropna().unique())
  empresas_selecionadas = st.sidebar.multiselect(
      "Empresas", options=empresas_disponiveis, key="empresas"
  )
else:
  empresas_selecionadas = []

if col_estado in df_vagas.columns:
  locais_disponiveis = sorted(
      df_vagas[col_estado].dropna().astype(str).str.strip().str.upper().unique()
  )
elif col_local in df_vagas.columns:
  locais_disponiveis = sorted(
      df_vagas[col_local]
      .dropna()
      .astype(str)
      .str.split(",")
      .str[-1]
      .str.strip()
      .str.upper()
      .unique()
  )
else:
  locais_disponiveis = []

local_selecionado = st.sidebar.multiselect(
    "Localização (estado ou cidade)",
    options=locais_disponiveis,
    key="localizacao",
)

if "seniority" in df_vagas.columns:
  senioridades = sorted(
      {
          str(v).strip().lower()
          for v in df_vagas["seniority"].dropna().astype(str).unique()
          if str(v).strip().lower() != "na"
      }
  )
  senioridade_disponivel = ["Todos"] + senioridades
  senioridade_selecionada = st.sidebar.selectbox(
      "Nível de experiência",
      senioridade_disponivel,
      index=0,
      key="senioridade",
  )
else:
  senioridade_selecionada = "Todos"

st.sidebar.divider()
st.sidebar.subheader("🎯 Stack Tecnológico")
skills_usuario = st.sidebar.multiselect(
    "Competências dominadas:",
    ["Python", "SQL", "Pandas", "Machine Learning", "AWS", "Tableau", "Spark"],
    default=["Python", "SQL"],
    key="skills_usuario",
)

if st.sidebar.button("Limpar filtros", use_container_width=True):
  for key in [
      "termo_busca",
      "empresas",
      "localizacao",
      "senioridade",
      "skills_usuario",
  ]:
    st.session_state.pop(key, None)
  st.rerun()


# --- FILTRAGEM E MATCH ---
df_filtrado = df_vagas.copy()

if termo_busca:
  df_filtrado = df_filtrado[
      df_filtrado[col_titulo]
      .astype(str)
      .str.contains(termo_busca, case=False, na=False)
  ]

if empresas_selecionadas:
  df_filtrado = df_filtrado[df_filtrado[col_empresa].isin(empresas_selecionadas)]

if local_selecionado:
  if col_estado in df_filtrado.columns:
    df_filtrado = df_filtrado[
        df_filtrado[col_estado].fillna("").astype(str).str.strip().str.upper().isin(
            {valor.upper() for valor in local_selecionado}
        )
    ]
  elif col_local in df_filtrado.columns:
    df_filtrado = df_filtrado[
        df_filtrado[col_local]
        .fillna("")
        .astype(str)
        .str.split(",")
        .str[-1]
        .str.strip()
        .str.upper()
        .isin({valor.upper() for valor in local_selecionado})
    ]

if senioridade_selecionada != "Todos" and "seniority" in df_filtrado.columns:
  df_filtrado = df_filtrado[
      df_filtrado["seniority"].fillna("na").astype(str).str.lower()
      == senioridade_selecionada.lower()
  ]


def calcular_match(descricao, skills):
  if not skills or pd.isna(descricao):
    return 50
  texto = str(descricao).lower()
  encontradas = sum(1 for s in skills if s.lower() in texto)
  return min(int(30 + (encontradas / len(skills)) * 69), 99)


if col_desc in df_filtrado.columns:
  df_filtrado["Match (%)"] = df_filtrado[col_desc].apply(
      lambda x: calcular_match(x, skills_usuario)
  )
else:
  df_filtrado["Match (%)"] = 75

df_filtrado = df_filtrado.sort_values(by="Match (%)", ascending=False)


# --- MÉTRICAS PRINCIPAIS (3 colunas limpas) ---
c1, c2, c3 = st.columns(3)

with c1:
  st.metric("Vagas Encontradas", len(df_filtrado))
with c2:
  match_medio = round(df_filtrado["Match (%)"].mean(), 1) if not df_filtrado.empty else 0
  st.metric("Match Médio", f"{match_medio}%")
with c3:
  local_principal = (
      str(df_filtrado[col_local].mode()[0]).split(",")[0]
      if col_local in df_filtrado.columns and not df_filtrado.empty
      else "N/A"
  )
  st.metric("Localização Principal", local_principal)

st.markdown("---")

# --- CONTEÚDO PRINCIPAL ---
col_left, col_right = st.columns([2, 1])

with col_left:
  st.subheader("📋 Lista de Oportunidades")
  if not df_filtrado.empty:
    colunas = [
        c
        for c in [col_titulo, col_empresa, col_local, "Match (%)"]
        if c in df_filtrado.columns
    ]
    st.dataframe(
        df_filtrado[colunas].head(30), use_container_width=True, hide_index=True
    )

    st.markdown("### 📩 Enviar Alerta de Vagas por E-mail")
    with st.form("form_enviar_email"):
      email_destino = st.text_input(
          "Endereço de E-mail de Destino", placeholder="teu.email@exemplo.com"
      )
      frequencia_envio = st.selectbox(
          "Frequência do Alerta", ["Imediato (Teste)", "Diário", "Semanal"]
      )
      enviar_btn = st.form_submit_button("Disparar Alerta de Vagas")

      if enviar_btn:
        if email_destino and "@" in email_destino:
          # Simula a formatação do conteúdo do alerta que seria enviado via API do Gmail
          resumo_vagas = "\n".join(
              [
                f"- {row.get(col_titulo, 'Vaga')} na empresa {row.get(col_empresa, 'N/A')} (Match: {row.get('Match (%)', 0)}%)"
                for _, row in df_filtrado.head(5).iterrows()
              ]
          )

          st.success(
              f"Alerta configurado e enviado com sucesso para **{email_destino}**"
              f" ({frequencia_envio})!\n\n**Resumo enviado:**\n{resumo_vagas}"
          )
        else:
          st.error("Por favor, introduza um endereço de e-mail válido.")
  else:
    st.warning("Nenhuma vaga encontrada com os critérios definidos.")

with col_right:
  st.subheader("📊 Top Empresas")
  if not df_filtrado.empty and col_empresa in df_filtrado.columns:
    top_empresas = df_filtrado[col_empresa].value_counts().head(5).reset_index()
    top_empresas.columns = ["Empresa", "Total"]

    fig = px.bar(
        top_empresas,
        x="Total",
        y="Empresa",
        orientation="h",
        text="Total",
        template="plotly_dark",
        color="Total",
        color_continuous_scale="Blues",
    )

    fig.update_traces(
        textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis=dict(showgrid=False, showticklabels=False, title=""),
        yaxis_title="",
        coloraxis_showscale=False,
        margin=dict(l=0, r=30, t=10, b=10),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(
        fig, use_container_width=True, config={"displayModeBar": False}
    )
  else:
    st.info("Sem dados suficientes.")