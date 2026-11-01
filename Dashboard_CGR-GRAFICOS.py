import streamlit as st
import pandas as pd
import plotly.express as px
import os
import glob

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Centro de Comando Operacional & Telemetria", page_icon="🎛️", layout="wide", initial_sidebar_state="expanded")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_PASTA = os.environ.get("DADOS_OPERACIONAIS_PATH", os.path.join(BASE_DIR, "dados_operacionais"))

# --- 2. TEMA, CORES E BLINDAGEM DE CONTRASTE DA BARRA LATERAL ---
st.sidebar.title("📺 Modo de Exibição")
modo_tv = st.sidebar.toggle("📺 Ativar Modo TV (Tela Cheia)", value=False)

st.sidebar.markdown("---")
st.sidebar.title("🎨 Estilo & Paleta")
paleta_selecionada = st.sidebar.selectbox(
    "Escolha o Tema de Cores:",
    ["Preto & Laranja (Dark)", "Azul Executivo (Dark)", "Roxo Cyber (Dark)", "Clean Moderno (Light)"]
)

if paleta_selecionada == "Preto & Laranja (Dark)":
    bg_app = "#121212"
    bg_card = "#1E1E1E"
    cor_texto = "#FFFFFF"
    cor_sidebar_texto = "#FFFFFF"
    bg_sidebar = "#1A1A1A"
    tema_plotly = "plotly_dark"
    cores_grafico = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#FF33F3', '#33FFF3', '#FFA533', '#A533FF']
elif paleta_selecionada == "Azul Executivo (Dark)":
    bg_app = "#0B132B"
    bg_card = "#1C2541"
    cor_texto = "#FFFFFF"
    cor_sidebar_texto = "#FFFFFF"
    bg_sidebar = "#131B31"
    tema_plotly = "plotly_dark"
    cores_grafico = ['#4CC9F0', '#4895EF', '#F72585', '#7209B7', '#4361EE', '#3A0CA3', '#560BAD']
elif paleta_selecionada == "Roxo Cyber (Dark)":
    bg_app = "#10002B"
    bg_card = "#240046"
    cor_texto = "#FFFFFF"
    cor_sidebar_texto = "#FFFFFF"
    bg_sidebar = "#17013B"
    tema_plotly = "plotly_dark"
    cores_grafico = ['#FF007F', '#00FFFF', '#7928CA', '#9D4EDD', '#C77DFF', '#E0AAFF', '#FFB703']
else: # Clean Moderno (Light)
    bg_app = "#F8F9FA"
    bg_card = "#FFFFFF"
    cor_texto = "#1E293B"
    cor_sidebar_texto = "#0F172A"
    bg_sidebar = "#E2E8F0"
    tema_plotly = "plotly_white"
    cores_grafico = px.colors.qualitative.Bold

css_modo_tv = """
    [data-testid="stSidebar"] {display: none;}
""" if modo_tv else ""

# CSS Blindado para forçar alto contraste absoluto nos títulos da barra lateral e blocos
st.markdown(f'''
    <style>
    .stApp {{ background-color: {bg_app}; }}
    div[data-testid="stMetric"], div[data-testid="stExpander"] {{
        background-color: {bg_card} !important;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(128,128,128,0.3);
    }}
    .block-container h1, h2, h3, h4, p, label, span, div[data-testid="stMetricValue"] {{
        color: {cor_texto} !important;
    }}
    /* FORÇAR CONTRASTE NA BARRA LATERAL INDEPENDENTE DO TEMA */
    section[data-testid="stSidebar"] {{
        background-color: {bg_sidebar} !important;
        border-right: 1px solid rgba(128,128,128,0.3);
    }}
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown {{
        color: {cor_sidebar_texto} !important;
        font-weight: 700 !important;
    }}
    {css_modo_tv}
    </style>
''', unsafe_allow_html=True)

if not modo_tv:
    st.title("📊 Centro de Comando Operacional - Telemetria & Campo")
    st.markdown("Painel analítico integrado de parâmetros e indicadores operacionais de campo.")
    st.markdown("---")
else:
    st.markdown("<h2 style='text-align: center;'>📺 PAINEL EXECUTIVO EM TEMPO REAL - OPERAÇÕES</h2>", unsafe_allow_html=True)
    st.markdown("---")

