import pytest

from app.formulas.bmr import calculate_bmr_mifflin_st_jeor
from app.models import Sex


def test_bmr_male_known_value():
    # Example: male, 30y, 175cm, 93kg
    # base = 10*93 + 6.25*175 - 5*30 = 930 + 1093.75 - 150 = 1873.75
    # +5 => 1878.75
    bmr = calculate_bmr_mifflin_st_jeor(sex=Sex.male, age_years=30, height_cm=175, weight_kg=93)
    assert bmr == pytest.approx(1878.75, abs=1e-6)


def test_bmr_female_known_value():
    # same inputs but female: 1873.75 - 161 = 1712.75
    bmr = calculate_bmr_mifflin_st_jeor(sex=Sex.female, age_years=30, height_cm=175, weight_kg=93)
    assert bmr == pytest.approx(1712.75, abs=1e-6)


def test_bmr_rejects_minors_for_now():
    with pytest.raises(ValueError):
        calculate_bmr_mifflin_st_jeor(sex=Sex.male, age_years=17, height_cm=175, weight_kg=93)


def test_bmr_rejects_bad_inputs():
    with pytest.raises(ValueError):
        calculate_bmr_mifflin_st_jeor(sex=Sex.male, age_years=30, height_cm=0, weight_kg=93)
    with pytest.raises(ValueError):
        calculate_bmr_mifflin_st_jeor(sex=Sex.male, age_years=30, height_cm=175, weight_kg=0)
