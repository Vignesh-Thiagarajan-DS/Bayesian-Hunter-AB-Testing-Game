# app.py
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Bandit Hunter: An Interactive A/B Test",
    page_icon="🎯",
    layout="wide"
)

# --- Page Title and Introduction ---
st.title("🎯 Bandit Hunter")
st.markdown("""
Welcome to Bandit Hunter! You have **100 keys** to open five treasure chests. 
Each chest has a different, secret probability of containing treasure. Your goal is to maximize your winnings.

This game is a live simulation of a **multi-armed bandit problem**, a classic dilemma in data science. 
As you play, the chart on the right will update your *belief* about each chest's payout rate. 
Will you **exploit** the chest you think is best, or **explore** others to gather more data?
""")

# --- Layout ---
left_pane, right_pane = st.columns(2)

with left_pane:
    st.header("The Treasure Chests")
    st.write("Click a chest to use a key!")
    # We will add the chest buttons here later.

with right_pane:
    st.header("Your Bayesian Beliefs")
    st.write("The probability distributions will appear here.")
    # We will add the chart here later.