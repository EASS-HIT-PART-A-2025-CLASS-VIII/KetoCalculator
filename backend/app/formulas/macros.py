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
    net_carbs_g: float | None = None,
    protein_g_per_kg: float | None = None,
) -> tuple[float, float, float, float]:
    """
    Calculate keto macros based on goal.

    Returns:
        (calories_total, protein_g, fat_g, net_carbs_g)

    Rules:
    - Net carbs defaults to 20g if not specified
    - Protein depends on goal if not specified
    - Fat fills remaining calories
    """
    if calories_total <= 0:
        raise ValueError("calories_total must be > 0")
    if weight_kg <= 0:
        raise ValueError("weight_kg must be > 0")

    # Use provided values or fall back to defaults
    actual_net_carbs = net_carbs_g if net_carbs_g is not None else NET_CARBS_G
    actual_protein_per_kg = (
        protein_g_per_kg if protein_g_per_kg is not None else PROTEIN_G_PER_KG_BY_GOAL[goal]
    )

    protein_g = weight_kg * actual_protein_per_kg

    protein_cal = protein_g * 4.0
    carbs_cal = actual_net_carbs * 4.0

    fat_cal = calories_total - (protein_cal + carbs_cal)
    if fat_cal < 0:
        raise ValueError("Calories too low for keto macro targets.")

    fat_g = fat_cal / 9.0

    return (
        float(calories_total),
        float(protein_g),
        float(fat_g),
        float(actual_net_carbs),
    )
