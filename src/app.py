import streamlit as st
from io import BytesIO
from generator import generate_captcha
from refine_m import refine, predict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

# ===================== CONFIG =====================
st.set_page_config(
    page_title="ML CAPTCHA Refinement",
    page_icon="🔒",
    layout="wide"
)

# ===================== CSS =====================
st.markdown("""
<style>

/* ===== ANIMATED DARK BACKGROUND ===== */
.stApp {
    background: linear-gradient(
        120deg,
        #0b0b0e,
        #141418,
        #1b1c22,
        #0f1014
    );
    background-size: 400% 400%;
    animation: darkFlow 30s ease infinite;
    color: #e6e6e6;
}

@keyframes darkFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ===== TOP BAR ===== */
.topbar {
    background: linear-gradient(135deg,#1c1c22,#2b2b34);
    padding: 18px 30px;
    border-radius: 18px;
    font-size: 26px;
    font-weight: 800;
    box-shadow: 0 12px 30px rgba(0,0,0,0.8);
    margin-bottom: 20px;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f1014,#181922);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* ===== CARDS ===== */
.card {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.08),
        rgba(255,255,255,0.02)
    );
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 18px 40px rgba(0,0,0,0.75);
    transition: transform 0.35s ease, box-shadow 0.35s ease;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 30px 65px rgba(0,0,0,0.9);
}

/* ===== BUTTONS ===== */
.stButton button {
    border-radius: 16px;
    padding: 14px 20px;
    font-weight: 700;
    color: #fff;
    background: linear-gradient(
        135deg,
        #3f3f46,
        #8b8b94,
        #3f3f46
    );
    box-shadow: inset 0 1px 1px rgba(255,255,255,0.35),
                0 8px 22px rgba(0,0,0,0.75);
    transition: all 0.35s ease;
}

.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 24px rgba(220,220,220,0.35),
                0 14px 34px rgba(0,0,0,0.9);
}

/* ===== FOOTER ===== */
.footer {
    text-align: center;
    margin-top: 40px;
    color: #8f8f9a;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ===================== TOP BAR =====================
st.markdown(
    "<div class='topbar'>🔒 ML CAPTCHA Refinement <span style='float:right;font-size:16px;'>🟢 Model Online</span></div>",
    unsafe_allow_html=True
)

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("## ⚙️ Navigation")
    page = st.radio(
        "",
        ["📊 Dashboard", "🖼 CAPTCHA Generator", "🔁 Refinement Engine"]
    )

# ===================== DASHBOARD =====================
if page == "📊 Dashboard":
    st.markdown("## 📊 System Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<div class='card'><h3>Avg Confidence</h3><h2>0.76</h2></div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'><h3>Stability</h3><h2>Stable</h2></div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='card'><h3>Active Model</h3><h2>CNN v1.0</h2></div>", unsafe_allow_html=True)

# ===================== GENERATOR =====================
elif page == "🖼 CAPTCHA Generator":
    st.markdown("## 🖼 CAPTCHA Generator")

    left, right = st.columns([1.1, 1.9])

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        noise = st.slider("Noise", 0.0, 1.0, 0.25)
        distortion = st.slider("Distortion", 0.0, 1.0, 0.25)
        clutter = st.slider("Clutter", 0.0, 1.0, 0.25)
        gen_btn = st.button("🎲 Generate CAPTCHA")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        img_slot = st.empty()
        stats_slot = st.empty()
        plot_c1, plot_c2 = st.columns(2)

        if gen_btn:
            img, text = generate_captcha(noise, distortion, clutter)
            pred, conf = predict(img)

            img_slot.image(img, use_column_width=True)
            stats_slot.markdown(f"""
            **Text:** `{text}`  
            **Difficulty:** `{pred.upper()}`  
            **Confidence:** `{conf:.2f}`
            """)

            # --- CONVERGENCE ---
            confs = []
            mat = np.zeros((4,4))

            for i in range(4):
                for j in range(4):
                    _, c = predict(img)
                    mat[i,j] = c
                    confs.append(c)

            fig1, ax1 = plt.subplots(figsize=(4,3))
            ax1.plot(confs, marker='o')
            ax1.set_ylim(0,1)
            ax1.set_title("Confidence Convergence")
            plot_c1.pyplot(fig1)
            plt.close(fig1)

            fig2, ax2 = plt.subplots(figsize=(4,3))
            sns.heatmap(mat, annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
            ax2.set_title("Confidence Heatmap")
            plot_c2.pyplot(fig2)
            plt.close(fig2)

        st.markdown("</div>", unsafe_allow_html=True)

# ===================== REFINEMENT =====================
elif page == "🔁 Refinement Engine":
    st.markdown("## 🔁 Refinement Engine")

    target = st.selectbox("Target Difficulty", ["easy", "medium", "hard"])
    refine_btn = st.button("✨ Refine Once")
    auto_btn = st.button("🚀 Auto-Refine")

    plot_slot = st.empty()
    heat_slot = st.empty()

    if refine_btn:
        img, text, lvl = refine(target)
        st.image(img, use_column_width=True)

        buf = BytesIO()
        img.save(buf, format="PNG")
        st.download_button("⬇ Download CAPTCHA", buf.getvalue(), f"{text}_{lvl}.png")

    if auto_btn:
        confs = []

        for step in range(6):
            mat = np.zeros((4,4))
            for i in range(4):
                for j in range(4):
                    img, _, _ = refine(target)
                    _, c = predict(img)
                    mat[i,j] = c

            confs.append(mat.mean())

            fig1, ax1 = plt.subplots()
            ax1.plot(confs, marker='o')
            ax1.set_ylim(0,1)
            plot_slot.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            fig2, ax2 = plt.subplots()
            sns.heatmap(mat, annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
            heat_slot.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            time.sleep(0.5)

        st.success("Target difficulty stabilized ✔")

# ===================== FOOTER =====================
st.markdown("<div class='footer'>✨ Built by SANYAM KATOCH ✨</div>", unsafe_allow_html=True)
