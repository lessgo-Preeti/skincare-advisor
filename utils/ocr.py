import easyocr
from PIL import Image
import re
from data.ingredients import SYNONYMS

# Initialize EasyOCR reader - English only
reader = easyocr.Reader(['en'], gpu=False)

def extract_ingredients(image_path):
    """
    Extracts ingredient list from product image
    """
    # Step 1: Extract raw text from image
    results = reader.readtext(image_path, detail=0)
    raw_text = " ".join(results).lower()

    # Step 2: Get text after "ingredients:" keyword
    if "ingredients" in raw_text:
        raw_text = raw_text.split("ingredients")[-1]

    # Step 3: Clean text - keep only letters and commas
    cleaned = re.sub(r'[^a-z\s,]', '', raw_text)

    # Step 4: Split by comma to get individual ingredients
    ingredients_list = [i.strip() for i in cleaned.split(",") if i.strip()]

    # Step 5: Normalize using synonyms mapping
    normalized = []
    for ingredient in ingredients_list:
        ingredient = ingredient.strip()
        if ingredient in SYNONYMS:
            ingredient = SYNONYMS[ingredient]
        normalized.append(ingredient)

    return normalized