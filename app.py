import streamlit as st
from PIL import Image
import tempfile
import os
from utils.ocr import extract_ingredients
from utils.recommend import analyze_ingredients

st.set_page_config(
    page_title="Smart Skincare Advisor",
    page_icon="🧴",
    layout="centered"
)

st.title("🧴 Smart Skincare Advisor")
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

if uploaded_file:
    if st.button("🔍 Analyze Product"):
        with st.spinner("Analyzing ingredients... Please wait!"):
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".jpg"
            ) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            ingredients = extract_ingredients(tmp_path)
            report = analyze_ingredients(ingredients, skin_type)
            os.unlink(tmp_path)

        st.markdown("---")
        st.markdown("### 📊 Analysis Result")

        verdict = report["verdict"]

        if verdict == "SUITABLE":
            st.success("✅ SUITABLE for your skin type!")
        elif verdict == "USE WITH CAUTION":
            st.warning("⚠️ USE WITH CAUTION!")
        else:
            st.error("❌ AVOID this product!")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Good", len(report["good_ingredients"]))
        with col2:
            st.metric("⚠️ Caution", len(report["caution_ingredients"]))
        with col3:
            st.metric("❌ Bad", len(report["bad_ingredients"]))

        if report["good_ingredients"]:
            st.markdown("#### ✅ Good Ingredients")
            for item in report["good_ingredients"]:
                st.success(f"**{item['name']}** — {item['reason']}")

        if report["caution_ingredients"]:
            st.markdown("#### ⚠️ Use With Caution")
            for item in report["caution_ingredients"]:
                st.warning(f"**{item['name']}** — {item['reason']}")

        if report["bad_ingredients"]:
            st.markdown("#### ❌ Avoid These Ingredients")
            for item in report["bad_ingredients"]:
                st.error(f"**{item['name']}** — {item['reason']}")

        if report["unknown_ingredients"]:
            st.markdown("#### 🔍 Unknown Ingredients")
            st.info(", ".join(report["unknown_ingredients"]))

        st.markdown("---")
        st.caption(
            f"Analyzed {report['total_analyzed']} ingredients "
            f"for {report['skin_type']} skin type"
        )

