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

# --- Custom CSS ---
def local_css(file_name):
    """Function to load a local CSS file."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

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
    # This whole section remains unchanged
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
    
    # --- NEW: EXPLAINER SECTION ---
    with st.expander("What does this chart mean? 🤔"):
        st.markdown("""
        This chart visualizes our **belief** about the true payout probability of each chest. This is a core concept in **Bayesian statistics**.

        - **X-axis**: The possible true payout rates (from 0% to 100%).
        - **Y-axis**: How likely we think each rate is. A higher peak means more certainty.
        - **Each Line**: Represents one chest.

        Initially, all lines are flat, meaning any payout rate is equally possible (total uncertainty). As you open a chest:
        - A **win** shifts the curve to the right (higher probability).
        - A **loss** shifts it to the left (lower probability).
        
        The more data you collect on a chest, the narrower and more confident its curve becomes!
        """)
    
    # --- Chart Generation (Unchanged) ---
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