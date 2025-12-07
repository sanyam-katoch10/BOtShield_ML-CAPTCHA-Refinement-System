import streamlit as st
from io import BytesIO
from PIL import Image
from generator import generate_captcha
from refine_m import refine, predict

st.set_page_config(page_title="CAPTCHA ML", layout="centered", page_icon="🔐")

st.title("🔐 ML CAPTCHA Refinement System")

st.subheader("Manual CAPTCHA Generator")

noise = st.slider("Noise", 0.0, 1.0, 0.2)
dist = st.slider("Distortion", 0.0, 1.0, 0.2)
clutter = st.slider("Clutter", 0.0, 1.0, 0.2)

if st.button("Generate CAPTCHA"):
    img, text = generate_captcha(noise, dist, clutter)
    st.image(img, caption=text)
    pred_label, conf = predict(img)
    st.info(f"Predicted Difficulty: {pred_label} ({conf:.2f})")

st.subheader("Target Difficulty Refinement")

target = st.selectbox("Choose Target Difficulty:", ["easy", "medium", "hard"])

if st.button("Refine CAPTCHA"):
    img, text, predicted = refine(target)
    st.image(img, caption=f"{text} | Predicted: {predicted}")

    buf = BytesIO()
    img.save(buf, format="PNG")
    st.download_button("Download CAPTCHA", 
                       data=buf.getvalue(),
                       file_name=f"{text}_{predicted}.png",
                       mime="image/png")
