# Operational Analytics Dashboard - Streamlit & Plotly
> Dashboard operacional interativo para monitoramento de telemetria e parâmetros de campo, com múltiplos temas visuais e modo TV para centrais de controle.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-blueviolet.svg)

---

## 📌 Visão Geral
Aplicação analítica moderna desenvolvida para transformar dados operacionais dispersos em planilhas em um centro de comando visual em tempo real. Ideal para salas de controle operacional (CCO) e acompanhamento gerencial.

## 🚀 Destaques da Aplicação
- **Múltiplos Temas Visuais:** Suporte dinâmico a 4 paletas de cores refinadas:
  - *Preto & Laranja (Dark)*
  - *Azul Executivo (Dark)*
  - *Roxo Cyber (Dark)*
  - *Clean Moderno (Light)*
- **Modo TV (Full-Screen):** Oculta barras de navegação e controles laterais para exibição limpa em monitores de sala de controle.
- **KPI Cards & Filtros Flexíveis:** Filtragem hierárquica por período, estações e setores operacionais.
- **Modo Demonstração Integrado:** Ao executar sem planilhas locais, o dashboard gera dados sintéticos realistas automaticamente para visualização imediata.

## 🛠️ Como Executar

### 1. Instalação
```bash
pip install streamlit pandas plotly openpyxl numpy
```

### 2. Execução
```bash
streamlit run Dashboard_CGR-GRAFICOS.py
```

O dashboard abrirá automaticamente no seu navegador em `http://localhost:8501`.
