### Link do site no ar : https://alerta-vagas-hbqhmi8qgbawcg7h2we5qq.streamlit.app/

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
git clone https://github.com/pedrosantos-code/Alerta-Vagas.git
```

### 2. Instalar as dependências essenciais
```bash
pip install -r requirements.txt
```

### 3. Executar a aplicação
```bash
python -m streamlit run app.py
```

### 4. Alternar entre Light e Dark
No menu nativo do Streamlit, no canto superior direito, escolhe **Light** ou **Dark**. Os dois temas estão configurados em `.streamlit/config.toml`; a aplicação acompanha a seleção e inicia em Light. A opção **System** fica oculta para manter apenas os dois modos pedidos.

### 5. Configurar envio real de e-mail (opcional)
Se quiseres activar o envio real via SMTP, define estas variáveis de ambiente antes de iniciar a app:

```bash
set DATA_PATH=data/Cleaned_DS_Jobs.csv
set SMTP_HOST=smtp.gmail.com
set SMTP_PORT=587
set SMTP_USER=teu-email@gmail.com
set SMTP_PASSWORD=sua-password-de-app
set SMTP_TLS=true
set PORT=8501
```

> Em Gmail, normalmente é necessário criar uma senha de app e ativar SMTP.

Se as variáveis não estiverem definidas, a app continua a funcionar em modo demo com vista previa do alerta no próprio dashboard.

### 6. Deploy em produção
Para ambientes cloud ou containerizados, usa uma das opções abaixo:

#### Opção A: Streamlit em servidor público
```bash
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
```

#### Opção B: Docker
```bash
docker build -t alerta-vagas .
docker run -p 8501:8501 --env-file .env alerta-vagas
```

#### Opção C: Script de arranque
```bash
bash start.sh
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
