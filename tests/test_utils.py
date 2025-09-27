import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import get_hse_from_nasa
def test_get_hse_from_nasa():
    lat, lon = -23.55, -46.63

    hse_days, days_in_month = get_hse_from_nasa(lat, lon)

    assert isinstance(hse_days, list), "hse_days não é lista"
    assert isinstance(days_in_month, list),  "days_in_month nao é lista"
    assert len(hse_days) == 12, "hse_days nao tme 12"
    assert len(days_in_month) == 12, "days_in_month nao tem 12"

    for val in hse_days:
        assert isinstance(val, (int, float)), f"valor invalido em hse_days: {val}"
    
    for dias in days_in_month:
        assert isinstance(dias, int)
        assert 28 <= dias <= 31