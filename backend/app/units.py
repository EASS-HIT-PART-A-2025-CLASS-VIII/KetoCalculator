from dataclasses import dataclass

from .models import UnitSystem, UserInput

LB_TO_KG = 0.45359237
IN_TO_CM = 2.54


@dataclass(frozen=True)
class NormalizedInputs:
    sex: str
    age_years: int
    height_cm: float
    weight_kg: float
    activity_level: str
    net_carbs_g: float
    protein_g_per_kg: float


def normalize_inputs(user: UserInput) -> NormalizedInputs:
    if user.unit_system == UnitSystem.metric:
        if user.height_cm is None or user.weight_kg is None:
            raise ValueError("For metric input, height_cm and weight_kg are required.")
        height_cm = user.height_cm
        weight_kg = user.weight_kg
    else:
        if user.height_in is None or user.weight_lb is None:
            raise ValueError("For imperial input, height_in and weight_lb are required.")
        height_cm = user.height_in * IN_TO_CM
        weight_kg = user.weight_lb * LB_TO_KG

    return NormalizedInputs(
        sex=user.sex.value,
        age_years=user.age_years,
        height_cm=float(height_cm),
        weight_kg=float(weight_kg),
        activity_level=user.activity_level.value,
        net_carbs_g=float(user.net_carbs_g),
        protein_g_per_kg=float(user.protein_g_per_kg),
    )
