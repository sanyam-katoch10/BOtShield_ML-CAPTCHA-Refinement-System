import streamlit as st
from io import BytesIO
from generator import generate_captcha
from refine_m import refine, predict
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import time

st.set_page_config(page_title="ML CAPTCHA Refinement", page_icon="🔒", layout="wide")

if "avg_conf" not in st.session_state:
    st.session_state.avg_conf = 0.0
if "conf_history" not in st.session_state:
    st.session_state.conf_history = []

st.markdown("""
<style>
.stApp {
    font-family: 'Segoe UI', sans-serif;
    overflow: hidden;
    color: #eaeaea;
    background: linear-gradient(-45deg, #1b1b1b, #2a2a2a, #121212, #2e2e2e, #1b1b1b);
    background-size: 1000% 1000%;
    animation: gradientShift 30s ease infinite;
}
@keyframes gradientShift {
    0% {background-position:0% 50%;}
    25% {background-position:50% 100%;}
    50% {background-position:100% 50%;}
    75% {background-position:50% 0%;}
    100% {background-position:0% 50%;}
}
.topbar {
    background: rgba(30,30,30,0.7);
    backdrop-filter: blur(15px);
    padding: 20px 30px;
    border-radius: 20px;
    box-shadow: 0 0 15px #00ffff, 0 0 25px #ff00ff;
    margin-bottom: 25px;
    font-size: 28px;
    font-weight: 800;
}
section[data-testid="stSidebar"] {
    background: rgba(20,20,20,0.85);
    backdrop-filter: blur(12px);
    box-shadow: 0 0 15px #00ffff, 0 0 25px #ff00ff;
}
.card {
    background: rgba(40,40,40,0.45);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 25px;
    border: 2px solid #00ffff;
    box-shadow: 0 0 15px rgba(0,255,255,0.3), 0 0 25px rgba(255,0,255,0.2);
    animation: glow 6s ease-in-out infinite alternate;
}
@keyframes glow {
    from {box-shadow: 0 0 15px #00ffff;}
    to {box-shadow: 0 0 40px #ff00ff;}
}
.stButton button {
    border-radius: 16px;
    padding: 14px;
    font-weight: 700;
    background: linear-gradient(135deg,#3b3b3b,#7b7b7b,#3b3b3b);
    box-shadow: 0 0 20px rgba(0,255,255,0.6);
}
#particleCanvas {
    position: absolute;
    top:0;
    left:0;
    width:100%;
    height:100%;
    z-index:-1;
}
.footer {
    text-align:center;
    margin-top:40px;
    color:#8d8d8d;
}
</style>

<canvas id="particleCanvas"></canvas>

<script>
const canvas = document.getElementById("particleCanvas");
const ctx = canvas.getContext("2d");
let W = canvas.width = window.innerWidth;
let H = canvas.height = window.innerHeight;
window.onresize = () => {W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight;}
const colors = ["#00ffff","#ff00ff","#00ffbf","#ffbf00","#ff007f"];
const particles = Array.from({length:220},()=>({
    x:Math.random()*W,y:Math.random()*H,
    vx:(Math.random()-0.5),vy:(Math.random()-0.5),
    r:Math.random()*3+2,c:colors[Math.floor(Math.random()*colors.length)]
}));
let mouse={x:W/2,y:H/2};
document.onmousemove=e=>{mouse.x=e.clientX;mouse.y=e.clientY;}
function animate(){
    ctx.fillStyle="rgba(0,0,0,0.15)";
    ctx.fillRect(0,0,W,H);
    particles.forEach(p=>{
        p.x+=p.vx; p.y+=p.vy;
        let dx=mouse.x-p.x,dy=mouse.y-p.y,d=Math.sqrt(dx*dx+dy*dy);
        if(d<200){p.vx+=dx*0.001;p.vy+=dy*0.001;}
        if(p.x<0)p.x=W;if(p.x>W)p.x=0;if(p.y<0)p.y=H;if(p.y>H)p.y=0;
        if(Math.random()<0.01)p.c=colors[Math.floor(Math.random()*colors.length)];
        ctx.beginPath();
        ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
        ctx.fillStyle=p.c;
        ctx.shadowColor=p.c;
        ctx.shadowBlur=15;
        ctx.fill();
    });
    requestAnimationFrame(animate);
}
animate();
</script>
""", unsafe_allow_html=True)

