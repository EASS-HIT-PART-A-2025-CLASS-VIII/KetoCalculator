from app.models import Goal


def calories_target_from_goal(*, tdee: float, goal: Goal) -> float:
    """
    Calculate daily calorie target based on goal.

    maintain: 100% TDEE
    lose:      80% TDEE  (-20%)
    gain:     120% TDEE  (+20%)
    """
    if tdee <= 0:
        raise ValueError("tdee must be > 0")

    if goal == Goal.lose:
        return tdee * 0.8
    if goal == Goal.gain:
        return tdee * 1.2
    return tdee
