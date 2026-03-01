from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
import tempfile
import os
from utils.ocr import extract_ingredients
from utils.recommend import analyze_ingredients
from utils.database import save_analysis, get_analysis_history, get_connection

app = FastAPI(
    title="Skincare Advisor API",
    description="AI-powered skincare ingredient analysis for Indian skin types",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Skincare Advisor API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Health check with real database connection test."""
    conn = get_connection()
    if conn:
        conn.close()
        db_status = "connected"
    else:
        db_status = "disconnected"

    return {
        "status": "healthy",
        "database": db_status
    }

@app.post("/analyze")
async def analyze_product(
    file: UploadFile = File(...),
    skin_type: Literal["oily", "dry", "combination", "sensitive", "normal"] = Form(...)
):
    """
    Analyze skincare product ingredients from image.
    Returns safety score, verdict and ingredient breakdown.
    """
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".jpg"
    ) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        ingredients = extract_ingredients(tmp_path)

        if not ingredients:
            raise HTTPException(
                status_code=422,
                detail="No ingredients detected in image"
            )

        report = analyze_ingredients(ingredients, skin_type)

        save_analysis(
            skin_type=report["skin_type"],
            safety_score=report["safety_score"],
            confidence=report["confidence"],
            verdict=report["verdict"],
            total_ingredients=report["total_analyzed"],
            total_matched=report["total_scored"]
        )

        return {
            "success": True,
            "verdict": report["verdict"],
            "verdict_detail": report["verdict_detail"],
            "safety_score": report["safety_score"],
            "confidence": report["confidence"],
            "skin_type": report["skin_type"],
            "total_analyzed": report["total_analyzed"],
            "total_scored": report["total_scored"],
            "good_ingredients": report["good_ingredients"],
            "caution_ingredients": report["caution_ingredients"],
            "bad_ingredients": report["bad_ingredients"],
            "unknown_ingredients": report["unknown_ingredients"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.get("/history")
def analysis_history():
    """Get past analysis history from database."""
    try:
        history = get_analysis_history()
        return {
            "success": True,
            "total": len(history),
            "history": [dict(h) for h in history]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ingredients")
def list_ingredients():
    """Get all ingredients in database."""
    try:
        from data.ingredients import INGREDIENTS_DB
        return {
            "success": True,
            "total": len(INGREDIENTS_DB),
            "ingredients": list(INGREDIENTS_DB.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

