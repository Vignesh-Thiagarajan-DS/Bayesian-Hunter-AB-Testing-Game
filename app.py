import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from bandit import Bandit
import base64
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(page_title="Bandit Hunter: A Bayesian Adventure", page_icon="🎯", layout="wide")

# --- Custom CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style.css")

st.markdown("""
<style>
/* This targets the text inside the tab buttons */
button[data-baseweb="tab"] > div > p {
    font-size: 1.1em;

}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Target the container for the tabs */
    div[data-testid="stTabs"] {
        font-size: 20px;
    }
    /* Target the individual tab buttons */
    button[data-baseweb="tab"] {
        font-size: 1.5em;
    }
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
label[data-testid="stWidgetLabel"] > div > p {
    font-size: 1.4em !important;
}
</style>
""", unsafe_allow_html=True)

# --- Helper function to embed images ---
def img_to_base64(image_path):
    path = Path(image_path)
    if path.exists():
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# --- Game Parameters ---
BANDITS_CONFIG = [
    {"name": "Wooden Chest", "image_path": "assets/wooden_chest.png", "true_payout_prob": 0.25},
    {"name": "Silver Chest", "image_path": "assets/silver_chest.png", "true_payout_prob": 0.50},
    {"name": "Golden Chest", "image_path": "assets/golden_chest.png", "true_payout_prob": 0.75},
]
TOTAL_KEYS = 10
TREASURE_GOAL = 5
EPSILON = 0.2

# --- Game State Initialization ---
if 'bandits' not in st.session_state:
    st.session_state.bandits = [Bandit(config["name"], config["true_payout_prob"]) for config in BANDITS_CONFIG]
    st.session_state.keys_remaining = TOTAL_KEYS
    st.session_state.total_treasure = 0
    st.session_state.last_result = None

# --- NEW: Callback function for button clicks ---
def handle_chest_click(chest_index):
    """This function handles the logic when a chest button is clicked."""
    if st.session_state.keys_remaining > 0:
        st.session_state.keys_remaining -= 1
        result = st.session_state.bandits[chest_index].pull()
        st.session_state.bandits[chest_index].update(result)
        if result == 1:
            st.session_state.total_treasure += 1
            st.session_state.last_result = {"message": f"Yayyy! You found 1 gold coin in the {BANDITS_CONFIG[chest_index]['name']}!"}
        else:
            st.session_state.last_result = {"message": f"The {BANDITS_CONFIG[chest_index]['name']} was empty."}

