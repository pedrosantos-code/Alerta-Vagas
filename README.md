# 💼 Job Alert & Analytics Dashboard

Um painel web interativo, minimalista e focado em dados reais, desenvolvido em **Python** e **Streamlit**, desenhado para eliminar o ruído na procura de emprego e otimizar a monitorização de oportunidades de mercado.

---

## 🎯 O Problema

A procura por oportunidades de emprego em plataformas tradicionais costuma ser exaustiva e ineficiente. Profissionais de tecnologia e análise de dados deparam-se constantemente com uma avalanche de notificações irrelevantes, cargos desajustados ao seu perfil e uma grande quantidade de ruído digital. Isto gera **fadiga de alertas** e perda de tempo preciosa a filtrar manualmente dezenas de ofertas que não correspondem às competências reais do candidato.

---

## 📋 Resumo da Solução

Para resolver este problema, foi desenvolvido este painel interativo e inteligente em **Streamlit e Python** alimentado por dados reais do mercado (Glassdoor/Kaggle). A aplicação oferece:

* **🔍 Filtros Dinâmicos e Limpos:** Busca rápida por cargos, palavras-chave e empresas específicas sem poluição visual.
* **🎯 Calculadora de Match de Perfil:** Um algoritmo em tempo real que cruza o teu *stack* tecnológico com as descrições das vagas, classificando a compatibilidade em percentagem.
* **📊 Visualização de Dados Avançada:** Gráficos interativos estilizados (Top Empresas) construídos com Plotly.
* **📈 KPIs e Inteligência de Mercado:** Indicadores claros de volume de vagas, alta compatibilidade e localização principal.
* **📩 Envio Automatizado de Alertas:** Funcionalidade integrada para disparar o resumo da *shortlist* de oportunidades diretamente para o teu e-mail.

---

## 🛠️ Tecnologias Utilizadas

O projeto foi construído utilizando o seguinte *stack* tecnológico:
* **Python** (Lógica de dados e processamento)
* **Streamlit** (Interface web interativa e dashboard)
* **Pandas** (Manipulação e tratamento de datasets)
* **Plotly** (Gráficos interativos e estilizados)

---

## 🛠️ Instalação e Execução

### 1. Clonar o repositório
```bash
git clone 
```

### 2. Instalar as dependências essenciais
```bash
pip install streamlit pandas plotly
```

### 3. Executar a aplicação
```bash
streamlit run app.py
```
---

## 📂 Estrutura do Projeto

```text
Alerta-Vagas/
│
├── data/
│   └── Cleaned_DS_Jobs.csv    # Base de dados de vagas (Glassdoor/Kaggle)
│
├── app.py                     # Aplicação principal Streamlit
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação do projeto
