import builtins
import pytest
from unittest.mock import patch
from main import main

def test_main_calculo_basico(capsus):
    entrada = iter([
       "-23.55",   # lat
        "-46.63",   # lon
        "300",      # consumo kWh/mês
        "400",      # potência painel W
        "1000",     # preço painel R$
        "1.0",      # cobertura 100%
        "0.7",      # tarifa R$/kWh
        "0.1",      # perdas 10%
    ])

def fake_input(promp = ""):
    return next(entradas)

fake_hse = ([5]*12, [30]*12)

with patch.object(builtins, "input", fake_input), \
     patch("main.get_hse_from_nasa", return_value=fake_hse):
    
    main()

saida = capsys.readouterr().out

assert "n° de paineis necessario" in saida
assert "Geração média mensal" in saida
assert "Investimento total" in saida
assert "Payback" in saida
