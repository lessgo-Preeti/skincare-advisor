# Skincare Advisor 🌿

AI-powered skincare ingredient analyzer built for Indian skin types.

## Features
- OCR-based ingredient extraction from product images
- Intelligent analysis using spaCy NLP
- 80+ ingredients database including Ayurvedic ingredients
- Per skin type ratings and reasons (Oily, Dry, Combination, Sensitive, Normal)
- Safety score out of 10 with confidence percentage
- PostgreSQL database for analysis history
- REST API with FastAPI
- Premium UI with Streamlit

## Tech Stack
- Python 3.11
- Streamlit (UI)
- EasyOCR + spaCy (OCR & NLP)
- FastAPI + Uvicorn (REST API)
- PostgreSQL (Database)
- AWS EC2 (Deployment)

## Project Structure
```
skincare-advisor/
├── app.py              # Streamlit UI
├── api.py              # FastAPI backend
├── requirements.txt    # Dependencies
├── data/
│   └── ingredients.py  # Ingredient database
└── utils/
    ├── ocr.py          # OCR + NLP processing
    ├── recommend.py    # Scoring logic
    └── database.py     # PostgreSQL connection
```

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/lessgo-Preeti/skincare-advisor.git
cd skincare-advisor
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Setup Environment Variables
Create `.env` file in root folder:
```
DB_HOST=localhost
DB_NAME=skincare_advisor
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

### 5. Setup PostgreSQL
```sql
CREATE DATABASE skincare_advisor;
\c skincare_advisor

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50),
    oily_rating VARCHAR(10),
    oily_reason TEXT,
    dry_rating VARCHAR(10),
    dry_reason TEXT,
    combination_rating VARCHAR(10),
    combination_reason TEXT,
    sensitive_rating VARCHAR(10),
    sensitive_reason TEXT,
    normal_rating VARCHAR(10),
    normal_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analysis_history (
    id SERIAL PRIMARY KEY,
    skin_type VARCHAR(20),
    safety_score FLOAT,
    confidence FLOAT,
    verdict VARCHAR(30),
    total_ingredients INT,
    total_matched INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Run Streamlit App
```bash
streamlit run app.py
```

### 7. Run FastAPI
```bash
uvicorn api:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API status |
| GET | /health | Health check with DB status |
| POST | /analyze | Analyze product image |
| GET | /history | Get analysis history |
| GET | /ingredients | List all ingredients |

## API Usage

### Analyze Product
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@product.jpg" \
  -F "skin_type=oily"
```

### Response
```json
{
  "success": true,
  "verdict": "USE WITH CAUTION",
  "safety_score": 4.1,
  "confidence": 100.0,
  "good_ingredients": [...],
  "caution_ingredients": [...],
  "bad_ingredients": [...]
}
```

## Supported Skin Types
- Oily
- Dry
- Combination
- Sensitive
- Normal

## Indian/Ayurvedic Ingredients Supported
Turmeric, Neem, Sandalwood, Rose Water, Bakuchiol,
Licorice Root, Manjistha, Ashwagandha, Amla, Tulsi,
Multani Mitti, Kasturi Turmeric, Lodhra, Brahmi, Vetiver

## Future Scope
- CNN classifier for product type detection
- Hindi/Tamil OCR support
- React/Flutter mobile app
- Dermatologist verified database
- User accounts and history

## Author
Preeti
Engineering Student | AI/ML Developer
GitHub: https://github.com/lessgo-Preeti
Focus: Indian skincare market & AI solutions
```