st.markdown("<div class='topbar'>🔒 ML CAPTCHA Refinement <span style='float:right;font-size:16px;'>🟢 Model Online</span></div>", unsafe_allow_html=True)

with st.sidebar:
    page = st.radio("", ["📊 Dashboard", "🖼 CAPTCHA Generator", "🔁 Refinement Engine"])

if page == "📊 Dashboard":
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='card'>### Avg Confidence<br><h2>{st.session_state.avg_conf:.2f}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'>### Stability<br><h2>Stable</h2></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='card'>### Active Model<br><h2>CNN v1.0</h2></div>", unsafe_allow_html=True)

elif page == "🖼 CAPTCHA Generator":
    c1,c2 = st.columns([1.2,1.8])
    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        n = st.slider("Noise",0.0,1.0,0.25)
        d = st.slider("Distortion",0.0,1.0,0.25)
        c = st.slider("Clutter",0.0,1.0,0.25)
        btn = st.button("🎲 Generate CAPTCHA")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        slot = st.empty()
        if btn:
            img, text = generate_captcha(n,d,c)
            slot.image(img, use_column_width=True)
            pred, conf = predict(img)
            st.session_state.conf_history.append(conf)
            st.session_state.avg_conf = sum(st.session_state.conf_history)/len(st.session_state.conf_history)
            st.markdown(f"**Text:** `{text}` | **Difficulty:** `{pred.upper()}` | **Confidence:** `{conf:.2f}`")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "🔁 Refinement Engine":
    target = st.selectbox("Target Difficulty",["easy","medium","hard"])
    st.markdown(f"<div class='card'><b>Live Avg Confidence</b><br><h2>{st.session_state.avg_conf:.2f}</h2></div>", unsafe_allow_html=True)
    refine_btn = st.button("✨ Refine Once")
    auto_btn = st.button("🚀 Auto-Refine")
    live = st.empty()
    col1,col2 = st.columns(2)
    conv = col1.empty()
    heat = col2.empty()

    if refine_btn:
        img,text,lvl = refine(target)
        live.image(img, use_column_width=True)
        _, conf = predict(img)
        st.session_state.conf_history.append(conf)
        st.session_state.avg_conf = sum(st.session_state.conf_history)/len(st.session_state.conf_history)
        buf = BytesIO(); img.save(buf, format="PNG")
        st.download_button("⬇ Download CAPTCHA", buf.getvalue(), f"{text}_{lvl}.png")

    if auto_btn:
        confs=[]
        mat_cur=np.zeros((4,4))
        for _ in range(6):
            mat=np.zeros((4,4))
            for i in range(4):
                for j in range(4):
                    img,_,_=refine(target)
                    live.image(img, use_column_width=True)
                    _,c=predict(img)
                    mat[i,j]=c
            avg=mat.mean()
            confs.append(avg)
            st.session_state.conf_history.append(avg)
            st.session_state.avg_conf=sum(st.session_state.conf_history)/len(st.session_state.conf_history)
            fig,ax=plt.subplots()
            ax.plot(confs,marker='o',color='#00ffff')
            ax.set_ylim(0,1)
            conv.pyplot(fig,clear_figure=True)
            plt.close(fig)
            fig2,ax2=plt.subplots()
            ax2.imshow(mat,cmap='plasma')
            heat.pyplot(fig2,clear_figure=True)
            plt.close(fig2)
            time.sleep(0.15)
        st.success("Target difficulty stabilized ✔")

st.markdown("<div class='footer'>✨ Built by SANYAM KATOCH ✨</div>", unsafe_allow_html=True)
