import streamlit as st
from PIL import Image
import tempfile
import os
from utils.ocr import extract_ingredients
from utils.recommend import analyze_ingredients
from utils.database import save_analysis

st.set_page_config(
    page_title="Skincare Advisor",
    layout="centered"
)

# Premium CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=DM+Sans:wght@300;400;500&display=swap');

* {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1208 50%, #0f0f0f 100%);
    min-height: 100vh;
}

.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem;
    font-weight: 300;
    color: #c9a84c;
    letter-spacing: 0.08em;
    text-align: center;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}

.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 300;
    color: #8a7a5a;
    letter-spacing: 0.25em;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.divider {
    width: 60px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
    margin: 1rem auto 2rem auto;
}

.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    color: #c9a84c;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.verdict-box {
    padding: 1.5rem 2rem;
    border-radius: 4px;
    text-align: center;
    margin: 1rem 0;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    font-weight: 400;
    letter-spacing: 0.15em;
}

.verdict-suitable {
    background: rgba(26, 74, 44, 0.3);
    border: 1px solid #2d6b3e;
    color: #6fcf8a;
}

.verdict-caution {
    background: rgba(74, 58, 12, 0.3);
    border: 1px solid #8a6e1a;
    color: #f0c040;
}

.verdict-risky {
    background: rgba(74, 40, 12, 0.3);
    border: 1px solid #8a4a1a;
    color: #f09040;
}

.verdict-avoid {
    background: rgba(74, 20, 20, 0.3);
    border: 1px solid #8a2020;
    color: #f06060;
}

.verdict-detail {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 300;
    color: #8a7a5a;
    text-align: center;
    font-style: italic;
    margin-top: 0.5rem;
}

.score-card {
    background: rgba(201, 168, 76, 0.05);
    border: 1px solid rgba(201, 168, 76, 0.15);
    border-radius: 4px;
    padding: 1.2rem;
    text-align: center;
}

.score-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 300;
    color: #c9a84c;
    line-height: 1;
}

.score-label {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6a5a3a;
    margin-top: 0.3rem;
}

.ingredient-card-good {
    background: rgba(26, 74, 44, 0.15);
    border-left: 2px solid #2d6b3e;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    border-radius: 0 4px 4px 0;
}

.ingredient-card-caution {
    background: rgba(74, 58, 12, 0.15);
    border-left: 2px solid #8a6e1a;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    border-radius: 0 4px 4px 0;
}

.ingredient-card-bad {
    background: rgba(74, 20, 20, 0.15);
    border-left: 2px solid #8a2020;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    border-radius: 0 4px 4px 0;
}

.ingredient-name {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    font-weight: 500;
    color: #e8d5a0;
    text-transform: capitalize;
}

.ingredient-reason {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 300;
    color: #7a6a4a;
    margin-top: 0.2rem;
}

.section-header {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    font-weight: 400;
    letter-spacing: 0.1em;
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(201, 168, 76, 0.15);
}

