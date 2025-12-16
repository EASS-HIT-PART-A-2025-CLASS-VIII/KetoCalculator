import pytest

from app.formulas.tdee import calculate_tdee
from app.models import ActivityLevel


def test_tdee_known_value():
    # Example: BMR 1878.75 * 1.55 (moderate) = 2912.0625
    tdee = calculate_tdee(bmr=1878.75, activity_level=ActivityLevel.moderate)
    assert tdee == pytest.approx(2912.0625, abs=1e-6)


def test_tdee_rejects_non_positive_bmr():
    with pytest.raises(ValueError):
        calculate_tdee(bmr=0, activity_level=ActivityLevel.sedentary)