# --- Main Game Logic ---
def play_game():
    player_level = 1 + (st.session_state.total_treasure // 2)
    icon_base64 = img_to_base64("assets/user_icon.png")
    st.markdown(
        f'<div class="player-name">'
        f'<img src="data:image/png;base64,{icon_base64}">'
        f'<div class="player-name-text">{st.session_state.player_name}<br><span style="font-size: 0.8em; color: #facc15;">Level {player_level}</span></div>'
        f'</div>', unsafe_allow_html=True
    )

    st.title("Bandit Hunter: A Bayesian Adventure")
    st.markdown(f'<p style="font-size: 1.5em;">🏆 Treasure Goal: {st.session_state.total_treasure} / {TREASURE_GOAL} Coins Found</p>', unsafe_allow_html=True)
    progress_percent = min(st.session_state.total_treasure / TREASURE_GOAL, 1.0)
    st.progress(progress_percent, text="")

    if st.button("🔄 Start New Game"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

    left_pane, right_pane = st.columns([1.2, 1], gap="large")

    with left_pane:
      with st.container(border=True):
        notification_placeholder = st.empty()
        if st.session_state.last_result:
            if "Treasure" in st.session_state.last_result["message"]:
                notification_placeholder.success(st.session_state.last_result["message"], icon="🎉")
            else:
                notification_placeholder.info(st.session_state.last_result["message"], icon="💨")
        
        st.header("The Three Chests")
        score_cols = st.columns(2)
        with score_cols[0]:
            # Calculate the number of attempts used
            attempts_used = TOTAL_KEYS - st.session_state.keys_remaining
            
            # Display the new text and variable
            st.markdown(f'<p style="font-size: 1.5em;">🔑 Choose your treasure wisely: </p>', unsafe_allow_html=True)
            
            # Update the progress bar to reflect attempts used
            attempts_percent = 0
            st.progress(attempts_percent, text="")
        with score_cols[1]:
            st.markdown(f'<p style="font-size: 1.5em;">❤️ Lifeline: {st.session_state.keys_remaining} Keys Left</p>', unsafe_allow_html=True)
            lifeline_percent = st.session_state.keys_remaining / TOTAL_KEYS
            st.progress(lifeline_percent, text="")

        chest_cols = st.columns(len(st.session_state.bandits))
        for i, bandit in enumerate(chest_cols):
            with bandit:
                chest_image_base64 = img_to_base64(BANDITS_CONFIG[i]["image_path"])
                st.markdown(
                    f"<div class='chest-image-container' style='background-image: url(data:image/png;base64,{chest_image_base64})'></div>",
                    unsafe_allow_html=True
                )
                
                # UPDATED: Button now uses the on_click callback for instant, smooth updates
                st.button(
                    f"Open {BANDITS_CONFIG[i]['name']}", 
                    key=f"bandit_{i}", 
                    on_click=handle_chest_click, 
                    args=(i,), 
                    use_container_width=True,
                    disabled=(st.session_state.keys_remaining <= 0 or st.session_state.total_treasure >= TREASURE_GOAL)
                )
        
        # Check for win condition first, then game over
        if st.session_state.total_treasure >= TREASURE_GOAL:
            st.success(f"You Win! You reached the goal of {TREASURE_GOAL} treasures.", icon="🎉")
        elif st.session_state.keys_remaining <= 0:
            st.warning(f"Game Over! You found {st.session_state.total_treasure} treasures.", icon="🏆")

    with right_pane:
      with st.container(border=True):
        st.header("Bayesian Beliefs")
        tab1, tab2, tab3 = st.tabs(["Belief Curves", "Best Guess", "💡 Hints"])
        with tab1:
            chart_data_pdf = []
            for b in st.session_state.bandits:
                x, y, name = b.get_pdf_data()
                df_temp = pd.DataFrame({'p': x, 'd': y, 'c': name})
                chart_data_pdf.append(df_temp)
            df_pdf = pd.concat(chart_data_pdf)
# This is the updated code block
            pdf_chart = alt.Chart(df_pdf).mark_line(strokeWidth=4).encode(
                x=alt.X('p:Q', title='Hidden Payout Probability'),
                y=alt.Y('d:Q', title='Density of Belief'),
                color=alt.Color('c:N', title="Chests",
                    # ADD THIS SCALE to define custom colors
                    scale=alt.Scale(
                        domain=['Golden Chest', 'Silver Chest', 'Wooden Chest'],
                        range=[ "#824ADC",'#4FDB6D', '#DB4F89'] # Gold, Silver, Brown
                    )
                )
            ).properties(title="Live Belief Update for Each Chest").configure_axis(
                labelFontSize=14, titleFontSize=18
            ).configure_title(fontSize=22).configure_legend(titleFontSize=16, labelFontSize=14)
            st.altair_chart(pdf_chart, use_container_width=True)

        with tab2:
            chart_data_mean = [{"c": b.name, "bg": b.get_mean()} for b in st.session_state.bandits]
            df_mean = pd.DataFrame(chart_data_mean)
            
            bars = alt.Chart(df_mean).mark_bar().encode(
                x=alt.X('c:N', title="Chests", sort='-y'),
                y=alt.Y('bg:Q', title='Estimated Payout Probability', scale=alt.Scale(domain=[0, 1])),
                color=alt.Color('c:N', legend=None),
                tooltip=[alt.Tooltip('c'), alt.Tooltip('bg', title="Best Guess", format='.1%')]
            )
            # NEW: Text labels on the bars to highlight probabilities
            text = bars.mark_text(align='center', baseline='bottom', dy=-5, color='white', size=16).encode(
                text=alt.Text('bg:Q', format='.1%')
            )
            bar_chart = (bars + text).properties(title="Current Best Guess for Each Chest").configure_axis(
                labelFontSize=14, titleFontSize=18
            ).configure_title(fontSize=22)
            st.altair_chart(bar_chart, use_container_width=True)
        with tab3:
            total_pulls = TOTAL_KEYS - st.session_state.keys_remaining
            if total_pulls > 0:
                ucb_scores = [b.get_ucb_score(total_pulls) for b in st.session_state.bandits]
                ucb_choice_index = np.argmax(ucb_scores)
                ucb_choice_name = st.session_state.bandits[ucb_choice_index].name
                means = [b.get_mean() for b in st.session_state.bandits]
                greedy_exploit_name = st.session_state.bandits[np.argmax(means)].name
                
                st.info("💡 **Algorithm's Advice**", icon="🤖")
                
                # UPDATED: Side-by-side layout for hints
                hint_col1, hint_col2 = st.columns(2)
                with hint_col1:
                    st.subheader("Upper Confidence Bound")
                    st.success(f"Suggests: **{ucb_choice_name}**")
                    st.markdown("- **Strategy:** It balances finding the best chest with exploring uncertain ones.")
                    if st.session_state.bandits[ucb_choice_index].get_mean() < max(means):
                        st.markdown(f"- **Reasoning:** It sees the **{ucb_choice_name}** as a high-potential unknown that's worth exploring.")
                    else:
                        st.markdown(f"- **Reasoning:** It's confident that the **{ucb_choice_name}** is the best choice based on its proven high performance.")
                with hint_col2:
                    st.subheader("Epsilon-Greedy")
                    if np.random.random() < EPSILON:
                        greedy_choice_name = np.random.choice([b.name for b in st.session_state.bandits])
                        st.success(f"Suggests: **{greedy_choice_name}** (Explore)")
                        st.markdown("- **Strategy:** Most of the time it exploits the winner, but sometimes it takes a random chance.")
                        st.markdown(f"- **Reasoning:** With a {int(EPSILON*100)}% chance, it chose to **explore** a random chest to gather fresh data.")
                    else:
                        greedy_choice_name = greedy_exploit_name
                        st.success(f"Suggests: **{greedy_choice_name}** (Exploit)")
                        st.markdown("- **Strategy:** Most of the time it exploits the winner, but sometimes it takes a random chance.")
                        st.markdown(f"- **Reasoning:** With a {100-int(EPSILON*100)}% chance, it chose to **exploit** the proven winner.")
            else:
                st.info("Open any chest to get your first hint!", icon="💡")


    with st.container(border=True):
        st.header("🎓 The Math Behind the Magic")
        st.markdown("This game is a classic **Multi-Armed Bandit problem**. You have limited resources (keys) and must choose between **exploiting** the chest you think is best and **exploring** others to gather more data.")
        st.markdown("---")
        
        math_col1, math_col2, math_col3 = st.columns(3, gap="large")
        with math_col1:
            with st.container(border=True):
                st.subheader("Beta Distribution")
                st.markdown("Our **'belief'** about a chest's payout rate is represented by this distribution, which is updated with every click.")
                st.latex("\\text{Best Guess} = \\frac{\\alpha}{\\alpha + \\beta}")
        with math_col2:
            with st.container(border=True):
                st.subheader("UCB Algorithm")
                st.markdown("This formula balances choosing the known best option (exploitation) with trying out less-certain options (exploration).")
                st.latex("\\text{Score} = \\text{Mean} + \\sqrt{\\frac{2 \\ln(N)}{n_i}}")
        with math_col3:
            with st.container(border=True):
                st.subheader("Epsilon-Greedy")
                st.markdown("A simpler strategy: with probability **ε**, pick a random chest. Otherwise, pick the current best one.")
                st.latex("P(\\text{action}) = \\begin{cases} 1-\\epsilon & \\text{exploit} \\\\ \\epsilon & \\text{explore} \\end{cases}")
        
        st.subheader("Live Stats Tracker")
        selected_chest_name = st.selectbox("Choose a chest to inspect:", [b.name for b in st.session_state.bandits])
        selected_bandit = [b for b in st.session_state.bandits if b.name == selected_chest_name][0]
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)

        # UPDATED: Replaced st.metric with custom st.markdown for full style control
        with stat_col1:
            st.markdown(f"""
            <p style="font-size: 1.3em;">Successes (α - 1)</p>
            <p style="font-size: 2.5em; font-weight: bold;">{selected_bandit.alpha - 1}</p>
            """, unsafe_allow_html=True)
        
        with stat_col2:
            st.markdown(f"""
            <p style="font-size: 1.3em;">Failures (β - 1)</p>
            <p style="font-size: 2.5em; font-weight: bold;">{selected_bandit.beta - 1}</p>
            """, unsafe_allow_html=True)

        with stat_col3:
            mean_payout = selected_bandit.get_mean()
            st.markdown(f"""
            <p style="font-size: 1.3em; color: #facc15;">Current Best Guess</p>
            <p style="font-size: 2.5em; font-weight: bold; color: #facc15;">{mean_payout:.2%}</p>
            """, unsafe_allow_html=True)


# --- Welcome Screen Logic ---
if 'player_name' not in st.session_state:
    banner_base64 = img_to_base64("assets/banner.jpg")
    st.markdown(f'<div class="banner-container"><img src="data:image/jpeg;base64,{banner_base64}"></div>', unsafe_allow_html=True)
    
    # UPDATED: Side-by-side layout for title and name input
    title_col, input_col = st.columns([0.7, 0.3])
    with title_col:
        st.title("Welcome to 🎯 Bandit Hunter!")
    with input_col:
        # UPDATED: Using st.markdown for a custom, larger label
        st.markdown('<p class="welcome-input-label">Enter your player name to begin:</p>', unsafe_allow_html=True)
        name = st.text_input(
            "Enter your player name to begin:", 
            key="player_name_input",
            label_visibility="collapsed" # This hides the small, default label
        )
        if st.button("Start Adventure"):
            if name: 
                st.session_state.player_name = name
                st.rerun()
            else: 
                st.warning("Please enter a name.")
    
    st.markdown("---")
    st.header("What You'll Learn:")
    info_cols = st.columns(3, gap="large")
    with info_cols[0]:
        st.markdown('<div class="info-box"><h3>🎰 The Multi-Armed Bandit</h3><p>Imagine facing multiple slot machines ("bandits"), each with a secret payout rate. How do you find the best one before your money runs out?</p></div>', unsafe_allow_html=True)
    with info_cols[1]:
        st.markdown('<div class="info-box"><h3>⚖️ A/B Testing Strategy</h3><p>This is the core challenge of A/B testing: balancing **Exploitation** (using the best option) with **Exploration** (gathering more data). This game is a live test of that strategy.</p></div>', unsafe_allow_html=True)
    with info_cols[2]:
        st.markdown('<div class="info-box"><h3>🧠 Bayesian Inference</h3><p>The game maintains a "belief" about each chest. This belief updates with every click, getting more confident over time. This is Bayesian reasoning in action.</p></div>', unsafe_allow_html=True)

else:
    play_game()