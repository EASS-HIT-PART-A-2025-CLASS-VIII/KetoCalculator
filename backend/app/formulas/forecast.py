# calculates weight forecast based on TDEE and calorie target
KCAL_PER_KG = 7700.0


def forecast_weight_kg(
    *,
    start_weight_kg: float,
    tdee: float,
    calories_target: float,
    weeks: int = 24,
) -> list[tuple[int, float]]:
    """
    Simple weight projection based on energy balance.

    daily_delta_kcal = calories_target - tdee
      negative -> weight loss
      positive -> weight gain

    delta_kg_per_week ≈ (daily_delta_kcal * 7) / 7700

    Returns list of (week_index, projected_weight_kg), including week 0.
    """
    if start_weight_kg <= 0:
        raise ValueError("start_weight_kg must be > 0")
    if tdee <= 0:
        raise ValueError("tdee must be > 0")
    if calories_target <= 0:
        raise ValueError("calories_target must be > 0")
    if weeks <= 0:
        raise ValueError("weeks must be > 0")

    daily_delta_kcal = calories_target - tdee
    delta_kg_per_week = (daily_delta_kcal * 7.0) / KCAL_PER_KG

    points: list[tuple[int, float]] = [(0, float(start_weight_kg))]
    current = float(start_weight_kg)

    for week in range(1, weeks + 1):
        current = current + delta_kg_per_week
        # Avoid negative projections for extreme deficits
        current = max(0.0, current)
        points.append((week, current))

    return points
