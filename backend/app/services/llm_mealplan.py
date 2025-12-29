import os

from google import genai
from google.genai import errors
from google.genai.types import GenerateContentConfig

from app.models import CalcOutput, UserInput
from app.models_mealplan import MealPlanResponse

SCHEMA_EXAMPLE = (
    '{"generated_mealplan":[{"meals":[{"meal_name":"lunch","items":[{"name":"chicken breast",'
    '"grams":200,"notes":"grilled"}],"protein_g":0,"fat_g":0,"net_carbs_g":0,"calories":0}],'
    '"totals":{"meal_name":"totals","items":[],"protein_g":0,"fat_g":0,"net_carbs_g":0,'
    '"calories":0}}],"shopping_list":["..."],"assumptions":["..."]}'
)


def _mealplan_pref_lines(user: UserInput) -> list[str]:
    mp = user.mealplan
    lines: list[str] = [
        f"- Number of days: {mp.days}",
        f"- Meals per day: {mp.meals_per_day} ({'OMAD' if mp.meals_per_day == 1 else 'standard'})",
        "- Each day MUST contain exactly `meals_per_day` meals.",
        "- Generate exactly `days` days in the meal plan.",
        "- Use these meal_name values:",
    ]

    if mp.meals_per_day == 1:
        lines.append('  - "meal"')
    else:
        base = ['"breakfast"', '"lunch"', '"dinner"', '"snack"', '"snack2"', '"snack3"']
        lines.append("  - " + ", ".join(base[: mp.meals_per_day]))

    return lines


def _dietary_lines(user: UserInput) -> list[str]:
    prefs = user.dietary

    rules: list[str] = []
    if prefs.vegan:
        rules.append("- Must be VEGAN (no meat, fish, eggs, dairy, honey).")
    elif prefs.vegetarian:
        rules.append("- Must be VEGETARIAN (no meat or fish).")

    if prefs.kosher:
        rules.append("- Must be KOSHER (no pork/shellfish; do not mix meat and dairy).")

    if prefs.halal:
        rules.append("- Must be HALAL (no pork/alcohol; halal meat only if meat is included).")

    if not rules:
        rules.append("- No special dietary restrictions.")

    return rules


def build_prompt(user: UserInput, calc: CalcOutput) -> str:
    dietary_rules = _dietary_lines(user)
    mealplan_rules = _mealplan_pref_lines(user)

    return "\n".join(
        [
            "You are a nutrition assistant. Create a keto meal plan.",
            "",
            "Rules:",
            f"- Net carbs target: {calc.macros.net_carbs_g:.0f}g/day",
            f"- Protein target: {calc.macros.protein_g:.0f}g/day",
            f"- Fat target: {calc.macros.fat_g:.0f}g/day",
            f"- Calories target: {calc.macros.calories_total:.0f} kcal/day",
            *mealplan_rules,
            "- Output MUST be valid JSON that matches this schema exactly:",
            SCHEMA_EXAMPLE,
            "",
            "Constraints:",
            "- Do not include raw newlines inside string values; use \\n if needed.",
            "- Ensure all strings are double-quoted and properly escaped.",
            "- Output compact JSON on a single line (no pretty formatting).",
            "- Use common foods; include grams for each item.",
            "- Limit each meal to at most 3 items.",
            "- Avoid alcohol.",
            "- Keep it simple.",
            "- Each day should be different; avoid repeating the same meals/items.",
            "- Net carbs per day MUST be <= 20g.",
            "- Protein per day MUST be >= the target.",
            "- Calories per day can be up to 5% off the target (within ±5% of target).",
            "- Meals should be realistic: combine a protein + vegetable + fat/sauce.",
            "- Snacks should be snack-like (e.g., olives, nuts, dark chocolate).",
            "- If user is imperial, you can still output grams (preferred).",
            *dietary_rules,
            "- Return JSON only. No markdown, no extra text.",
        ]
    )


def _check_truncation(resp: object) -> bool:
    """Check if the response was truncated by examining finish_reason."""
    try:
        candidates = getattr(resp, "candidates", None) or []
        if candidates:
            finish_reason = getattr(candidates[0], "finish_reason", None)
            # MAX_TOKENS indicates truncation
            if finish_reason == "MAX_TOKENS" or str(finish_reason) == "MAX_TOKENS":
                return True
    except Exception:
        pass
    return False


def generate_meal_plan(user: UserInput, calc: CalcOutput) -> MealPlanResponse:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    client = genai.Client()
    prompt = build_prompt(user, calc)

    # Use maximum allowed tokens for Gemini 2.5 Flash (8192)
    # This should be sufficient for up to 7 days with 6 meals per day
    max_tokens = 8192

    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MealPlanResponse,
                max_output_tokens=max_tokens,
            ),
        )

        # Check if response was truncated
        if _check_truncation(resp):
            raise RuntimeError(
                f"Response was truncated (max_output_tokens={max_tokens} may be too low). "
                "Try reducing the number of days or meals per day."
            )

        parsed = _get_parsed_response(resp)
        if parsed is not None:
            if isinstance(parsed, MealPlanResponse):
                return parsed
            return MealPlanResponse.model_validate(parsed)
        text = _response_text(resp)
        json_text = _extract_json(text)

        # Check if JSON appears truncated (doesn't end properly)
        if json_text and not json_text.rstrip().endswith("}"):
            raise RuntimeError(
                f"Response appears to be truncated. JSON doesn't end properly. "
                f"Preview (last 200 chars): {text[-200:] if len(text) > 200 else text}"
            )

        try:
            return MealPlanResponse.model_validate_json(json_text)
        except Exception as e:
            preview = text[:500] if text else ""
            raise RuntimeError(
                f"LLM returned invalid JSON. "
                f"This may indicate truncation (max_output_tokens={max_tokens}). "
                f"Preview: {preview}"
            ) from e

    except errors.APIError as e:
        if getattr(e, "status_code", None) == 429:
            raise RuntimeError(f"RATE_LIMIT:{e}") from e
        raise RuntimeError(f"Gemini API error: {e}") from e


def _extract_json(text: str) -> str:
    t = text.strip()

    if t.startswith("```"):
        t = t.strip("`").strip()
        if t.lower().startswith("json"):
            t = t[4:].strip()

    start = t.find("{")
    end = t.rfind("}")
    if start != -1 and end != -1 and end > start:
        return t[start : end + 1]

    return t


def _get_parsed_response(resp: object) -> object | None:
    parsed = getattr(resp, "parsed", None)
    if parsed is not None:
        return parsed

    try:
        candidates = getattr(resp, "candidates", None) or []
        if candidates:
            content = getattr(candidates[0], "content", None)
            parts = getattr(content, "parts", None) or []
            for part in parts:
                part_parsed = getattr(part, "parsed", None)
                if part_parsed is not None:
                    return part_parsed
    except Exception:
        return None

    return None


def _response_text(resp: object) -> str:
    text = getattr(resp, "text", None)
    if text:
        return text
    try:
        candidates = getattr(resp, "candidates", None) or []
        if candidates:
            content = getattr(candidates[0], "content", None)
            parts = getattr(content, "parts", None) or []
            combined: list[str] = []
            for part in parts:
                part_text = getattr(part, "text", None)
                if part_text:
                    combined.append(part_text)
            if combined:
                return "".join(combined)
    except Exception:
        return ""
    return ""
