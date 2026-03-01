from data.ingredients import INGREDIENTS_DB, SYNONYMS

# Scoring constants
SCORE_GOOD = 2
SCORE_CAUTION = 0
SCORE_BAD = -2

# Verdict thresholds
THRESHOLD_SUITABLE = 7
THRESHOLD_CAUTION = 4
THRESHOLD_RISKY = 2

VALID_SKIN_TYPES = {"oily", "dry", "combination", "sensitive", "normal"}

def analyze_ingredients(ingredients_list, skin_type):
    """
    Analyzes ingredients against user skin type.
    Returns detailed report with safety score and confidence.
    """
    skin_type = skin_type.lower()

    # KeyError protection for invalid skin type
    if skin_type not in VALID_SKIN_TYPES:
        skin_type = "normal"

    good = []
    caution = []
    bad = []
    unknown = []
    score = 0
    total_scored = 0

    # Deduplicate ingredients
    seen = []
    for ingredient in ingredients_list:
        normalized = ingredient.strip().lower()
        if normalized not in seen:
            seen.append(normalized)

    for normalized in seen:
        # Apply synonym mapping
        if normalized in SYNONYMS:
            normalized = SYNONYMS[normalized]

        if normalized in INGREDIENTS_DB:
            # KeyError protection for skin type
            skin_data = INGREDIENTS_DB[normalized].get(skin_type, {})
            rating = skin_data.get("rating", "caution")
            reason = skin_data.get("reason", "No information available")
            total_scored += 1

            if rating == "good":
                good.append({"name": normalized, "reason": reason})
                score += SCORE_GOOD
            elif rating == "caution":
                caution.append({"name": normalized, "reason": reason})
                score += SCORE_CAUTION
            elif rating == "bad":
                bad.append({"name": normalized, "reason": reason})
                score += SCORE_BAD
        else:
            unknown.append(normalized)

    total_ingredients = len(seen)

    # Scoring based on known ingredients only
    if total_scored > 0:
        raw_score = score / (total_scored * 2)
        safety_score = round(raw_score * 10, 1)
        safety_score = max(0, min(10, safety_score))
    else:
        safety_score = 0

    # Confidence metric
    if total_ingredients > 0:
        confidence = round((total_scored / total_ingredients) * 100, 1)
    else:
        confidence = 0

    # Verdict based on safety score
    if safety_score >= THRESHOLD_SUITABLE:
        verdict = "SUITABLE"
        verdict_detail = "This product is safe for your skin type."
    elif safety_score >= THRESHOLD_CAUTION:
        verdict = "USE WITH CAUTION"
        verdict_detail = "This product has some ingredients that may cause mild reactions."
    elif safety_score >= THRESHOLD_RISKY:
        verdict = "RISKY"
        verdict_detail = "This product has several ingredients that may not suit your skin."
    else:
        verdict = "AVOID"
        verdict_detail = "This product contains ingredients harmful for your skin type."

    # Downgrade verdict if confidence is low
    if confidence < 40 and verdict == "SUITABLE":
        verdict = "USE WITH CAUTION"
        verdict_detail = "Low confidence - too many unrecognized ingredients to confirm safety."

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