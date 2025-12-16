from app.models import Goal

NET_CARBS_G = 20.0

PROTEIN_G_PER_KG_BY_GOAL: dict[Goal, float] = {
    Goal.lose: 1.8,
    Goal.maintain: 1.6,
    Goal.gain: 2.2,
}


def calculate_keto_macros(
    *,
    calories_total: float,
    weight_kg: float,
    goal: Goal,
) -> tuple[float, float, float, float]:
    """
    Calculate keto macros based on goal.

    Returns:
        (calories_total, protein_g, fat_g, net_carbs_g)

    Rules:
    - Net carbs fixed at 20g
    - Protein depends on goal
    - Fat fills remaining calories
    """
    if calories_total <= 0:
        raise ValueError("calories_total must be > 0")
    if weight_kg <= 0:
        raise ValueError("weight_kg must be > 0")

    protein_g_per_kg = PROTEIN_G_PER_KG_BY_GOAL[goal]
    protein_g = weight_kg * protein_g_per_kg

    protein_cal = protein_g * 4.0
    carbs_cal = NET_CARBS_G * 4.0

    fat_cal = calories_total - (protein_cal + carbs_cal)
    if fat_cal < 0:
        raise ValueError("Calories too low for keto macro targets.")

    fat_g = fat_cal / 9.0

    return (
        float(calories_total),
        float(protein_g),
        float(fat_g),
        float(NET_CARBS_G),
    )
