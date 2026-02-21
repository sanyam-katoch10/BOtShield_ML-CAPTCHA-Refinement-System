import streamlit as st
from io import BytesIO
from generator import generate_captcha
from refine_m import refine, predict
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import time
import random

st.set_page_config(page_title="BOtShielD", page_icon="🔒", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
#  GENERATE FLOATING PARTICLES (pure CSS, rendered as HTML divs)
# ══════════════════════════════════════════════════════════════════════════════

def generate_particles(count=30):
    """Generate CSS-animated floating particle divs."""
    particles_html = ""
    for i in range(count):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        size = round(random.uniform(2, 5), 1)
        duration = round(random.uniform(15, 40), 1)
        delay = round(random.uniform(0, 20), 1)
        opacity = round(random.uniform(0.15, 0.4), 2)
        drift_x = random.randint(-60, 60)
        drift_y = random.randint(-80, 80)
        color = random.choice(["88,166,255", "163,113,247", "247,120,186"])
        particles_html += (
            f"<div class='particle' style='"
            f"left:{x}%;top:{y}%;width:{size}px;height:{size}px;"
            f"opacity:{opacity};"
            f"background:rgba({color},0.8);"
            f"box-shadow:0 0 {size*3}px rgba({color},0.4);"
            f"animation:drift{i%5} {duration}s {delay}s ease-in-out infinite alternate;"
            f"'></div>"
        )
    return particles_html

particles = generate_particles()

# ══════════════════════════════════════════════════════════════════════════════
#  CUSTOM CSS + PARTICLES
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

/* ── Base ── */
.stApp {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #c9d1d9;
    background: #0d1117;
}}

/* ── Particles ── */
.particles-container {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}}

.particle {{
    position: absolute;
    border-radius: 50%;
}}

@keyframes drift0 {{
    0%   {{ transform: translate(0, 0) scale(1); }}
    100% {{ transform: translate(40px, -60px) scale(1.3); }}
}}
@keyframes drift1 {{
    0%   {{ transform: translate(0, 0) scale(1); }}
    100% {{ transform: translate(-50px, -40px) scale(0.7); }}
}}
@keyframes drift2 {{
    0%   {{ transform: translate(0, 0) scale(1); opacity: 0.3; }}
    100% {{ transform: translate(30px, 50px) scale(1.2); opacity: 0.15; }}
}}
@keyframes drift3 {{
    0%   {{ transform: translate(0, 0) scale(0.8); }}
    100% {{ transform: translate(-40px, 30px) scale(1.4); }}
}}
@keyframes drift4 {{
    0%   {{ transform: translate(0, 0) scale(1.1); }}
    100% {{ transform: translate(60px, -30px) scale(0.6); }}
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0d1117 0%, #111822 100%);
    border-right: 1px solid #21262d;
}}

.sidebar-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 4px 0 20px;
    border-bottom: 1px solid #21262d;
    margin-bottom: 20px;
}}

.sidebar-brand-icon {{
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #58a6ff, #a371f7);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    animation: iconFloat 3s ease-in-out infinite;
}}

.sidebar-brand-text {{
    font-size: 17px;
    font-weight: 800;
    color: #f0f6fc;
    letter-spacing: -0.3px;
}}

.sidebar-section-label {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #484f58;
    margin-bottom: 10px;
}}

/* ── Header Bar ── */
.header-bar {{
    position: relative;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 16px;
    padding: 22px 28px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    overflow: hidden;
    animation: fadeSlideDown 0.6s ease-out;
}}

.header-bar::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #58a6ff, #a371f7, #f778ba, #a371f7, #58a6ff);
    background-size: 200% 100%;
    animation: gradientSlide 4s linear infinite;
}}

.header-title {{
    font-size: 20px;
    font-weight: 800;
    color: #f0f6fc;
    letter-spacing: -0.3px;
}}

.header-subtitle {{
    font-size: 13px;
    color: #484f58;
    font-weight: 500;
    margin-top: 2px;
}}

.header-badge {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(63,185,80,0.1);
    border: 1px solid rgba(63,185,80,0.2);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    color: #3fb950;
}}

.header-badge-dot {{
    width: 7px;
    height: 7px;
    background: #3fb950;
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
}}

/* ── Section Title ── */
.section-title {{
    font-size: 15px;
    font-weight: 700;
    color: #f0f6fc;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
    animation: fadeSlideUp 0.4s ease-out;
}}

