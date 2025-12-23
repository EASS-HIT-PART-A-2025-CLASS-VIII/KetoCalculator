from app.models import Sex


def estimate_body_fat_percent_from_bmi(*, bmi: float, age_years: int, sex: Sex) -> float | None:
    """
    Approximate body fat % estimate using BMI, age, and sex.

    IMPORTANT:
    - This is a rough estimate and not a medical measurement.
    - For minors (<18), returns None (we do not estimate in this milestone).

    Uses a commonly-cited BMI-based estimation model (adult-oriented).
    """
    if age_years < 18:
        return None
    if bmi <= 0:
        raise ValueError("bmi must be > 0")

    sex_bit = 1 if sex == Sex.male else 0
    bf = 1.20 * bmi + 0.23 * age_years - 10.8 * sex_bit - 5.4

    return max(0.0, min(75.0, bf))
