from core.utils import get_hse_from_nasa

def main():
    print("=== Simulador de Sistema Solar Fotovoltaico ===\n")

    lat = float(input("Latitude do local (ex: -23.55): "))
    lon = float(input("Longitude do local (ex: -46.63): "))
    demanda = float(input("Consumo médio mensal (kWh): "))
    potencia_painel = float(input("Potência de cada painel (W): "))
    preco_painel = float(input("Preço de cada painel (R$): "))
    cobertura = float(input("Cobertura da demanda (ex: 1.0 = 100%, 0.8 = 80%): "))
    tarifa = float(input("Tarifa de energia (R$/kWh): "))
    perdas = float(input("Perdas totais do sistema (fração, ex: 0.2 para 20%): "))

    pr = 1 - perdas
    if pr <= 0 or pr > 1:
        raise ValueError("As perdas devem resultar em um fator entre 0 e 1.")

    print("Consultando dados da NASA POWER ...")
    try:
        hse_days, days_in_month = get_hse_from_nasa(lat, lon)
    except Exception as e:
        print(f"Falha ao consultar NASA POWER: {e}")
        hse_days = [5]*12
        days_in_month = [30,31,30,31,30,31,30,31,30,31,30,31]

    # Geração mensal de um painel (kWh)
    potencia_painel_kw = potencia_painel / 1000
    geracao_mensal = []
    for mes in range(12):
        energia_mes = hse_days[mes] * days_in_month[mes] * potencia_painel_kw * pr
        geracao_mensal.append(round(energia_mes, 2))

    # Média e quantidade de painéis
    media_geracao_mensal = sum(geracao_mensal) / 12
    demanda_ajustada = demanda * cobertura
    num_paineis = int(-(-demanda_ajustada // media_geracao_mensal))  # teto

    # Investimento e payback
    investimento = num_paineis * preco_painel
    economia_mensal = media_geracao_mensal * tarifa * num_paineis
    payback = investimento / economia_mensal if economia_mensal > 0 else float('inf')

    # Resultado final
    print("\n=== Resultado da Simulação ===")
    print(f"Nº de painéis necessários : {num_paineis}")
    print(f"Geração média mensal (kWh): {media_geracao_mensal:.1f}")
    print(f"Investimento total (R$)   : {investimento:.2f}")
    print(f"Payback (anos)            : {payback:.1f}")

if __name__ == "__main__":
    main()
