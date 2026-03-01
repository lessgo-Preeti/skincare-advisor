import easyocr
import re
import spacy
from data.ingredients import SYNONYMS

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Load spaCy English model
nlp = spacy.load('en_core_web_sm')

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

def clean_with_spacy(text):
    """
    Uses spaCy NLP to extract meaningful ingredient tokens.
    Removes stop words, punctuation, and irrelevant tokens.
    Returns cleaned ingredient text.
    """
    doc = nlp(text)
    
    cleaned_tokens = []
    for token in doc:
        # Skip stop words like "and", "the", "or"
        if token.is_stop:
            continue
        # Skip pure punctuation
        if token.is_punct:
            continue
        # Skip very short tokens
        if len(token.text.strip()) < 2:
            continue
        # Skip numbers only
        if token.is_digit:
            continue
        cleaned_tokens.append(token.text.lower().strip())
    
    return " ".join(cleaned_tokens)

def extract_ingredients(image_path):
    """
    Extracts ingredient list from product image using OCR and spaCy NLP.
    Returns normalized list of ingredients.
    """
    # Step 1: Extract raw text from image using EasyOCR
    results = reader.readtext(image_path, detail=0)
    raw_text = " ".join(results).lower()

    # Step 2: Get text after "ingredients" keyword
    if "ingredients" in raw_text:
        raw_text = raw_text.split("ingredients")[-1]

    # Step 3: Clean text - keep only letters and commas
    cleaned = re.sub(r'[^a-z\s,]', '', raw_text)

    # Step 4: Split by comma to get individual ingredients
    raw_ingredients = [i.strip() for i in cleaned.split(",") if i.strip()]

    # Step 5: Filter out non-ingredient phrases
    filtered_list = []
    for ingredient in raw_ingredients:
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

    # Step 6: Apply spaCy NLP processing for better matching
    normalized = []
    for ingredient in filtered_list:
        ingredient = ingredient.strip().lower()

        # Check direct match first
        if ingredient in SYNONYMS:
            ingredient = SYNONYMS[ingredient]
            normalized.append(ingredient)
            continue

        # Apply spaCy cleaning for better matching
        spacy_cleaned = clean_with_spacy(ingredient)
        
        # Check if spaCy cleaned version matches synonyms
        if spacy_cleaned in SYNONYMS:
            normalized.append(SYNONYMS[spacy_cleaned])
        else:
            normalized.append(ingredient)

    return normalized