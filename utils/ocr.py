import easyocr
import re
from data.ingredients import SYNONYMS

# Initialize EasyOCR reader - English only
reader = easyocr.Reader(['en'], gpu=False)

# Phrases to filter out from ingredient list
FILTER_PHRASES = [
    "read more",
    "ingredient list",
    "how to read",
    "visit our website",
    "for more information",
    "www.",
    "http",
]

def extract_ingredients(image_path):
    """
    Extracts ingredient list from product image using OCR.
    Returns normalized list of ingredients.
    """
    # Step 1: Extract raw text from image
    results = reader.readtext(image_path, detail=0)
    raw_text = " ".join(results).lower()

    # Step 2: Get text after "ingredients" keyword
    if "ingredients" in raw_text:
        raw_text = raw_text.split("ingredients")[-1]

    # Step 3: Clean text - keep only letters and commas
    cleaned = re.sub(r'[^a-z\s,]', '', raw_text)

    # Step 4: Split by comma to get individual ingredients
    ingredients_list = [i.strip() for i in cleaned.split(",") if i.strip()]

    # Step 5: Filter out non-ingredient phrases and short words
    filtered_list = []
    for ingredient in ingredients_list:
        ingredient = ingredient.strip()

        # Skip very short entries
        if len(ingredient) < 3:
            continue

        # Skip entries containing filter phrases
        should_skip = False
        for phrase in FILTER_PHRASES:
            if phrase in ingredient:
                should_skip = True
                break

        if not should_skip:
            filtered_list.append(ingredient)

    # Step 6: Normalize using synonyms mapping
    normalized = []
    for ingredient in filtered_list:
        ingredient = ingredient.strip().lower()
        if ingredient in SYNONYMS:
            ingredient = SYNONYMS[ingredient]
        normalized.append(ingredient)

    return normalized