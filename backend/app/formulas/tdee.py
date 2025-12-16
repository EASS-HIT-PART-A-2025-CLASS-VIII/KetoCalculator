from app.models import ActivityLevel

ACTIVITY_MULTIPLIERS: dict[ActivityLevel, float] = {
    ActivityLevel.sedentary: 1.2,
    ActivityLevel.light: 1.375,
    ActivityLevel.moderate: 1.55,
    ActivityLevel.very: 1.725,
    ActivityLevel.athlete: 1.9,
}


def calculate_tdee(*, bmr: float, activity_level: ActivityLevel) -> float:
    """
    TDEE = BMR * activity_multiplier
    """
    if bmr <= 0:
        raise ValueError("bmr must be > 0")

    multiplier = ACTIVITY_MULTIPLIERS[activity_level]
    return bmr * multiplier