.section-header-good { color: #6fcf8a; }
.section-header-caution { color: #f0c040; }
.section-header-bad { color: #f06060; }
.section-header-unknown { color: #8a7a5a; }

.unknown-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 4px;
    padding: 0.8rem 1rem;
    font-size: 0.78rem;
    color: #6a5a3a;
    line-height: 1.6;
}

.footer-text {
    font-size: 0.7rem;
    color: #4a3a2a;
    text-align: center;
    letter-spacing: 0.1em;
    margin-top: 2rem;
}

.stSelectbox label, .stFileUploader label {
    font-size: 0.7rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #c9a84c !important;
}

.stButton button {
    background: transparent !important;
    border: 1px solid #c9a84c !important;
    color: #c9a84c !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 2.5rem !important;
    border-radius: 2px !important;
    width: 100% !important;
}

div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #c9a84c, #e8d5a0) !important;
}
</style>
""", unsafe_allow_html=True)

# Hero section
st.markdown('<div class="hero-title">Skincare Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Intelligent Ingredient Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Skin type selection
st.markdown('<div class="section-label">Your Skin Type</div>', unsafe_allow_html=True)
skin_type = st.selectbox(
    "",
    ["Oily", "Dry", "Combination", "Sensitive", "Normal"],
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# Image upload
st.markdown('<div class="section-label">Product Image</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, width=500)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Analyze Product"):
        with st.spinner("Analyzing..."):

            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".jpg"
            ) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            try:
                ingredients = extract_ingredients(tmp_path)
                if ingredients:
                    report = analyze_ingredients(ingredients, skin_type)
                    st.session_state["report"] = report
                    st.session_state["ingredients"] = ingredients

                    # Save to database
                    save_analysis(
                        skin_type=report["skin_type"],
                        safety_score=report["safety_score"],
                        confidence=report["confidence"],
                        verdict=report["verdict"],
                        total_ingredients=report["total_analyzed"],
                        total_matched=report["total_scored"]
                    )
                else:
                    st.session_state["report"] = None
                    st.session_state["ingredients"] = []
            except Exception as e:
                st.error("OCR processing failed. Please try a clearer image.")
                st.session_state["report"] = None
                st.session_state["ingredients"] = []
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

# Display results from session state
if st.session_state.get("report"):
    report = st.session_state["report"]
    verdict = report["verdict"]

    if not st.session_state.get("ingredients"):
        st.error("Could not detect ingredients. Please upload a clearer image.")
    else:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        verdict_class = {
            "SUITABLE": "verdict-suitable",
            "USE WITH CAUTION": "verdict-caution",
            "RISKY": "verdict-risky",
            "AVOID": "verdict-avoid"
        }.get(verdict, "verdict-caution")

        st.markdown(
            f'<div class="verdict-box {verdict_class}">{verdict}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="verdict-detail">{report["verdict_detail"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
                <div class="score-card">
                    <div class="score-value">{report["safety_score"]}</div>
                    <div class="score-label">Safety Score</div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
                <div class="score-card">
                    <div class="score-value">{report["confidence"]}%</div>
                    <div class="score-label">Confidence</div>
                </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
                <div class="score-card">
                    <div class="score-value">{report["total_analyzed"]}</div>
                    <div class="score-label">Ingredients</div>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(report["safety_score"] / 10)
        st.markdown("<br>", unsafe_allow_html=True)

        col4, col5, col6 = st.columns(3)
        with col4:
            st.markdown(f'''
                <div class="score-card">
                    <div class="score-value" style="color:#6fcf8a">{len(report["good_ingredients"])}</div>
                    <div class="score-label">Beneficial</div>
                </div>
            ''', unsafe_allow_html=True)
        with col5:
            st.markdown(f'''
                <div class="score-card">
                    <div class="score-value" style="color:#f0c040">{len(report["caution_ingredients"])}</div>
                    <div class="score-label">Caution</div>
                </div>
            ''', unsafe_allow_html=True)
        with col6:
            st.markdown(f'''
                <div class="score-card">
                    <div class="score-value" style="color:#f06060">{len(report["bad_ingredients"])}</div>
                    <div class="score-label">Avoid</div>
                </div>
            ''', unsafe_allow_html=True)

        if report["good_ingredients"]:
            st.markdown(
                '<div class="section-header section-header-good">Beneficial Ingredients</div>',
                unsafe_allow_html=True
            )
            for item in report["good_ingredients"]:
                st.markdown(f'''
                    <div class="ingredient-card-good">
                        <div class="ingredient-name">{item["name"]}</div>
                        <div class="ingredient-reason">{item["reason"]}</div>
                    </div>
                ''', unsafe_allow_html=True)

        if report["caution_ingredients"]:
            st.markdown(
                '<div class="section-header section-header-caution">Use With Caution</div>',
                unsafe_allow_html=True
            )
            for item in report["caution_ingredients"]:
                st.markdown(f'''
                    <div class="ingredient-card-caution">
                        <div class="ingredient-name">{item["name"]}</div>
                        <div class="ingredient-reason">{item["reason"]}</div>
                    </div>
                ''', unsafe_allow_html=True)

        if report["bad_ingredients"]:
            st.markdown(
                '<div class="section-header section-header-bad">Avoid These Ingredients</div>',
                unsafe_allow_html=True
            )
            for item in report["bad_ingredients"]:
                st.markdown(f'''
                    <div class="ingredient-card-bad">
                        <div class="ingredient-name">{item["name"]}</div>
                        <div class="ingredient-reason">{item["reason"]}</div>
                    </div>
                ''', unsafe_allow_html=True)

        if report["unknown_ingredients"]:
            st.markdown(
                '<div class="section-header section-header-unknown">Not In Database</div>',
                unsafe_allow_html=True
            )
            st.markdown(f'''
                <div class="unknown-box">
                    {", ".join(report["unknown_ingredients"])}
                </div>
            ''', unsafe_allow_html=True)

        st.markdown(f'''
            <div class="footer-text">
                {report["total_analyzed"]} ingredients analyzed &nbsp;|&nbsp;
                {report["total_scored"]} matched &nbsp;|&nbsp;
                Skin type: {report["skin_type"]}
            </div>
        ''', unsafe_allow_html=True)

else:
    if not uploaded_file:
        st.markdown(
            '<div style="text-align:center; color:#4a3a2a; font-size:0.8rem; '
            'letter-spacing:0.15em; padding:2rem 0;">Upload a product image to begin analysis</div>',
            unsafe_allow_html=True
        )
