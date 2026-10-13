import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Alerta de Vagas & Analytics", page_icon="💼", layout="wide"
)

st.title("💼 Alerta de Vagas & Analytics")
st.markdown("Filtra e monitoriza as melhores oportunidades sem ruído visual.")


# --- CARREGAR DADOS ---
@st.cache_data
def carregar_vagas():
  return pd.read_csv("data/Cleaned_DS_Jobs.csv")


try:
  df_vagas = carregar_vagas()
except Exception as e:
  st.error(f"Erro ao carregar o ficheiro de dados: {e}")
  st.stop()


# --- BARRA LATERAL SIMPLIFICADA ---
st.sidebar.header("🔍 Filtros")

termo_busca = st.sidebar.text_input("Cargo / Palavra-Chave", "")

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

skills_usuario = st.sidebar.multiselect(
    "Stack Tecnológico",
    ["Python", "SQL", "Pandas", "Machine Learning", "AWS", "Tableau"],
    default=["Python", "SQL"],
)


# --- FILTRAGEM E MATCH ---
df_filtrado = df_vagas.copy()

if termo_busca:
  df_filtrado = df_filtrado[
      df_filtrado[col_titulo]
      .astype(str)
      .str.contains(termo_busca, case=False, na=False)
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


# --- MÉTRICAS PRINCIPAIS (3 colunas para maior espaçamento) ---
c1, c2, c3 = st.columns(3)

with c1:
  st.metric("Vagas Encontradas", len(df_filtrado))
with c2:
  st.metric(
      "Alta Compatibilidade",
      len(df_filtrado[df_filtrado["Match (%)"] >= 80]),
  )
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
    colunas = [c for c in [col_titulo, col_empresa, col_local, "Match (%)"] if c in df_filtrado.columns]
    st.dataframe(
        df_filtrado[colunas].head(30), use_container_width=True, hide_index=True
    )

    csv_data = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Descarregar Shortlist (CSV)",
        data=csv_data,
        file_name="vagas_filtradas.csv",
        mime="text/csv",
    )
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
        template="plotly_dark",
        height=280,
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=0, r=0, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
  else:
    st.info("Sem dados suficientes.")