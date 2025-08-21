# app.py
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from bandit import Bandit

# --- Page Configuration ---
st.set_page_config(
    page_title="Bandit Hunter: A Bayesian Adventure",
    page_icon="🎯",
    layout="wide"
)

# --- Custom CSS for Styling ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# We will create this style.css file in the next step
# For now, let's inject CSS directly for simplicity
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');

html, body, [class*="st-"] {
    font-family: 'MedievalSharp', cursive;
}
.st-emotion-cache-1y4p8pa {
    background-color: #1a2a3a; /* Dark blue-gray background */
}
.st-emotion-cache-16txtl3 {
    padding: 2rem;
}
.st-emotion-cache-10trblm {
    color: #f0f2f6; /* Lighter text color */
}
div[data-testid="stMetric"] {
    background-color: #334155;
    border-radius: 10px;
    padding: 15px;
}
.stButton>button {
    border: 2px solid #f0f2f6;
    border-radius: 10px;
    color: #f0f2f6;
    background-color: transparent;
    transition: all 0.2s ease-in-out;
}
.stButton>button:hover {
    border-color: #facc15; /* Gold color on hover */
    color: #facc15;
}
</style>
""", unsafe_allow_html=True)


# --- Game Parameters ---
BANDITS_CONFIG = [
    {"name": "Skull Chest", "image_path": "assets/chest_1.png", "true_payout_prob": 0.25},
    {"name": "Gold Chest", "image_path": "assets/chest_2.png", "true_payout_prob": 0.60},
    {"name": "Bronze Chest", "image_path": "assets/chest_3.png", "true_payout_prob": 0.45},
    {"name": "Silver Chest", "image_path": "assets/chest_4.png", "true_payout_prob": 0.55},
    {"name": "Spooky Chest", "image_path": "assets/chest_5.png", "true_payout_prob": 0.30},
]
TOTAL_KEYS = 100

# --- Game State Initialization ---
if 'bandits' not in st.session_state:
    st.session_state.bandits = [Bandit(config["name"], config["true_payout_prob"]) for config in BANDITS_CONFIG]
    st.session_state.keys_remaining = TOTAL_KEYS
    st.session_state.total_treasure = 0
    st.session_state.game_log = []

# --- Header Section ---
st.title("🎯 Bandit Hunter: A Bayesian Adventure")
st.markdown(f"You have **{TOTAL_KEYS} keys** to uncover the secrets of the five chests. Choose wisely.")

if st.button("🔄 Start New Game"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- Main Layout ---
left_pane, right_pane = st.columns(2, gap="large")

with left_pane:
    st.header("The Five Chests of Mystery")
    
    score_cols = st.columns(2)
    score_cols[0].metric("🔑 Keys Remaining", st.session_state.keys_remaining)
    score_cols[1].metric("💰 Total Treasure", st.session_state.total_treasure)
    
    st.write("---")
    
    chest_cols = st.columns(len(st.session_state.bandits))
    for i, bandit in enumerate(st.session_state.bandits):
        with chest_cols[i]:
            st.image(BANDITS_CONFIG[i]["image_path"], use_column_width=True)
            if st.session_state.keys_remaining > 0:
                if st.button(f"Open {bandit.name}", key=f"bandit_{i}", use_container_width=True):
                    st.session_state.keys_remaining -= 1
                    result = bandit.pull()
                    bandit.update(result)
                    
                    if result == 1:
                        st.session_state.total_treasure += 1
                        log_message = f"🎉 TREASURE! The {bandit.name} yielded gold."
                        st.balloons()
                    else:
                        log_message = f"💨 Empty... The {bandit.name} was empty."
                    
                    st.session_state.game_log.append(log_message)
            else:
                st.button(f"Open {bandit.name}", key=f"bandit_{i}", use_container_width=True, disabled=True)

    if st.session_state.keys_remaining <= 0:
        st.warning(f"**Game Over!** You found {st.session_state.total_treasure} treasures.", icon="🏆")

    st.header("Captain's Log")
    log_container = st.container(height=200)
    for msg in reversed(st.session_state.game_log):
        log_container.write(msg)

with right_pane:
    st.header("Bayesian Belief Chart")
    st.write("Your belief about each chest's true payout rate, updated in real-time.")
    
    chart_data = []
    for bandit in st.session_state.bandits:
        x, y, name = bandit.get_pdf_data()
        for x_val, y_val in zip(x, y):
            chart_data.append({"x": x_val, "pdf": y_val, "Chest": name})

    df = pd.DataFrame(chart_data)

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('x', title='Hidden Payout Probability'),
        y=alt.Y('pdf', title='Density of Belief'),
        color=alt.Color('Chest', title="Chests"),
        tooltip=['Chest', 'x', 'pdf']
    ).properties(
        title="Belief Distributions for Chest Payout Rates"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)