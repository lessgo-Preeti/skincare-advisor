import streamlit as st
from PIL import Image
import tempfile
import os
from utils.ocr import extract_ingredients
from utils.recommend import analyze_ingredients

st.set_page_config(
    page_title="Smart Skincare Advisor",
    layout="centered"
)

st.title("Smart Skincare Advisor")
st.subheader("Find out if a product is right for your skin!")

st.markdown("### Step 1: Select Your Skin Type")
skin_type = st.selectbox(
    "What is your skin type?",
    ["Oily", "Dry", "Combination", "Sensitive", "Normal"]
)

st.markdown("### Step 2: Upload Product Image")
uploaded_file = st.file_uploader(
    "Upload a clear image of the ingredients list",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=500)

    if st.button("Analyze Product"):
        with st.spinner("Analyzing ingredients... Please wait!"):

            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".jpg"
            ) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            try:
                ingredients = extract_ingredients(tmp_path)
            except Exception:
                st.error("OCR processing failed. Please try a clearer image.")
                ingredients = []
            finally:
                os.unlink(tmp_path)

        if len(ingredients) == 0:
            st.error("Could not detect ingredients. Please upload a clearer image.")
        else:
            report = analyze_ingredients(ingredients, skin_type)

            st.markdown("---")
            st.markdown("### Analysis Result")

            verdict = report["verdict"]

            if verdict == "SUITABLE":
                st.success(verdict)
            elif verdict in ["USE WITH CAUTION", "RISKY"]:
                st.warning(verdict)
            else:
                st.error(verdict)

            st.markdown(f"_{report['verdict_detail']}_")

            st.markdown("---")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Safety Score", f"{report['safety_score']} / 10")
            with col2:
                st.metric("Confidence", f"{report['confidence']}%")
            with col3:
                st.metric("Ingredients Analyzed", report['total_analyzed'])

            st.progress(report["safety_score"] / 10)

            st.markdown("---")

            col4, col5, col6 = st.columns(3)
            with col4:
                st.metric("Good", len(report["good_ingredients"]))
            with col5:
                st.metric("Caution", len(report["caution_ingredients"]))
            with col6:
                st.metric("Bad", len(report["bad_ingredients"]))

            if report["good_ingredients"]:
                st.markdown("#### Good Ingredients")
                for item in report["good_ingredients"]:
                    st.success(f"**{item['name']}** - {item['reason']}")

            if report["caution_ingredients"]:
                st.markdown("#### Use With Caution")
                for item in report["caution_ingredients"]:
                    st.warning(f"**{item['name']}** - {item['reason']}")

            if report["bad_ingredients"]:
                st.markdown("#### Avoid These Ingredients")
                for item in report["bad_ingredients"]:
                    st.error(f"**{item['name']}** - {item['reason']}")

            if report["unknown_ingredients"]:
                st.markdown("#### Unknown Ingredients")
                st.info(
                    f"These ingredients were not found in our database: "
                    f"{', '.join(report['unknown_ingredients'])}"
                )

            st.markdown("---")
            st.caption(
                f"Analyzed {report['total_analyzed']} ingredients | "
                f"{report['total_scored']} matched | "
                f"Skin type: {report['skin_type']}"
            )

else:
    st.info("Please upload an image of the product ingredients list.")