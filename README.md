# Simulador de Sistema Solar Fotovoltaico 

Este projeto é um **simulador de sistemas fotovoltaicos** desenvolvido em Python com **Streamlit** para interface web, **Plotly** para gráficos interativos e **FPDF** para geração de relatórios em PDF.  

O objetivo é calcular:

- Número de painéis necessários para atender determinada demanda de energia.  
- Geração mensal estimada em kWh.  
- Investimento total e payback do sistema.  

---

## Tecnologias e Bibliotecas

- Python 3.11+  
- [Streamlit](https://streamlit.io/) – Interface web interativa  
- [Plotly](https://plotly.com/python/) – Gráficos interativos  
- [FPDF](https://pyfpdf.github.io/fpdf2/) – Geração de PDFs  
- [Requests](https://docs.python-requests.org/) – Consulta à API NASA POWER  

---

## Estrutura do Projeto
├─ app/
│ ├─ plots/ <- gráficos gerados automaticamente
│ └─ ui_streamlit.py <- interface web
├─ core/
│ ├─ init.py
│ ├─ calculations.py <- cálculos do sistema
│ └─ utils.py <- consulta à API NASA POWER
├─ main.py <- execução em terminal (opcional)
├─ requirements.txt <- dependências
└─ README.md

---

## Como Rodar

### 1. Clonar o repositório

```bash
git clone https://github.com/Vinicius01/Simulador-Solar-Fotovoltaico.git
cd Simulador-Solar-Fotovoltaico

