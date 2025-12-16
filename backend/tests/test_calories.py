from app.formulas.calories import calories_target_from_goal
from app.models import Goal


def test_calories_maintain():
    assert calories_target_from_goal(tdee=2500, goal=Goal.maintain) == 2500


def test_calories_lose():
    assert calories_target_from_goal(tdee=2500, goal=Goal.lose) == 2000


def test_calories_gain():
    assert calories_target_from_goal(tdee=2500, goal=Goal.gain) == 3000
