from data.ingredients import INGREDIENTS_DB

def analyze_ingredients(ingredients_list, skin_type):
    """
    Analyzes ingredients against user's skin type
    Returns recommendation report
    """
    skin_type = skin_type.lower()
    
    good = []
    caution = []
    bad = []
    unknown = []

    # Check each ingredient against database
    for ingredient in ingredients_list:
        if ingredient in INGREDIENTS_DB:
            rating = INGREDIENTS_DB[ingredient][skin_type]
            reason = INGREDIENTS_DB[ingredient]["reason"]
            
            if rating == "good":
                good.append({"name": ingredient, "reason": reason})
            elif rating == "caution":
                caution.append({"name": ingredient, "reason": reason})
            elif rating == "bad":
                bad.append({"name": ingredient, "reason": reason})
        else:
            unknown.append(ingredient)

    # Generate final verdict
    if len(bad) > 0:
        verdict = "AVOID"
    elif len(caution) > 0:
        verdict = "USE WITH CAUTION"
    else:
        verdict = "SUITABLE"

    # Build report
    report = {
        "verdict": verdict,
        "skin_type": skin_type,
        "good_ingredients": good,
        "caution_ingredients": caution,
        "bad_ingredients": bad,
        "unknown_ingredients": unknown,
        "total_analyzed": len(ingredients_list)
    }

    return report