import os
import smtplib
from html import escape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
            --page-padding: clamp(1rem, 3vw, 3rem);
            --ink: light-dark(#16233a, #edf4ff);
            --muted: light-dark(#73819a, #91a1bb);
            --line: light-dark(rgba(80, 101, 137, 0.15), rgba(148, 174, 218, 0.14));
            --panel: light-dark(rgba(255, 255, 255, 0.92), rgba(15, 24, 43, 0.78));
            --accent: light-dark(#7064d8, #6d55c7);
            --accent-strong: light-dark(#5f4ec4, #c0b5ff);
        }

        .stApp {
            background:
                radial-gradient(ellipse at 88% 0%, rgba(123, 108, 232, 0.09), transparent 35rem),
                radial-gradient(ellipse at 0% 14%, rgba(112, 100, 216, 0.07), transparent 30rem),
                light-dark(#f5f7fb, #080d18);
            color: var(--ink);
        }

        [data-testid="stHeader"] {
            background: light-dark(rgba(245, 247, 251, 0.82), rgba(8, 13, 24, 0.82));
        }

        [data-testid="stMainMenuItem-theme-System"] {
            display: none !important;
        }

        .block-container {
            padding-top: 1.6rem !important;
            padding-left: var(--page-padding) !important;
            padding-right: var(--page-padding) !important;
            max-width: 1480px !important;
        }

        h1, h2, h3, p, label {
            color: var(--ink);
        }

        h1, h2, h3 {
            letter-spacing: -0.035em;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: clamp(1.5rem, 4vw, 3.25rem);
            margin: 0.6rem 0 1.6rem;
            border: 1px solid color-mix(in srgb, var(--accent) 20%, transparent);
            border-radius: 28px;
            background:
                radial-gradient(ellipse at 90% 12%, rgba(140, 123, 247, 0.18), transparent 34%),
                radial-gradient(ellipse at 68% 100%, rgba(137, 116, 224, 0.1), transparent 37%),
                linear-gradient(
                    120deg,
                    light-dark(#ffffff, #142036) 0%,
                    light-dark(#f5f8ff, #0d1425) 55%,
                    light-dark(#f2f7fb, #0d1425) 100%
                );
            box-shadow: 0 24px 70px rgba(44, 60, 94, 0.09), inset 0 1px rgba(255,255,255,0.9);
        }

        .hero:after {
            content: "";
            position: absolute;
            right: -5rem;
            top: -9rem;
            width: 25rem;
            height: 25rem;
            border: 1px solid color-mix(in srgb, var(--accent) 20%, transparent);
            border-radius: 50%;
            box-shadow: 0 0 0 2.5rem color-mix(in srgb, var(--accent) 4%, transparent), 0 0 0 5rem rgba(126, 111, 226, 0.035);
            pointer-events: none;
        }

        .hero-eyebrow, .section-kicker {
            color: var(--accent);
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .hero-eyebrow {
            color: var(--accent-strong);
        }

        .hero-title {
            position: relative;
            z-index: 1;
            max-width: 760px;
            margin: 0.8rem 0 0.7rem;
            font-size: clamp(2.2rem, 5vw, 4.25rem);
            font-weight: 780;
            letter-spacing: -0.065em;
            line-height: 1.04;
        }

        .hero-title span {
            color: transparent;
            background: linear-gradient(
                105deg,
                light-dark(#6847c7, #a99aff) 0%,
                light-dark(#9675f5, #d0bfff) 100%
            );
            background-clip: text;
            -webkit-background-clip: text;
        }

        .hero-copy {
            max-width: 650px;
            margin: 0;
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.7;
        }

        .hero-status {
            position: absolute;
            right: 2rem;
            bottom: 1.8rem;
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            padding: 0.6rem 0.85rem;
            border: 1px solid color-mix(in srgb, var(--accent) 22%, transparent);
            border-radius: 999px;
            background: light-dark(rgba(255, 255, 255, 0.78), rgba(8, 20, 31, 0.52));
            color: light-dark(#53647d, #b7c8da);
            font-size: 0.75rem;
        }

        .hero-status i {
            width: 0.45rem;
            height: 0.45rem;
            border-radius: 50%;
            background: light-dark(#8b5cf6, #bc8cff);
            box-shadow: 0 0 14px light-dark(rgba(139, 92, 246, 0.9), rgba(188, 140, 255, 0.95));
        }

        .metric-card {
            min-height: 132px;
            padding: 1.15rem 1.3rem;
            border: 1px solid var(--line);
            border-radius: 20px;
            background: linear-gradient(
                145deg,
                light-dark(#ffffff, rgba(20, 31, 53, 0.88)),
                light-dark(#fbfcff, rgba(13, 20, 35, 0.82))
            );
            box-shadow: 0 12px 30px rgba(38, 55, 87, 0.045), inset 0 1px light-dark(#ffffff, rgba(255,255,255,0.04));
        }

        .metric-label {
            margin-bottom: 0.75rem;
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 650;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--ink);
            font-size: clamp(1.55rem, 2.8vw, 2.2rem);
            font-weight: 760;
            letter-spacing: -0.06em;
            line-height: 1.1;
            overflow-wrap: anywhere;
        }

        .metric-foot {
            margin-top: 0.55rem;
            color: var(--muted);
            font-size: 0.76rem;
        }

        .section-heading {
            margin: 1.8rem 0 0.95rem;
            color: var(--ink);
            font-size: 1.25rem;
            font-weight: 720;
            letter-spacing: -0.035em;
        }

        .section-heading span {
            display: block;
            margin-bottom: 0.35rem;
            color: var(--accent-strong) !important;
            font-size: 0.65rem;
            font-weight: 750;
            letter-spacing: 0.15em;
            text-transform: uppercase;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid var(--line) !important;
            border-radius: 20px !important;
            background: var(--panel) !important;
            box-shadow: 0 12px 34px rgba(38, 55, 87, 0.045);
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--line);
            background:
                radial-gradient(ellipse at 0% 0%, color-mix(in srgb, var(--accent) 9%, transparent), transparent 28rem),
                light-dark(#f1effa, #111322);
        }

        [data-testid="stSidebar"] > div:first-child {
            background: transparent;
        }

        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            letter-spacing: -0.035em;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: var(--muted);
        }

        input:not([type="range"]):not([role="combobox"]), textarea, [data-baseweb="select"] > div {
            border-color: var(--line) !important;
            border-radius: 12px !important;
            background-color: light-dark(#ffffff, rgba(11, 18, 32, 0.85)) !important;
            color: var(--ink) !important;
        }

        [data-testid="stMultiSelect"] [data-rac][role="group"],
        [data-testid="stSelectbox"] [data-rac][role="group"] {
            box-sizing: border-box;
            border: 1px solid var(--line);
            border-radius: 12px;
            background-color: light-dark(#ffffff, rgba(11, 18, 32, 0.85));
            color: var(--ink);
        }

        [data-testid="stMultiSelect"] input[role="combobox"],
        [data-testid="stSelectbox"] input[role="combobox"] {
            border: 0 !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        input[type="range"] {
            border: 0 !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        input:not([type="range"]):not([role="combobox"]):focus,
        textarea:focus,
        [data-testid="stMultiSelect"]:focus-within [data-rac][role="group"],
        [data-testid="stSelectbox"]:focus-within [data-rac][role="group"] {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent) 18%, transparent) !important;
        }

        button[kind="primary"], [data-testid="stFormSubmitButton"] button {
            border: 1px solid color-mix(in srgb, var(--accent) 48%, transparent) !important;
            border-radius: 12px !important;
            background: linear-gradient(
                110deg,
                #684bc8,
                #8065dd
            ) !important;
            color: #ffffff !important;
            font-weight: 750 !important;
            transition: transform 160ms ease, filter 160ms ease;
        }

        button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] button:hover {
            filter: brightness(1.08);
            transform: translateY(-1px);
        }

        [data-testid="stDataFrame"] {
            overflow: hidden;
            border: 1px solid var(--line);
            border-radius: 16px;
        }

        [data-testid="stPlotlyChart"] {
            padding: 0.35rem;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: light-dark(rgba(255, 255, 255, 0.8), rgba(12, 19, 34, 0.5));
            box-shadow: 0 12px 34px rgba(38, 55, 87, 0.045);
        }

        [data-testid="stPlotlyChart"] svg text {
            fill: light-dark(#52617a, #edf4ff) !important;
        }

        hr {
            border-color: var(--line) !important;
        }

        [data-testid="stSidebar"] button:not([kind="primary"]):hover {
            border-color: color-mix(in srgb, var(--accent) 55%, transparent) !important;
            color: var(--accent-strong) !important;
        }

        .stDataFrame {
            overflow-x: auto;
        }

        @media (max-width: 768px) {
            .block-container {
                padding-top: 1rem !important;
                padding-left: 0.8rem !important;
                padding-right: 0.8rem !important;
            }

            .hero {
                padding: 1.5rem;
                border-radius: 22px;
            }

            .hero-status {
                position: static;
                width: fit-content;
                margin-top: 1.2rem;
            }

            div[data-testid="stHorizontalBlock"] {
                display: block !important;
            }

            div[data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                max-width: 100% !important;
            }

            div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                margin-bottom: 0.9rem !important;
            }

            .metric-card {
                min-height: 0;
                margin-bottom: 0.65rem;
            }
        }

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <div class="hero-eyebrow">Inteligência de carreira · 2026</div>
        <h1 class="hero-title"><span>A próxima oportunidade</span><br><span>começa com clareza.</span></h1>
        <p class="hero-copy">Explore o mercado, encontre vagas alinhadas ao seu perfil e transforme a busca em uma decisão estratégica.</p>
        <div class="hero-status"><i></i> Radar de oportunidades ativo</div>
    </section>
    """,
    unsafe_allow_html=True,
)


# --- CARREGAR DADOS ---
@st.cache_data
def carregar_vagas():
    data_path = os.getenv("DATA_PATH", "data/Cleaned_DS_Jobs.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Ficheiro de dados não encontrado em '{data_path}'. "
            "Certifica-te de que a variável DATA_PATH aponta para o CSV correto."
        )
    return pd.read_csv(data_path)


try:
    df_vagas = carregar_vagas()
except Exception as e:
    st.error(
        "Não foi possível carregar o ficheiro 'data/Cleaned_DS_Jobs.csv'."
        f" Detalhe técnico: {e}"
    )
    st.stop()


def obter_valor_numero(valor):
    if pd.isna(valor):
        return 0
    try:
        return float(str(valor).replace("$", "").replace(",", "").strip())
    except ValueError:
        return 0


def enviar_alerta_email(destino, frequencia, vagas_top):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    use_tls = os.getenv("SMTP_TLS", "true").lower() in {"1", "true", "yes", "y"}

    if not smtp_host or not smtp_user or not smtp_password:
        return False, "SMTP não configurado. O alerta foi apenas simulado no dashboard."

    assunto = f"Alerta de Vagas - {frequencia}"
    corpo = "\n".join(
        [
            "Olá,",
            "",
            "Aqui vai o resumo das vagas mais alinhadas ao teu perfil:",
            "",
            *[
                f"- {linha['Job Title']} na empresa {linha.get('Company Name', 'N/A')} "
                f"(Match: {linha.get('Match (%)', 0)}%, salário médio: ${linha.get('avg_salary', 0)}k)"
                for _, linha in vagas_top.head(5).iterrows()
            ],
            "",
            "Atenciosamente,",
            "Alerta de Vagas & Analytics",
        ]
    )

    mensagem = MIMEMultipart()
    mensagem["From"] = smtp_user
    mensagem["To"] = destino
    mensagem["Subject"] = assunto
    mensagem.attach(MIMEText(corpo, "plain", "utf-8"))

    with smtplib.SMTP(smtp_host, smtp_port) as servidor:
        if use_tls:
            servidor.starttls()
        servidor.login(smtp_user, smtp_password)
        servidor.send_message(mensagem)

    return True, "Alerta enviado com sucesso por SMTP."


def calcular_match(descricao, skills, linha=None):
    if not skills:
        return 50

    texto = str(descricao or "").lower()
    peso_total = 0.0

    for skill in skills:
        nome = str(skill).strip().lower()
        score_skill = 0.0

        if nome in texto:
            score_skill += 0.7

        if linha is not None:
            mapa_colunas = {
                "python": ["python"],
                "sql": ["sql"],
                "pandas": ["pandas"],
                "machine learning": ["machine_learning", "ml", "deep_learning"],
                "aws": ["aws"],
                "tableau": ["tableau"],
                "spark": ["spark"],
            }
            for coluna in mapa_colunas.get(nome, []):
                valor = linha.get(coluna, 0)
                if isinstance(valor, str):
                    valor_normalizado = valor.strip().lower()
                    if valor_normalizado in {"1", "true", "yes", "y"}:
                        score_skill += 0.3
                elif pd.notna(valor):
                    try:
                        if float(valor) > 0:
                            score_skill += 0.3
                    except (TypeError, ValueError):
                        pass

        peso_total += min(score_skill, 1.0)

    if not skills:
        return 50

    percentual = (peso_total / len(skills)) * 100
    return min(int(percentual), 99)


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

if "avg_salary" in df_vagas.columns:
    salario_minimo = st.sidebar.slider(
        "Salário mínimo (k USD/ano)",
        min_value=40,
        max_value=300,
        value=40,
        step=10,
        key="salario_minimo",
    )
else:
    salario_minimo = 0

st.sidebar.divider()
st.sidebar.subheader("🎯 Stack Tecnológico")
skills_usuario = st.sidebar.multiselect(
    "Competências dominadas:",
    ["Python", "SQL", "Pandas", "Machine Learning", "AWS", "Tableau", "Spark"],
    default=["Python", "SQL"],
    key="skills_usuario",
)

match_minimo = st.sidebar.slider(
    "Match mínimo (%)",
    min_value=0,
    max_value=100,
    value=40,
    step=5,
    key="match_minimo",
)

if st.sidebar.button("Limpar filtros", use_container_width=True):
    for key in [
        "termo_busca",
        "empresas",
        "localizacao",
        "senioridade",
        "skills_usuario",
        "salario_minimo",
        "match_minimo",
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

if "avg_salary" in df_filtrado.columns:
    df_filtrado["avg_salary"] = df_filtrado["avg_salary"].apply(obter_valor_numero)
    df_filtrado = df_filtrado[df_filtrado["avg_salary"] >= salario_minimo]

if col_desc in df_filtrado.columns:
    df_filtrado["Match (%)"] = df_filtrado.apply(
        lambda row: calcular_match(row.get(col_desc, ""), skills_usuario, row),
        axis=1,
    )
else:
    df_filtrado["Match (%)"] = 75

if not df_filtrado.empty:
    df_filtrado = df_filtrado[df_filtrado["Match (%)"] >= match_minimo]

df_filtrado = df_filtrado.sort_values(by="Match (%)", ascending=False)


# --- MÉTRICAS PRINCIPAIS ---
match_medio = round(df_filtrado["Match (%)"].mean(), 1) if not df_filtrado.empty else 0
local_principal = (
    str(df_filtrado[col_local].mode()[0]).split(",")[0]
    if col_local in df_filtrado.columns and not df_filtrado.empty
    else "N/A"
)
vagas_match_alto = int((df_filtrado["Match (%)"] >= 80).sum())

metricas = [
    ("Oportunidades", f"{len(df_filtrado):,}".replace(",", "."), "Vagas dentro dos filtros"),
    ("Match médio", f"{match_medio}%", "Aderência média ao seu stack"),
    ("Alta compatibilidade", f"{vagas_match_alto}", "Vagas com match igual ou acima de 80%"),
    ("Local em destaque", escape(local_principal), "Localização mais frequente"),
]

st.markdown(
    '<div class="section-heading"><span>Visão geral</span>Seu radar em números</div>',
    unsafe_allow_html=True,
)
metric_cols = st.columns(4)
for coluna, (rotulo, valor, detalhe) in zip(metric_cols, metricas):
    with coluna:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{rotulo}</div>
                <div class="metric-value">{valor}</div>
                <div class="metric-foot">{detalhe}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- CONTEÚDO PRINCIPAL ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown(
        '<div class="section-heading"><span>Seleção personalizada</span>Oportunidades em destaque</div>',
        unsafe_allow_html=True,
    )
    if not df_filtrado.empty:
        colunas = [
            c
            for c in [col_titulo, col_empresa, col_local, "avg_salary", "Match (%)"]
            if c in df_filtrado.columns
        ]
        tabela_vagas = df_filtrado[colunas].head(30).rename(
            columns={"avg_salary": "Salário médio (k USD)"}
        )
        st.dataframe(
            tabela_vagas, use_container_width=True, hide_index=True
        )

        st.markdown(
            '<div class="section-heading"><span>Fique à frente</span>Receba sua shortlist por e-mail</div>',
            unsafe_allow_html=True,
        )
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
                    resumo_vagas = "\n".join(
                        [
                            f"- {row.get(col_titulo, 'Vaga')} na empresa {row.get(col_empresa, 'N/A')} (Match: {row.get('Match (%)', 0)}%)"
                            for _, row in df_filtrado.head(5).iterrows()
                        ]
                    )

                    sucesso, mensagem = enviar_alerta_email(
                        email_destino, frequencia_envio, df_filtrado.head(5)
                    )

                    if sucesso:
                        st.success(
                            f"{mensagem}\n\n**Resumo enviado:**\n{resumo_vagas}"
                        )
                    else:
                        st.warning(
                            f"{mensagem}\n\n**Resumo do preview:**\n{resumo_vagas}"
                        )
                else:
                    st.error("Por favor, introduza um endereço de e-mail válido.")
    else:
        st.warning("Nenhuma vaga encontrada com os critérios definidos.")

with col_right:
    st.markdown(
        '<div class="section-heading"><span>Quem está contratando</span>Empresas em alta</div>',
        unsafe_allow_html=True,
    )
    if not df_filtrado.empty and col_empresa in df_filtrado.columns:
        top_empresas = df_filtrado[col_empresa].value_counts().head(5).reset_index()
        top_empresas.columns = ["Empresa", "Total"]

        paleta_empresas = ["#7154cf", "#8b62d5", "#a16ad2", "#795edb", "#b37ad6"]
        fig = px.bar(
            top_empresas,
            x="Total",
            y="Empresa",
            orientation="h",
            text="Total",
            template="plotly_white",
        )

        fig.update_traces(
            marker=dict(
                color=paleta_empresas[: len(top_empresas)],
                cornerradius=8,
                line=dict(width=0),
            ),
            textfont_size=13,
            textfont_color="#6d628f",
            textangle=0,
            textposition="outside",
            insidetextanchor="end",
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>%{x} vagas<extra></extra>",
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            xaxis=dict(
                showgrid=False,
                showticklabels=False,
                showline=False,
                zeroline=False,
                title="",
                range=[0, top_empresas["Total"].max() * 1.14],
            ),
            yaxis_title="",
            font=dict(color="#6d628f"),
            bargap=0.36,
            margin=dict(l=8, r=36, t=16, b=12),
            height=320,
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(255,255,255,0)",
        )

        st.plotly_chart(
            fig, use_container_width=True, config={"displayModeBar": False}
        )
    else:
        st.info("Sem dados suficientes.")