import pytest

from app.formulas.macros import calculate_keto_macros
from app.models import Goal


def test_macros_maintain():
    cal, protein_g, fat_g, net_carbs_g = calculate_keto_macros(
        calories_total=2800,
        weight_kg=80,
        goal=Goal.maintain,
    )

    assert protein_g == pytest.approx(128.0, abs=1e-9)
    assert net_carbs_g == 20.0

    assert fat_g == pytest.approx(245.333, abs=1e-3)


def test_macros_gain_has_higher_protein():
    cal, protein_g, fat_g, net_carbs_g = calculate_keto_macros(
        calories_total=2800,
        weight_kg=80,
        goal=Goal.gain,
    )

    assert protein_g == pytest.approx(176.0, abs=1e-9)


def test_macros_rejects_too_low_calories():
    with pytest.raises(ValueError):
        calculate_keto_macros(
            calories_total=500,
            weight_kg=80,
            goal=Goal.gain,
        )
