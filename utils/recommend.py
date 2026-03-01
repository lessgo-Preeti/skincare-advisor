from data.ingredients import INGREDIENTS_DB

def analyze_ingredients(ingredients_list, skin_type):
    """
    Analyzes ingredients against user skin type.
    Returns detailed report with safety score and confidence.
    """
    skin_type = skin_type.lower()

    good = []
    caution = []
    bad = []
    unknown = []
    score = 0
    total_scored = 0

    for ingredient in ingredients_list:
        # Normalize ingredient before matching
        normalized = ingredient.strip().lower()

        if normalized in INGREDIENTS_DB:
            rating = INGREDIENTS_DB[normalized][skin_type]
            reason = INGREDIENTS_DB[normalized]["reason"]
            total_scored += 1

            if rating == "good":
                good.append({"name": normalized, "reason": reason})
                score += 2
            elif rating == "caution":
                caution.append({"name": normalized, "reason": reason})
                score -= 1
            elif rating == "bad":
                bad.append({"name": normalized, "reason": reason})
                score -= 2
        else:
            unknown.append(normalized)

    # Safety score — unknown ingredients reduce confidence
    total_ingredients = len(ingredients_list)

    if total_ingredients > 0:
        raw_score = score / (total_ingredients * 2)
        safety_score = round(raw_score * 10, 1)
        safety_score = max(0, min(10, safety_score))
    else:
        safety_score = 0

    # Confidence metric — how many ingredients were matched
    if total_ingredients > 0:
        confidence = round((total_scored / total_ingredients) * 100, 1)
    else:
        confidence = 0

    # Verdict based on safety score
    if safety_score >= 7:
        verdict = "SUITABLE"
        verdict_detail = "This product is safe for your skin type."
    elif safety_score >= 4:
        verdict = "USE WITH CAUTION"
        verdict_detail = "This product has some ingredients that may cause mild reactions."
    elif safety_score >= 2:
        verdict = "RISKY"
        verdict_detail = "This product has several ingredients that may not suit your skin."
    else:
        verdict = "AVOID"
        verdict_detail = "This product contains ingredients harmful for your skin type."

    # Build report
    report = {
        "verdict": verdict,
        "verdict_detail": verdict_detail,
        "safety_score": safety_score,
        "confidence": confidence,
        "skin_type": skin_type,
        "good_ingredients": good,
        "caution_ingredients": caution,
        "bad_ingredients": bad,
        "unknown_ingredients": unknown,
        "total_analyzed": total_ingredients,
        "total_scored": total_scored
    }

    return report