import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("energy_model.pkl")

# Page config
st.set_page_config(page_title="Energy Predictor", layout="centered")

# Custom CSS for box UI
st.markdown("""
<style>
.box {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.title-box {
    background: linear-gradient(135deg, #f9d423, #ff4e50);
    color: white;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 26px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Title box
st.markdown('<div class="title-box">⚡ Energy Consumption Prediction</div>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="box"><h3>🔢 Input Parameters</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    hour = st.number_input("⏰ Hour (0–23)", 0, 23)
    day = st.number_input("📅 Day (1–31)", 1, 31)

with col2:
    month = st.number_input("🗓️ Month (1–12)", 1, 12)
    dayofweek = st.number_input("📆 Day of Week (0=Mon, 6=Sun)", 0, 6)

st.markdown('</div>', unsafe_allow_html=True)

# Prediction Section
st.markdown('<div class="box"><h3>📊 Prediction Result</h3>', unsafe_allow_html=True)

if st.button("🔮 Predict Energy Usage"):
    X = np.array([[hour, day, month, dayofweek]])
    pred = model.predict(X)
    st.success(f"⚡ Predicted Energy Consumption: **{pred[0]:.2f} kWh**")

st.markdown('</div>', unsafe_allow_html=True)
