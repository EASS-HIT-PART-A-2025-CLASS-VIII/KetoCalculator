import pytest

from app.formulas.ffmi import calculate_ffmi


def test_ffmi_none_when_bodyfat_none():
    assert calculate_ffmi(weight_kg=80, height_cm=180, body_fat_percent=None) is None


def test_ffmi_known_value():
    ffmi = calculate_ffmi(weight_kg=80, height_cm=180, body_fat_percent=19.18)

    assert ffmi == pytest.approx(19.95, abs=0.05)


def test_ffmi_rejects_invalid_bodyfat():
    with pytest.raises(ValueError):
        calculate_ffmi(weight_kg=80, height_cm=180, body_fat_percent=120)