# --- 3. LEITURA DE DADOS ---
@st.cache_data
def carregar_dados_operacionais():
    def _gerar_dados_sinteticos_demonstracao():
    import numpy as np
    datas = pd.date_range(end=pd.Timestamp.now(), periods=30, freq='D')
    estacoes = ['Estação Central 01', 'Estação Central 02', 'Estação Periférica Norte', 'Estação Periférica Sul', 'Estação Distribuição Leste']
    registros = []
    for d in datas:
        for est in estacoes:
            tipo = 'Central' if 'Central' in est else 'Periférico'
            registros.append({
                'DATA': d,
                'ESTACAO_ABA': est,
                'TIPO_ROTA': tipo,
                'ARQUIVO_ORIGEM': 'Demonstracao_Sintetica',
                'Pressão de Entrada (bar)': round(np.random.uniform(15.0, 22.0), 2),
                'Pressão de Saída (bar)': round(np.random.uniform(3.5, 4.5), 2),
                'Vazão Instantânea (m³/h)': round(np.random.uniform(120.0, 350.0), 1),
                'Temperatura Operacional (°C)': round(np.random.uniform(18.0, 28.0), 1),
                'Nível Odorização (mg/m³)': round(np.random.uniform(12.0, 18.0), 2),
            })
    df_mock = pd.DataFrame(registros)
    df_mock['DATA_FORMATADA'] = pd.to_datetime(df_mock['DATA'])
    return df_mock

    if not os.path.exists(CAMINHO_PASTA):
        st.info("💡 Modo Demonstração Ativo: Carregando dados operacionais simulados (configure DADOS_OPERACIONAIS_PATH para apontar para sua pasta de planilhas).")
        return _gerar_dados_sinteticos_demonstracao(), "Sucesso (Modo Demonstração)"
        return pd.DataFrame(), f"Pasta não encontrada: {CAMINHO_PASTA}"
        
    arquivos = glob.glob(os.path.join(CAMINHO_PASTA, "*.xls*"))
        if not arquivos:
        st.info("💡 Modo Demonstração Ativo: Nenhum arquivo Excel na pasta local. Carregando dados simulados.")
        return _gerar_dados_sinteticos_demonstracao(), "Sucesso (Modo Demonstração)"
        return pd.DataFrame(), "Nenhum arquivo Excel encontrado na pasta."
        
    lista_dfs = []
    for arq in arquivos:
        try:
            xls = pd.read_excel(arq, sheet_name=None, engine='openpyxl')
            for nome_aba, df_aba in xls.items():
                if 'MEDIDAS_' in nome_aba.upper() or 'DADOS_' in nome_aba.upper():
                    continue
                if df_aba.dropna(how='all').empty:
                    continue
                
                df_aba['ARQUIVO_ORIGEM'] = os.path.basename(arq).split('.')[0]
                df_aba['ESTACAO_ABA'] = nome_aba
                
                if 'PERIFÉRICO' in nome_aba.upper() or 'PERIFERICO' in nome_aba.upper():
                    df_aba['TIPO_ROTA'] = 'Periférico'
                elif 'CENTRAL' in nome_aba.upper():
                    df_aba['TIPO_ROTA'] = 'Central'
                else:
                    df_aba['TIPO_ROTA'] = 'Outros'
                    
                df_aba.columns = [str(c).strip() for c in df_aba.columns]
                lista_dfs.append(df_aba)
        except Exception as e:
            pass
            
    if not lista_dfs:
        return pd.DataFrame(), "Nenhum dado operacional válido encontrado."
        
    df_completo = pd.concat(lista_dfs, ignore_index=True)
    
    colunas_data = [c for c in df_completo.columns if c.upper() in ['DIA', 'DATA', 'DATA REGISTRO']]
    if colunas_data:
        col_data = colunas_data[0]
        df_completo['DATA_FORMATADA'] = pd.to_datetime(df_completo[col_data], errors='coerce')
    
    return df_completo, "Sucesso"

if not modo_tv:
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Sincronizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.sidebar.markdown("---")

with st.spinner("Lendo planilhas operacionais..."):
    df, status = carregar_dados_operacionais()

if df.empty:
    st.error(status)
    st.stop()

# --- 4. FILTRAGEM GLOBAL DE PERÍODO ---
if not modo_tv:
    st.sidebar.subheader("📅 Controle de Período")
    if 'DATA_FORMATADA' in df.columns and not df['DATA_FORMATADA'].dropna().empty:
        min_data = df['DATA_FORMATADA'].min().date()
        max_data = df['DATA_FORMATADA'].max().date()
        
        data_inicio, data_fim = st.sidebar.date_input(
            "Intervalo de Datas:",
            value=(min_data, max_data),
            min_value=min_data,
            max_value=max_data
        )
        df = df[(df['DATA_FORMATADA'].dt.date >= data_inicio) & (df['DATA_FORMATADA'].dt.date <= data_fim)]

