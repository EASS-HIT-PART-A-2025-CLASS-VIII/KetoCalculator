import pytest

from app.models import ActivityLevel, Sex, UnitSystem, UserInput
from app.units import normalize_inputs


def test_normalize_metric_ok():
    user = UserInput(
        unit_system=UnitSystem.metric,
        sex=Sex.male,
        age_years=30,
        height_cm=175,
        weight_kg=93,
        activity_level=ActivityLevel.moderate,
    )
    norm = normalize_inputs(user)
    assert norm.height_cm == 175
    assert norm.weight_kg == 93


def test_normalize_imperial_ok():
    user = UserInput(
        unit_system=UnitSystem.imperial,
        sex=Sex.male,
        age_years=30,
        height_in=70,  # 5'10"
        weight_lb=205,  # ~93 kg
        activity_level=ActivityLevel.moderate,
    )
    norm = normalize_inputs(user)
    assert norm.height_cm == pytest.approx(177.8, abs=1e-6)
    assert norm.weight_kg == pytest.approx(92.986, abs=1e-3)


def test_normalize_metric_missing_fields_raises():
    user = UserInput(
        unit_system=UnitSystem.metric,
        sex=Sex.male,
        age_years=30,
        activity_level=ActivityLevel.moderate,
    )
    with pytest.raises(ValueError):
        normalize_inputs(user)
