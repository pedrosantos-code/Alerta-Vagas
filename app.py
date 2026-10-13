from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Alerta de Vagas & Analytics", page_icon="💼", layout="wide"
)

st.title("💼 Alerta de Vagas & Painel de Oportunidades (Glassdoor Data)")
st.markdown(
    "Filtra, analisa e monitoriza as melhores vagas de Ciência de Dados sem ruído e sem spam de notificações."
)


# --- CARREGAR DADOS REAIS DO KAGGLE ---
@st.cache_data
def carregar_vagas():
  # Lê o arquivo CSV localizado na pasta data/
  df = pd.read_csv("data/Cleaned_DS_Jobs.csv")
  return df


try:
  df_vagas = carregar_vagas()
except Exception as e:
  st.error(
      f"Erro ao carregar o arquivo CSV. Verifique se o caminho 'data/Cleaned_DS_Jobs.csv' está correto. Detalhe: {e}"
  )
  st.stop()

# --- BARRA LATERAL (FILTROS DE BUSCA) ---
st.sidebar.header("⚙️ Configurar Filtros de Vagas")

# Busca por texto genérico (no título ou descrição, dependendo das colunas)
# Geralmente colunas comuns em datasets do Glassdoor: 'Job Title', 'Company Name', 'Location', 'Salary Estimate'
coluna_titulo = (
    "Job Title" if "Job Title" in df_vagas.columns else df_vagas.columns[0]
)
coluna_empresa = (
    "Company Name"
    if "Company Name" in df_vagas.columns
    else df_vagas.columns[1]
)
coluna_local = (
    "Location" if "Location" in df_vagas.columns else df_vagas.columns[2]
)

termo_busca = st.sidebar.text_input(
    "Filtrar por Palavra-Chave / Cargo", value=""
)

# Filtro por Empresa se a coluna existir
if coluna_empresa in df_vagas.columns:
  empresas_unicas = sorted(df_vagas[coluna_empresa].dropna().unique())
  empresas_selecionadas = st.sidebar.multiselect(
      "Filtrar por Empresa", options=empresas_unicas, default=[]
  )
else:
  empresas_selecionadas = []

st.sidebar.divider()
alert_email = st.sidebar.checkbox("Ativar Notificações por E-mail", value=True)

# --- FILTRAGEM DINÂMICA ---
df_filtrado = df_vagas.copy()

# Aplica filtro de texto no título do cargo
if termo_busca:
  df_filtrado = df_filtrado[
      df_filtrado[coluna_titulo]
      .astype(str)
      .str.contains(termo_busca, case=False, na=False)
  ]

# Aplica filtro de empresas se selecionadas
if empresas_selecionadas and coluna_empresa in df_vagas.columns:
  df_filtrado = df_filtrado[
      df_filtrado[coluna_empresa].isin(empresas_selecionadas)
  ]

# --- PAINEL PRINCIPAL (KPIs) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
  st.metric(label="Total de Vagas Encontradas", value=len(df_filtrado))
with col2:
  total_empresas = (
      df_filtrado[coluna_empresa].nunique()
      if coluna_empresa in df_filtrado.columns
      else 0
  )
  st.metric(label="Empresas Distintas", value=total_empresas)
with col3:
  modalidade_freq = (
      df_filtrado["Location"].mode()[0]
      if "Location" in df_filtrado.columns and not df_filtrado.empty
      else "N/A"
  )
  st.metric(label="Localização Mais Comum", value=str(modalidade_freq)[:20])
with col4:
  st.metric(
      label="Status do Alerta",
      value="Ativo 🟢" if alert_email else "Pausado 🔴",
  )

st.divider()

# --- GRÁFICOS E ANÁLISE ---
col_left, col_right = st.columns([2, 1])

with col_left:
  st.subheader("📋 Lista de Vagas Filtradas")
  if not df_filtrado.empty:
    st.dataframe(
        df_filtrado.head(100), use_container_width=True, hide_index=True
    )
  else:
    st.warning("Nenhuma vaga encontrada com os filtros selecionados.")

with col_right:
  st.subheader("📊 Top Empresas com Vagas")
  if not df_filtrado.empty and coluna_empresa in df_filtrado.columns:
    top_empresas = df_filtrado[coluna_empresa].value_counts().reset_index()
    top_empresas.columns = ["Empresa", "Quantidade"]
    fig = px.bar(
        top_empresas.head(5),
        x="Quantidade",
        y="Empresa",
        orientation="h",
        template="plotly_dark",
        title="Empresas com Mais Oportunidades",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
  else:
    st.info("Dados insuficientes para gerar o gráfico.")

# --- AÇÃO / CADASTRO DE NOVO ALERTA ---
st.divider()
st.subheader("📩 Testar Envio de Alerta")

with st.form("form_alerta"):
  email_user = st.text_input(
      "Introduza o seu e-mail para receber um resumo diário de vagas:"
  )
  frequencia = st.selectbox(
      "Frequência do Alerta", ["Imediata", "Diária", "Semanal"]
  )
  submit = st.form_submit_button("Salvar Preferências de Alerta")

  if submit:
    if email_user:
      st.success(
          f"Alerta configurado com sucesso para {email_user}! Frequência:"
          f" {frequencia}."
      )
    else:
      st.error("Por favor, informe um e-mail válido.")