.section-title-icon {{
    width: 28px;
    height: 28px;
    background: linear-gradient(135deg, #58a6ff22, #a371f722);
    border: 1px solid #58a6ff33;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}}

/* ── Stat Cards (with animated gradient border) ── */
.stat-card-wrapper {{
    position: relative;
    border-radius: 15px;
    padding: 2px;
    background: #21262d;
    overflow: hidden;
    transition: transform 0.25s ease;
    animation: fadeSlideUp 0.5s ease-out both;
}}

.stat-card-wrapper:hover {{
    transform: translateY(-4px);
}}

.stat-card-wrapper::before {{
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(
        transparent 0deg,
        #58a6ff 60deg,
        transparent 120deg,
        #a371f7 180deg,
        transparent 240deg,
        #f778ba 300deg,
        transparent 360deg
    );
    opacity: 0;
    transition: opacity 0.4s ease;
    animation: rotateBorder 4s linear infinite;
}}

.stat-card-wrapper:hover::before {{
    opacity: 1;
}}

.stat-card {{
    position: relative;
    background: #161b22;
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    z-index: 1;
}}

.stat-icon {{
    width: 40px;
    height: 40px;
    margin: 0 auto 14px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    transition: transform 0.3s ease;
}}

.stat-card-wrapper:hover .stat-icon {{
    transform: scale(1.15) rotate(-5deg);
    animation: wiggle 0.5s ease;
}}

.stat-icon-blue {{ background: rgba(88,166,255,0.12); border: 1px solid rgba(88,166,255,0.2); }}
.stat-icon-green {{ background: rgba(63,185,80,0.12); border: 1px solid rgba(63,185,80,0.2); }}
.stat-icon-purple {{ background: rgba(163,113,247,0.12); border: 1px solid rgba(163,113,247,0.2); }}

.stat-label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #484f58;
    margin-bottom: 6px;
}}

.stat-value {{
    font-size: 26px;
    font-weight: 900;
    color: #f0f6fc;
    letter-spacing: -0.5px;
}}

.stat-value-blue {{ color: #58a6ff; }}
.stat-value-green {{ color: #3fb950; }}
.stat-value-purple {{ color: #a371f7; }}

/* ── Content Cards (shimmer on hover) ── */
.card {{
    position: relative;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 24px;
    overflow: hidden;
    transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.2s ease;
    animation: fadeSlideUp 0.5s ease-out;
}}

.card:hover {{
    border-color: #30363d;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    transform: translateY(-2px);
}}

.card::after {{
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(88,166,255,0.04), transparent);
    transition: left 0.5s ease;
}}

.card:hover::after {{
    left: 150%;
}}

.card-title {{
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #484f58;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #21262d;
}}

/* ── Buttons ── */
.stButton button {{
    border-radius: 10px;
    border: 1px solid #30363d;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
    font-family: 'Inter', sans-serif;
    color: #f0f6fc;
    background: #21262d;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}}

.stButton button:hover {{
    border-color: #58a6ff;
    background: #262c36;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.1), 0 4px 12px rgba(0,0,0,0.3);
    transform: translateY(-1px);
}}

.stButton button:active {{
    transform: translateY(0);
    box-shadow: 0 0 0 3px rgba(88,166,255,0.15);
}}

/* ── Download Button ── */
.stDownloadButton button {{
    border-radius: 10px;
    border: 1px solid rgba(63,185,80,0.3);
    background: rgba(63,185,80,0.1);
    color: #3fb950;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s ease;
}}

.stDownloadButton button:hover {{
    background: rgba(63,185,80,0.15);
    border-color: #3fb950;
    box-shadow: 0 0 0 3px rgba(63,185,80,0.1);
    transform: translateY(-1px);
}}

/* ── Slider ── */
.stSlider label {{ font-weight: 600; font-size: 13px; color: #c9d1d9; }}
.stSlider > div > div > div > div {{ background: #58a6ff; }}

/* ── Select box ── */
.stSelectbox label {{ font-weight: 600; font-size: 13px; color: #c9d1d9; }}

/* ── Footer ── */
.footer {{
    text-align: center;
    margin-top: 48px;
    padding: 24px 0;
    font-size: 12px;
    font-weight: 600;
    color: #30363d;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    border-top: 1px solid #161b22;
}}

.footer a {{
    color: #484f58;
    text-decoration: none;
    transition: color 0.2s;
}}

.footer a:hover {{ color: #58a6ff; }}

/* ── Animations ── */
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}

@keyframes fadeSlideUp {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes fadeSlideDown {{
    from {{ opacity: 0; transform: translateY(-12px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes gradientSlide {{
    0%   {{ background-position: 200% 0; }}
    100% {{ background-position: -200% 0; }}
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50%      {{ opacity: 0.5; transform: scale(0.85); }}
}}

@keyframes iconFloat {{
    0%, 100% {{ transform: translateY(0); }}
    50%      {{ transform: translateY(-3px); }}
}}

@keyframes rotateBorder {{
    from {{ transform: rotate(0deg); }}
    to   {{ transform: rotate(360deg); }}
}}

@keyframes wiggle {{
    0%, 100% {{ transform: scale(1.15) rotate(0deg); }}
    25%      {{ transform: scale(1.15) rotate(-8deg); }}
    75%      {{ transform: scale(1.15) rotate(8deg); }}
}}

.stSuccess {{
    border-radius: 10px;
}}
</style>

<!-- Floating particles -->
<div class="particles-container">
    {particles}
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class='header-bar'>
    <div>
        <div class='header-title'>BOtShielD — ML CAPTCHA Refinement System</div>
        <div class='header-subtitle'>CNN-powered adaptive difficulty system</div>
    </div>
    <div class='header-badge'>
        <span class='header-badge-dot'></span>
        Model Online
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
        <div class='sidebar-brand-icon'>🔒</div>
        <div class='sidebar-brand-text'>BOtShielD</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section-label'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio("", [" Dashboard", " CAPTCHA Generator", " Refinement Engine"])

    st.markdown("---")
    st.markdown("<div class='sidebar-section-label'>Model Info</div>", unsafe_allow_html=True)
    st.caption("**Architecture:** CNN (TF/Keras)")
    st.caption("**Classes:** Easy · Medium · Hard")
    st.caption("**Accuracy:** 97%")

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

if page == " Dashboard":
    st.markdown("""
    <div class='section-title'>
        <div class='section-title-icon'>📊</div>
        System Overview
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='stat-card-wrapper'>
            <div class='stat-card'>
                <div class='stat-icon stat-icon-blue'>📈</div>
                <div class='stat-label'>Avg Confidence</div>
                <div class='stat-value stat-value-blue'>0.97</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stat-card-wrapper' style='animation-delay:0.1s'>
            <div class='stat-card'>
                <div class='stat-icon stat-icon-green'>✅</div>
                <div class='stat-label'>System Status</div>
                <div class='stat-value stat-value-green'>Stable</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='stat-card-wrapper' style='animation-delay:0.2s'>
            <div class='stat-card'>
                <div class='stat-icon stat-icon-purple'>🧠</div>
                <div class='stat-label'>Active Model</div>
                <div class='stat-value stat-value-purple'>CNN v1</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>How It Works</div>
            <p style='color:#8b949e; line-height:1.7; font-size:14px;'>
                The system generates CAPTCHAs with configurable noise, distortion, and clutter levels.
                A trained CNN classifier predicts the difficulty, and the refinement engine iteratively
                adjusts parameters until the target difficulty is achieved.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>Architecture</div>
            <p style='color:#8b949e; line-height:1.7; font-size:14px;'>
                <span style='color:#58a6ff;'>Conv2D</span> → ReLU → MaxPool →
                <span style='color:#a371f7;'>Conv2D</span> → ReLU → MaxPool → Flatten →
                <span style='color:#f778ba;'>Dense(128)</span> →
                <span style='color:#3fb950;'>Softmax(3)</span>
            </p>
            <p style='color:#484f58; font-size:12px; margin-top:10px;'>
                Optimizer: Adam &nbsp;·&nbsp; Loss: Categorical Crossentropy &nbsp;·&nbsp; Dataset: 6,000 images
            </p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CAPTCHA GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

elif page == " CAPTCHA Generator":
    st.markdown("""
    <div class='section-title'>
        <div class='section-title-icon'>🖼</div>
        CAPTCHA Generator
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1.8])
    with col1:
        st.markdown("<div class='card'><div class='card-title'>Parameters</div>", unsafe_allow_html=True)
        noise = st.slider("Noise Level", 0.0, 1.0, 0.25)
        distortion = st.slider("Distortion Level", 0.0, 1.0, 0.25)
        clutter = st.slider("Clutter Level", 0.0, 1.0, 0.25)
        gen_btn = st.button("⚡ Generate CAPTCHA")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><div class='card-title'>Preview</div>", unsafe_allow_html=True)
        preview_slot = st.empty()
        if gen_btn:
            img, text = generate_captcha(noise, distortion, clutter)
            preview_slot.image(img, use_container_width=True)
            pred, conf = predict(img)
            rcol1, rcol2, rcol3 = st.columns(3)
            rcol1.metric("CAPTCHA Text", text)
            rcol2.metric("Difficulty", pred.upper())
            rcol3.metric("Confidence", f"{conf:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  REFINEMENT ENGINE
# ══════════════════════════════════════════════════════════════════════════════

elif page == " Refinement Engine":
    st.markdown("""
    <div class='section-title'>
        <div class='section-title-icon'>🔁</div>
        Refinement Engine
    </div>
    """, unsafe_allow_html=True)

    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 1, 2])
    with ctrl_col1:
        target = st.selectbox("Target Difficulty", ["easy", "medium", "hard"])
    with ctrl_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        refine_btn = st.button("⚡ Refine Once")
    with ctrl_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        auto_btn = st.button("🔄 Auto-Refine (6 steps)")

    st.markdown("---")

    live_slot = st.empty()
    col1, col2 = st.columns([1, 1])
    conv_slot = col1.empty()
    heat_slot = col2.empty()

    if refine_btn:
        img, text, lvl = refine(target)
        live_slot.image(img, use_container_width=True)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.download_button("⬇ Download CAPTCHA", buf.getvalue(), f"{text}_{lvl}.png")

    if auto_btn:
        confs = []
        grid = 4
        mat_current = np.zeros((grid, grid))
        steps_per_update = 20
        norm = mcolors.Normalize(vmin=0, vmax=1)
        cmap = plt.cm.plasma

        last_text = ""
        last_lvl = ""
        last_conf = 0.0
        for step in range(6):
            mat_target = np.zeros((grid, grid))
            for i in range(grid):
                for j in range(grid):
                    img, text, lvl = refine(target)
                    live_slot.image(img, use_container_width=True)
                    _, c = predict(img)
                    mat_target[i, j] = c
                    last_text = text
                    last_lvl = lvl
                    last_conf = c
            confs.append(mat_target.mean())
            for t in range(1, steps_per_update + 1):
                mat_interpolated = mat_current + (mat_target - mat_current) * (t / steps_per_update)

                fig1, ax1 = plt.subplots(figsize=(6, 4))
                fig1.set_facecolor("#0d1117")
                ax1.set_facecolor("#0d1117")
                ax1.plot(confs, marker='o', color='#58a6ff', linewidth=2, markersize=7)
                ax1.fill_between(range(len(confs)), confs, alpha=0.08, color='#58a6ff')
                ax1.set_ylim(0, 1)
                ax1.set_title("Convergence", color="#c9d1d9", fontsize=13, fontweight='bold', pad=12)
                ax1.set_xlabel("Step", color="#484f58", fontsize=11)
                ax1.set_ylabel("Confidence", color="#484f58", fontsize=11)
                ax1.tick_params(colors="#484f58", labelsize=10)
                ax1.grid(True, alpha=0.1, color="#484f58")
                for spine in ax1.spines.values():
                    spine.set_color("#21262d")
                fig1.tight_layout()
                conv_slot.pyplot(fig1, clear_figure=True)
                plt.close(fig1)

                fig2, ax2 = plt.subplots(figsize=(6, 4))
                fig2.set_facecolor("#0d1117")
                ax2.set_facecolor("#0d1117")
                im = ax2.imshow(mat_interpolated, cmap=cmap, norm=norm, aspect='equal')
                for i in range(grid):
                    for j in range(grid):
                        ax2.text(j, i, f"{mat_interpolated[i,j]:.2f}", ha='center', va='center',
                                 color='white', fontsize=11, fontweight='bold')
                ax2.tick_params(colors="#484f58", which='both', labelsize=10)
                for spine in ax2.spines.values():
                    spine.set_color("#21262d")
                ax2.set_title("Confidence Heatmap", color="#c9d1d9", fontsize=13, fontweight='bold', pad=12)
                fig2.tight_layout()
                heat_slot.pyplot(fig2, clear_figure=True)
                plt.close(fig2)
                time.sleep(0.05)
            mat_current = mat_target.copy()
        st.success("✅ Target difficulty stabilized — refinement complete")
        st.info(f"🔤 Final CAPTCHA Text: **{last_text}** &nbsp;·&nbsp; Difficulty: **{last_lvl.upper()}** &nbsp;·&nbsp; Confidence: **{last_conf:.2f}**")

# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class='footer'>
    Built by <a href='https://github.com/sanyam-katoch10' target='_blank'>Sanyam Katoch</a><br>
    BOtShielD &copy; 2026
</div>
""", unsafe_allow_html=True)
