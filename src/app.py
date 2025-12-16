/* ---------- BACKGROUND ---------- */
.stApp {
    position: relative;
    background: linear-gradient(135deg, #1a1a1a, #2a2a2a, #1f1f1f, #2b2b2b);
    background-size: 400% 400%;
    animation: bgGradientShift 30s ease infinite;
    color: #eaeaea;
    font-family: 'Segoe UI', sans-serif;
    overflow: hidden;
}

/* Gradient shift animation */
@keyframes bgGradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Flowing particles/dots */
.stApp::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(#888 1px, transparent 1px);
    background-size: 30px 30px;
    animation: moveDots 60s linear infinite;
    opacity: 0.1;
    pointer-events: none;
}

@keyframes moveDots {
    0% {transform: translate(0, 0);}
    50% {transform: translate(50px, 50px);}
    100% {transform: translate(0, 0);}
}