# --- 5. LIMPEZA DOS PARÂMETROS NUMÉRICOS ---
colunas_ignorar = ['ARQUIVO_ORIGEM', 'ESTACAO_ABA', 'TIPO_ROTA', 'DATA_FORMATADA', 'TAG', 'HORA', 'DIA', 'DATA', 'DATA REGISTRO', 'ID OBJETO', 'DESCRIÇÃO DO OBJETO', 'UNID MEDIDA']

colunas_validas = []
for col in df.columns:
    if col not in colunas_ignorar:
        serie_num = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
        if serie_num.notna().sum() > 0:
            colunas_validas.append(col)
            df[col] = serie_num

if len(colunas_validas) == 0:
    colunas_validas = [c for c in df.columns if c not in colunas_ignorar]

estacoes_disponiveis = sorted(df['ESTACAO_ABA'].unique().tolist())

def seletor_estacoes_estilo_excel(key_prefix, todas_estacoes):
    if modo_tv:
        return todas_estacoes
    with st.expander(f"📌 Filtro de Estações ({key_prefix})", expanded=False):
        col_btn1, col_btn2 = st.columns(2)
        marcar_todas = col_btn1.button("✅ Marcar Todas", key=f"all_{key_prefix}")
        desmarcar_todas = col_btn2.button("❌ Desmarcar", key=f"none_{key_prefix}")
        
        selecoes = []
        for est in todas_estacoes:
            default_val = True
            if marcar_todas: default_val = True
            elif desmarcar_todas: default_val = False
                
            check = st.checkbox(est, value=default_val, key=f"chk_{key_prefix}_{est}")
            if check: selecoes.append(est)
    return selecoes

def gerar_grafico_flexivel(df_sub, x_col, y_col, tipo_grafico, titulo, cor_col):
    if df_sub.empty:
        return None
    if tipo_grafico == "Linha":
        fig = px.line(df_sub, x=x_col, y=y_col, color=cor_col, markers=True, template=tema_plotly, color_discrete_sequence=cores_grafico)
    elif tipo_grafico == "Barras":
        fig = px.bar(df_sub, x=x_col, y=y_col, color=cor_col, barmode='group', template=tema_plotly, color_discrete_sequence=cores_grafico)
    elif tipo_grafico == "Área Preenchida":
        fig = px.area(df_sub, x=x_col, y=y_col, color=cor_col, template=tema_plotly, color_discrete_sequence=cores_grafico)
    else: # Dispersão
        fig = px.scatter(df_sub, x=x_col, y=y_col, color=cor_col, template=tema_plotly, color_discrete_sequence=cores_grafico)
    
    fig.update_layout(title=titulo, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color=cor_texto), margin=dict(t=30, b=20, l=20, r=20))
    return fig


# =========================================================================
# GRADE DE 4 PAINÉIS INDEPENDENTES (COM ESCOLHA DO TIPO DE GRÁFICO)
# =========================================================================

col_t1, col_t2 = st.columns(2)

# --- PAINEL 1 ---
with col_t1:
    st.markdown("### 📈 1. Evolução Temporal")
    tipo_g1 = st.selectbox("Tipo de Gráfico:", ["Linha", "Barras", "Área Preenchida", "Dispersão"], key="t_g1")
    param_linha = st.selectbox("Parâmetro:", colunas_validas, index=0, key="l_p")
    estacoes_l = seletor_estacoes_estilo_excel("grafico1", estacoes_disponiveis)
    escala_tempo = st.radio("Escala:", ["Diário", "Mensal", "Anual"], horizontal=True, key="escala_l")

    df_l_val = df.dropna(subset=[param_linha])
    if estacoes_l: df_l_val = df_l_val[df_l_val['ESTACAO_ABA'].isin(estacoes_l)]

    if 'DATA_FORMATADA' in df_l_val.columns:
        if escala_tempo == "Diário": df_l_val['TEMPO_AGRUPADO'] = df_l_val['DATA_FORMATADA'].dt.strftime('%Y-%m-%d')
        elif escala_tempo == "Mensal": df_l_val['TEMPO_AGRUPADO'] = df_l_val['DATA_FORMATADA'].dt.to_period('M').astype(str)
        else: df_l_val['TEMPO_AGRUPADO'] = df_l_val['DATA_FORMATADA'].dt.year.astype(str)
    else:
        df_l_val['TEMPO_AGRUPADO'] = "Geral"

    df_linha_plot = df_l_val.dropna(subset=['TEMPO_AGRUPADO', param_linha]).groupby(['TEMPO_AGRUPADO', 'ESTACAO_ABA'])[param_linha].mean().reset_index()
    fig1 = gerar_grafico_flexivel(df_linha_plot, 'TEMPO_AGRUPADO', param_linha, tipo_g1, f"Evolução de {param_linha}", 'ESTACAO_ABA')
    if fig1: st.plotly_chart(fig1, use_container_width=True)
    else: st.info("Sem dados para exibir.")

