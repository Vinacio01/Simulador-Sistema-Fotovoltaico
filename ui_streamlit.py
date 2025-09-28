import streamlit as st
from main import calcular_sistema
from core.utils import get_hse_from_nasa
import plotly.graph_objects as go
from fpdf import FPDF
import plotly.io as pio
import os


usuarios = {"teste@teste.com": "1234"}


if "logado" not in st.session_state:
    st.session_state.logado = False
if "email" not in st.session_state:
    st.session_state.email = ""


if not st.session_state.logado:
    st.title("🔒 Login")
    email_input = st.text_input("Email")
    senha_input = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email_input in usuarios and usuarios[email_input] == senha_input:
            st.session_state.logado = True
            st.session_state.email = email_input
            st.success("Login bem-sucedido!")
        else:
            st.error("Email ou senha incorretos!")


if st.session_state.logado:
    st.success(f"Bem-vindo! Usuário logado: {st.session_state.email}")

    st.markdown("<h1 style='text-align: center; color: #1F4E79;'>Simulador de Sistema Fotovoltaico</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#333;'>Calcule número de painéis, investimento e payback do seu sistema solar</p>", unsafe_allow_html=True)
    st.markdown("---")


    st.subheader("Dados do local e consumo")
    lat = st.number_input("Latitude do local", value=-23.550000, format="%.6f", step=0.000001)
    lon = st.number_input("Longitude do local", value=-46.630000, format="%.6f", step=0.000001)
    demanda = st.number_input("Consumo médio mensal (kWh)", value=300.0, step=1.0)

    st.subheader("Dados do sistema fotovoltaico")
    potencia_painel = st.number_input("Potência de cada painel (W)", value=400.0, step=1.0)
    preco_painel = st.number_input("Preço de cada painel (R$)", value=1000.0, step=1.0)
    cobertura = st.number_input("Cobertura da demanda (0 a 1)", value=1.0, min_value=0.0, max_value=1.0, step=0.01)
    tarifa = st.number_input("Custo médio da energia (R$/kWh)", value=0.9, step=0.01)
    perdas = st.number_input("Perdas do sistema (fração, ex: 0.2 para 20%)", value=0.2, min_value=0.0, max_value=1.0, step=0.01)
    st.markdown("---")

    
    def gerar_pdf(resultados, fig_geracao, fig_invest):
        
        os.makedirs("app/plots", exist_ok=True)

        
        for arquivo in os.listdir("app/plots"):
            caminho = os.path.join("app/plots", arquivo)
            if os.path.isfile(caminho):
                os.remove(caminho)

        
        caminho_geracao = "app/plots/geracao.png"
        caminho_invest = "app/plots/invest.png"
        pio.write_image(fig_geracao, caminho_geracao, scale=2)
        pio.write_image(fig_invest, caminho_invest, scale=2)

        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 18)
        pdf.cell(0, 10, "Relatório do Sistema Fotovoltaico", ln=True, align="C")

        pdf.set_font("Arial", '', 12)
        for key, value in resultados.items():
            pdf.ln(5)
            pdf.cell(0, 10, f"{key}: {value}", ln=True)

        pdf.ln(10)
        pdf.image(caminho_geracao, w=180)
        pdf.ln(10)
        pdf.image(caminho_invest, w=180)

        pdf.set_y(-20)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, "Projeto criado por Vinicius Consorte Vieira", 0, 0, 'C')

        arquivo_pdf = "relatorio_solar.pdf"
        pdf.output(arquivo_pdf)
        return arquivo_pdf

    
    if st.button("📄 Gerar Relatório"):
        
        num_paineis, media_geracao, investimento, payback = calcular_sistema(
            lat, lon, demanda, potencia_painel, preco_painel,
            cobertura, tarifa, perdas
        )

        
        st.subheader("Resultados do Relatório")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Número de painéis", value=num_paineis)
            st.metric(label="Geração média mensal (kWh)", value=f"{media_geracao:.1f}")
        with col2:
            st.metric(label="Investimento total (R$)", value=f"{investimento:.2f}")
            st.metric(label="Payback (anos)", value=f"{payback:.1f}")

        
        try:
            hse_days, days_in_month = get_hse_from_nasa(lat, lon)
        except Exception as e:
            st.warning(f"Falha ao consultar NASA POWER. Usando valores padrão: {e}")
            hse_days = [5]*12
            days_in_month = [30,31]*6

        potencia_painel_kw = potencia_painel / 1000
        pr = 1 - perdas
        geracao_mensal = [round(hse_days[i]*days_in_month[i]*potencia_painel_kw*pr,2) for i in range(12)]
        meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

        
        fig1 = go.Figure(data=go.Bar(x=meses, y=geracao_mensal, marker_color='#FFA500'))
        fig1.update_layout(
            yaxis_title="kWh",
            xaxis_title="Mês",
            template="plotly_white",
            title="Geração Mensal Estimada",
            title_x=0.5
        )
        st.plotly_chart(fig1, use_container_width=True)

        
        economia_mensal = [media_geracao * tarifa] * 12
        economia_acumulada = [sum(economia_mensal[:i+1]) for i in range(12)]
        investimento_total = investimento

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=meses,
            y=[investimento_total]*12,
            name="Investimento Total",
            marker_color="#D61207",
            opacity=0.6
        ))
        fig2.add_trace(go.Scatter(
            x=meses,
            y=economia_acumulada,
            name="Economia Acumulada",
            mode='lines+markers',
            line=dict(color='#2ECC40', width=4),
            marker=dict(size=8)
        ))
        fig2.update_layout(
            yaxis_title="R$",
            xaxis_title="Mês",
            template="plotly_white",
            legend=dict(x=0.7, y=0.95),
            title="Investimento vs Economia Acumulada",
            title_x=0.5
        )
        st.plotly_chart(fig2, use_container_width=True)

       
        resultados = {
            "Número de painéis": num_paineis,
            "Geração média mensal (kWh)": f"{media_geracao:.1f}",
            "Investimento total (R$)": f"{investimento:.2f}",
            "Payback (anos)": f"{payback:.1f}"
        }
        arquivo_pdf = gerar_pdf(resultados, fig1, fig2)
        st.success("PDF gerado com sucesso!")
        with open(arquivo_pdf, "rb") as f:
            st.download_button(
                label="⬇️ Baixar Relatório PDF",
                data=f,
                file_name=arquivo_pdf,
                mime="application/pdf"
            )

   
    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size:12px; color:gray;'>Projeto criado por Vinicius Consorte Vieira</p>", unsafe_allow_html=True)
