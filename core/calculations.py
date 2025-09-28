
def calcular_hse_media(hse_days: list[float]) -> float:
    
    if not hse_days:
        raise ValueError("Lista de HSE está vazia.")
    return sum(hse_days) / len(hse_days)


def calcular_geracao_mensal(demanda_kwh_mes: float, perdas_percentual: float) -> float:
    
    if perdas_percentual >= 100:
        raise ValueError("Perdas não podem ser 100% ou mais.")
    return demanda_kwh_mes / (1 - perdas_percentual / 100)


def calcular_numero_paineis(
    geracao_mensal_ajustada: float,
    hse_media: float,
    potencia_painel_kwp: float
) -> int:
    
    if hse_media <= 0 or potencia_painel_kwp <= 0:
        raise ValueError("HSE média e potência do painel devem ser positivas.")
    energia_mensal_painel = 30 * hse_media * potencia_painel_kwp
    return round(geracao_mensal_ajustada / energia_mensal_painel)
