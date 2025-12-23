from app.formulas.forecast import KCAL_PER_KG, forecast_weight_kg


def test_forecast_week0_equals_start():
    pts = forecast_weight_kg(start_weight_kg=80, tdee=2500, calories_target=2500, weeks=4)
    assert pts[0] == (0, 80.0)
    assert len(pts) == 5


def test_forecast_deficit_decreases_weight():
    pts = forecast_weight_kg(start_weight_kg=80, tdee=2500, calories_target=2000, weeks=4)
    assert pts[-1][1] < 80.0


def test_forecast_surplus_increases_weight():
    pts = forecast_weight_kg(start_weight_kg=80, tdee=2500, calories_target=2800, weeks=4)
    assert pts[-1][1] > 80.0


def test_forecast_expected_weekly_change_math():
    pts = forecast_weight_kg(
        start_weight_kg=80, tdee=2500, calories_target=2500 - KCAL_PER_KG / 7, weeks=1
    )
    assert abs(pts[1][1] - 79.0) < 1e-6
