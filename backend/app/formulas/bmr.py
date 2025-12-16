from app.models import Sex


def calculate_bmr_mifflin_st_jeor(
    *, sex: Sex, age_years: int, height_cm: float, weight_kg: float
) -> float:
    """
    Basal Metabolic Rate (BMR) using Mifflin–St Jeor equation.

    Notes:
    - Commonly used for adults.
    - For minors (<18), we intentionally raise an error in this milestone to avoid
      applying adult equations without validated references.

    Formula (kcal/day):
      Men:    10*kg + 6.25*cm - 5*age + 5
      Women:  10*kg + 6.25*cm - 5*age - 161
    """
    if age_years < 18:
        raise ValueError("BMR formula not supported for minors (<18) yet.")
    if weight_kg <= 0:
        raise ValueError("weight_kg must be > 0")
    if height_cm <= 0:
        raise ValueError("height_cm must be > 0")
    if age_years <= 0:
        raise ValueError("age_years must be > 0")

    base = 10.0 * weight_kg + 6.25 * height_cm - 5.0 * age_years
    if sex == Sex.male:
        return base + 5.0
    return base - 161.0
