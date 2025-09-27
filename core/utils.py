import requests
import calendar

"""
Consulta a API NASA POWER e retorna:
"""

def get_hse_from_nasa(lat: float, lon: float, year = 2025):
    url = (
        "https://power.larc.nasa.gov/api/temporal/climatology/point"
        f"?parameters=ALLSKY_SFC_SW_DWN"
        f"&community=RE"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&format=JSON"
    )

    resp = requests.get(url, timeout=20)
    resp.raise_for_status() # lança um erro se a requisição falhar

    data = resp.json()
    monthly = data.get("properties", {}).get("parameter", {}).get("ALLSKY_SFC_SW_DWN")
    if not monthly:
        raise ValueError("Resposta da NASA POWER não contém ALLSKY_SFC_SW_DWN")

# NASA devolve um dicionário com meses como strings 'JAN'
    monthly = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]

# Converte para lista ordenada de Jan a Dez
    months_order = ["JAN","FEB","MAR","APR","MAY","JUN",
                    "JUL","AUG","SEP","OCT","NOV","DEC"]
    hse_days = [monthly[m] for m in months_order]

#Calcula dias de cada mes 
    days_in_month = [calendar.monthrange(year, i+1)[1] for i in range(12)]

    return hse_days, days_in_month
