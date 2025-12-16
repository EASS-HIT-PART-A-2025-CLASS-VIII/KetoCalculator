from app.formulas.forecast import KCAL_PER_KG, forecast_weight_kg


def test_forecast_week0_equals_start():
    pts = forecast_weight_kg(start_weight_kg=80, tdee=2500, calories_target=2500, weeks=4)
    assert pts[0] == (0, 80.0)
    assert len(pts) == 5  # 0..4


def test_forecast_deficit_decreases_weight():
    # 500 kcal/day deficit
    pts = forecast_weight_kg(start_weight_kg=80, tdee=2500, calories_target=2000, weeks=4)
    assert pts[-1][1] < 80.0


def test_forecast_surplus_increases_weight():
    # 300 kcal/day surplus
    pts = forecast_weight_kg(start_weight_kg=80, tdee=2500, calories_target=2800, weeks=4)
    assert pts[-1][1] > 80.0


def test_forecast_expected_weekly_change_math():
    # 7700 kcal deficit over a week -> ~1 kg loss
    pts = forecast_weight_kg(
        start_weight_kg=80, tdee=2500, calories_target=2500 - KCAL_PER_KG / 7, weeks=1
    )
    # one week later should be ~79
    assert abs(pts[1][1] - 79.0) < 1e-6
