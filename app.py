import streamlit as st
import joblib
import numpy as np

# ---------------- LOAD MODEL ----------------
model = joblib.load("energy_model.pkl")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Energy Consumption Predictor",
    layout="centered"
)

# ---------------- ELECTRIC UI + CURSOR EFFECTS ----------------
st.markdown("""
<style>

/* ========== GLOBAL BACKGROUND ========== */
.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(0,255,255,0.08), transparent 40%),
        radial-gradient(circle at 80% 30%, rgba(138,43,226,0.08), transparent 40%),
        linear-gradient(135deg, #020617, #0a0f1c);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* ========== ELECTRIC GRID ANIMATION ========== */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,255,255,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(138,43,226,0.08) 1px, transparent 1px);
    background-size: 40px 40px;
    animation: gridMove 25s linear infinite;
    z-index: 0;
}

@keyframes gridMove {
    from { background-position: 0 0; }
    to   { background-position: 400px 400px; }
}

/* ========== CURSOR GLOW FOLLOW ========== */
body::after {
    content: "";
    position: fixed;
    top: var(--y);
    left: var(--x);
    width: 160px;
    height: 160px;
    pointer-events: none;
    background: radial-gradient(
        circle,
        rgba(0,245,255,0.25),
        transparent 60%
    );
    transform: translate(-50%, -50%);
    z-index: 9999;
    transition: top 0.05s linear, left 0.05s linear;
}

/* ========== TITLE BOX ========== */
.title-box {
    background: linear-gradient(90deg, #00f5ff, #8a2be2, #ffb703);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    color: #020617;
    box-shadow: 0 0 30px rgba(0,255,255,0.5);
    animation: glow 3s infinite alternate;
}

@keyframes glow {
    from { box-shadow: 0 0 20px rgba(0,255,255,0.4); }
    to   { box-shadow: 0 0 40px rgba(138,43,226,0.8); }
}

/* ========== GLASS BOX ========== */
.box {
    position: relative;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(14px);
    padding: 24px;
    border-radius: 18px;
    margin-top: 25px;
    border: 1px solid rgba(255,255,255,0.12);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    z-index: 1;
}

.box:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 0 30px rgba(0,255,255,0.4);
}

/* ========== ENERGY RIPPLE ON HOVER ========== */
.box::after {
    content: "";
    position: absolute;
    inset: -2px;
    border-radius: inherit;
    background: linear-gradient(
        120deg,
        transparent,
        rgba(0,255,255,0.6),
        transparent
    );
    opacity: 0;
    transition: opacity 0.3s ease;
}

.box:hover::after {
    opacity: 1;
}

/* ========== INPUT STYLING ========== */
label {
    color: #9ae6ff !important;
    font-weight: 600;
}

input {
    background: rgba(0,0,0,0.4) !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    transition: box-shadow 0.3s ease, transform 0.2s ease;
}

input:hover {
    box-shadow: 0 0 20px rgba(0,255,255,0.6);
    transform: scale(1.02);
}

/* ========== BUTTON ========== */
.stButton > button {
    width: 100%;
    padding: 14px;
    font-size: 18px;
    font-weight: 800;
    border-radius: 14px;
    border: none;
    color: #020617;
    background: linear-gradient(90deg, #00f5ff, #8a2be2);
    box-shadow: 0 0 20px rgba(0,255,255,0.5);
    transition: all 0.3s ease;
    animation: pulse 2.5s infinite;
}

.stButton > button:hover {
    transform: scale(1.06);
    box-shadow: 0 0 40px rgba(138,43,226,0.9);
}

@keyframes pulse {
    0% { box-shadow: 0 0 15px rgba(0,255,255,0.4); }
    50% { box-shadow: 0 0 35px rgba(138,43,226,0.9); }
    100% { box-shadow: 0 0 15px rgba(0,255,255,0.4); }
}

/* ========== SUCCESS BOX ========== */
.stSuccess {
    background: rgba(0,255,200,0.15);
    border-left: 6px solid #00ffd5;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- CURSOR TRACKING JS ----------------
st.markdown("""
<script>
document.addEventListener("mousemove", e => {
    document.body.style.setProperty('--x', e.clientX + 'px');
    document.body.style.setProperty('--y', e.clientY + 'px');
});
</script>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    '<div class="title-box">⚡ Energy Consumption Prediction</div>',
    unsafe_allow_html=True
)

# ---------------- INPUT SECTION ----------------
st.markdown('<div class="box"><h3>🔢 Input Parameters</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    hour = st.number_input("⏰ Hour (0–23)", 0, 23)
    day = st.number_input("📅 Day (1–31)", 1, 31)

with col2:
    month = st.number_input("🗓️ Month (1–12)", 1, 12)
    dayofweek = st.number_input("📆 Day of Week (0=Mon, 6=Sun)", 0, 6)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PREDICTION ----------------
st.markdown('<div class="box"><h3>📊 Prediction Output</h3>', unsafe_allow_html=True)

if st.button("🔮 Predict Energy Usage"):
    X = np.array([[hour, day, month, dayofweek]])
    pred = model.predict(X)
    st.success(f"⚡ Predicted Energy Consumption: **{pred[0]:.2f} kWh**")

st.markdown('</div>', unsafe_allow_html=True)