# --- PAINEL 2 ---
with col_t2:
    st.markdown("### 📊 2. Comparativo de Médias")
    tipo_g2 = st.selectbox("Tipo de Gráfico:", ["Barras", "Linha", "Área Preenchida", "Dispersão"], key="t_g2")
    param_g2 = st.selectbox("Parâmetro:", colunas_validas, index=min(1, len(colunas_validas)-1), key="g2_p")
    estacoes_g2 = seletor_estacoes_estilo_excel("grafico2", estacoes_disponiveis)
    
    df_g2 = df.dropna(subset=[param_g2])
    if estacoes_g2: df_g2 = df_g2[df_g2['ESTACAO_ABA'].isin(estacoes_g2)]
    df_g2_plot = df_g2.groupby('ESTACAO_ABA')[param_g2].mean().reset_index()
    
    fig2 = gerar_grafico_flexivel(df_g2_plot, 'ESTACAO_ABA', param_g2, tipo_g2, f"Média de {param_g2}", 'ESTACAO_ABA')
    if fig2: st.plotly_chart(fig2, use_container_width=True)
    else: st.info("Sem dados para exibir.")

st.markdown("<br>", unsafe_allow_html=True)
col_t3, col_t4 = st.columns(2)

# --- PAINEL 3 ---
with col_t3:
    st.markdown("### 📉 3. Comparativo de Acumulados")
    tipo_g3 = st.selectbox("Tipo de Gráfico:", ["Barras", "Linha", "Área Preenchida", "Dispersão"], key="t_g3")
    param_g3 = st.selectbox("Parâmetro:", colunas_validas, index=min(2, len(colunas_validas)-1), key="g3_p")
    estacoes_g3 = seletor_estacoes_estilo_excel("grafico3", estacoes_disponiveis)
    
    df_g3 = df.dropna(subset=[param_g3])
    if estacoes_g3: df_g3 = df_g3[df_g3['ESTACAO_ABA'].isin(estacoes_g3)]
    df_g3_plot = df_g3.groupby('ESTACAO_ABA')[param_g3].sum().reset_index()
    
    fig3 = gerar_grafico_flexivel(df_g3_plot, 'ESTACAO_ABA', param_g3, tipo_g3, f"Soma de {param_g3}", 'ESTACAO_ABA')
    if fig3: st.plotly_chart(fig3, use_container_width=True)
    else: st.info("Sem dados para exibir.")

# --- PAINEL 4 ---
with col_t4:
    st.markdown("### 📊 4. Correlação Operacional")
    tipo_g4 = st.selectbox("Tipo de Gráfico:", ["Dispersão", "Linha", "Barras", "Área Preenchida"], key="t_g4")
    col_sc1, col_sc2 = st.columns(2)
    with col_sc1: param_sc_x = st.selectbox("Eixo X:", colunas_validas, index=0, key="sc_x")
    with col_sc2: param_sc_y = st.selectbox("Eixo Y:", colunas_validas, index=min(1, len(colunas_validas)-1), key="sc_y")

    estacoes_g4 = seletor_estacoes_estilo_excel("grafico4", estacoes_disponiveis)
    df_sc = df.dropna(subset=[param_sc_x, param_sc_y])
    if estacoes_g4: df_sc = df_sc[df_sc['ESTACAO_ABA'].isin(estacoes_g4)]

    fig4 = gerar_grafico_flexivel(df_sc, param_sc_x, param_sc_y, tipo_g4, f"Relação entre {param_sc_x} e {param_sc_y}", 'ESTACAO_ABA')
    if fig4: st.plotly_chart(fig4, use_container_width=True)
    else: st.info("Dados insuficientes para cruzar estes parâmetros.")

# --- 8. TABELA DETALHADA ---
if not modo_tv:
    st.markdown("---")
    st.markdown("### 🗃️ Tabela de Dados Operacionais Filtrados")
    st.dataframe(df, use_container_width=True)

