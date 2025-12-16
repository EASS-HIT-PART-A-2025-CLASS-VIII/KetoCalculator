import pytest

from app.formulas.macros import calculate_keto_macros
from app.models import Goal


def test_macros_maintain():
    # Subject: 80kg, maintain, calories 2800
    cal, protein_g, fat_g, net_carbs_g = calculate_keto_macros(
        calories_total=2800,
        weight_kg=80,
        goal=Goal.maintain,
    )

    # Protein: 1.6 * 80 = 128g
    assert protein_g == pytest.approx(128.0, abs=1e-9)
    assert net_carbs_g == 20.0

    # Protein+carbs calories = 128*4 + 20*4 = 512 + 80 = 592
    # Remaining = 2208 → fat = 245.333...
    assert fat_g == pytest.approx(245.333, abs=1e-3)


def test_macros_gain_has_higher_protein():
    cal, protein_g, fat_g, net_carbs_g = calculate_keto_macros(
        calories_total=2800,
        weight_kg=80,
        goal=Goal.gain,
    )

    # Protein: 2.2 * 80 = 176g
    assert protein_g == pytest.approx(176.0, abs=1e-9)


def test_macros_rejects_too_low_calories():
    with pytest.raises(ValueError):
        calculate_keto_macros(
            calories_total=500,
            weight_kg=80,
            goal=Goal.gain,
        )
