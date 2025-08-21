# app.py
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from bandit import Bandit  # Import our new class

# --- Page Configuration ---
st.set_page_config(
    page_title="Bandit Hunter: An Interactive A/B Test",
    page_icon="🎯",
    layout="wide"
)

# --- Game Parameters ---
# Define our bandits with their secret payout probabilities
# We hide these from the player!
BANDITS_CONFIG = [
    {"name": "Skull Chest", "true_payout_prob": 0.25},
    {"name": "Gold Chest", "true_payout_prob": 0.60},
    {"name": "Bronze Chest", "true_payout_prob": 0.45},
    {"name": "Silver Chest", "true_payout_prob": 0.55},
    {"name": "Spooky Chest", "true_payout_prob": 0.30},
]
TOTAL_KEYS = 100

# --- Game State Initialization ---
# Use session_state to store game data across reruns
if 'bandits' not in st.session_state:
    st.session_state.bandits = [Bandit(config["name"], config["true_payout_prob"]) for config in BANDITS_CONFIG]
    st.session_state.keys_remaining = TOTAL_KEYS
    st.session_state.total_treasure = 0
    st.session_state.game_log = [] # To store messages for the player

# --- Page Title and Introduction ---
st.title("Bandit Hunter")
st.markdown(f"""
Welcome to Bandit Hunter! You have **{TOTAL_KEYS} keys** to open five treasure chests. 
Each chest has a different, secret probability of containing treasure. Your goal is to maximize your winnings.

This game is a live simulation of a **multi-armed bandit problem**, a classic dilemma in data science. 
As you play, the chart on the right will update your *belief* about each chest's payout rate. 
Will you **exploit** the chest you think is best, or **explore** others to gather more data?
""")

# --- Reset Button ---
if st.button("🔄 Start New Game"):
    # Clear the session state to reset the game
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun() # Rerun the script to re-initialize the game

# --- Layout ---
left_pane, right_pane = st.columns(2, gap="large")

with left_pane:
    st.header("The Treasure Chests")
    st.write("Click a chest to use a key!")

    # Display score and keys in a more prominent way
    score_cols = st.columns(2)
    score_cols[0].metric("🔑 Keys Remaining", st.session_state.keys_remaining)
    score_cols[1].metric("💰 Total Treasure", st.session_state.total_treasure)

    st.write("---")  # Divider

    # --- Create the buttons for each bandit ---
    # Use columns to lay them out neatly
    button_cols = st.columns(len(st.session_state.bandits))

    for i, bandit in enumerate(st.session_state.bandits):
        with button_cols[i]:
            # Check if we have keys left before showing the button
            if st.session_state.keys_remaining > 0:
                if st.button(f"Open {bandit.name}", key=f"bandit_{i}", use_container_width=True):
                    # --- This is the core game logic block ---

                    # 1. Use a key
                    st.session_state.keys_remaining -= 1

                    # 2. Pull the bandit's arm (open the chest)
                    result = bandit.pull()

                    # 3. Update the bandit's belief (alpha and beta)
                    bandit.update(result)

                    # 4. Update the total treasure
                    if result == 1:
                        st.session_state.total_treasure += 1
                        log_message = f"Success! Found treasure in the {bandit.name}."
                    else:
                        log_message = f"Empty. No treasure in the {bandit.name}."

                    # 5. Add to the game log
                    st.session_state.game_log.append(log_message)

            else:
                # Show a disabled button if no keys are left
                st.button(f"Open {bandit.name}", key=f"bandit_{i}", use_container_width=True, disabled=True)
    
    # --- Game Over Message ---
    if st.session_state.keys_remaining <= 0:
        st.warning(f"**Game Over!** You found a total of {st.session_state.total_treasure} treasures.", icon="🎉")


    # --- Display the game log ---
    st.write("📜 **Game Log**")
    log_container = st.container(height=200)
    for msg in reversed(st.session_state.game_log):
        log_container.write(msg)

with right_pane:
    st.header("Your Bayesian Beliefs")
    st.write("This chart shows the probability distribution of each chest's payout rate based on your results so far.")

    # Prepare data for Altair chart
    chart_data = []
    for bandit in st.session_state.bandits:
        x, y, name = bandit.get_pdf_data()
        # Associate the data with the bandit's name
        for x_val, y_val in zip(x, y):
            chart_data.append({"x": x_val, "pdf": y_val, "Chest": name})

    df = pd.DataFrame(chart_data)

    # Create the Altair chart
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('x', title='Hidden Payout Probability'),
        y=alt.Y('pdf', title='Probability Density'),
        color=alt.Color('Chest', title='Treasure Chests'),
        tooltip=['Chest', 'x', 'pdf']
    ).properties(
        title="Belief Distributions for Chest Payout Rates"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)