import pytest

from app.formulas.bodyfat import estimate_body_fat_percent_from_bmi
from app.models import Sex


def test_bodyfat_returns_none_for_minors():
    assert estimate_body_fat_percent_from_bmi(bmi=22.0, age_years=17, sex=Sex.male) is None


def test_bodyfat_adult_known_value_male():
    bmi = 80 / (1.8 * 1.8)

    bf = estimate_body_fat_percent_from_bmi(bmi=bmi, age_years=25, sex=Sex.male)

    assert bf == pytest.approx(19.18, abs=0.02)


def test_bodyfat_rejects_bad_bmi():
    with pytest.raises(ValueError):
        estimate_body_fat_percent_from_bmi(bmi=0, age_years=25, sex=Sex.male)
