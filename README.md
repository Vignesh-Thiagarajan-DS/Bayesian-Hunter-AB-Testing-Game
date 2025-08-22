<h1 align="center">Bandit Hunter: A Bayesian Adventure</h1>

<p align="center">
  <img src="assets/banner.jpg" alt="Bandit Hunter Banner">
</p>

> An interactive web application that turns a classic data science problem the **Multi-Armed Bandit** into an engaging game. This project is designed to provide a hands-on, visual understanding of Bayesian inference, A/B testing strategies, and the explore-exploit tradeoff.
>
<p align="center">
  <a href="https://medium.com/@Vignesh-Thiagarajan-DS/beyond-a-b-testing-understanding-multi-armed-bandits-with-an-interactive-game-461bd81e9241" target="_blank">
    <img src="https://img.shields.io/badge/Read_The_Full_Write--up-Medium-black?style=for-the-badge&logo=medium" alt="Read on Medium">
  </a>
  &nbsp;&nbsp;
  <a href="https://vignesh-bayesian-hunter-ab-testing-game.streamlit.app/" target="_blank">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit">
  </a>
</p>

<br>

<h3 align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#core-concepts">Core Concepts</a> •
  <a href="#how-to-run">How To Run</a> •
  <a href="#tech-stack">Tech Stack</a>
</h3>

---

<h2 id="live-demo">📽️ Live Demo</h2>

<p align="center">
  <br><br>
  ![Bandit Hunter Gameplay Demo](assets/gameplay-demo.gif) 
</p>

---

<h2 id="key-features">Key Features</h2>

* **Interactive Gameplay:** A simple and intuitive game where your choices directly impact the statistical model.
* **Real-Time Bayesian Visualization:** Watch the belief distributions for each chest update in real-time with every click.
* **Multiple Chart Types:** Switch between "Belief Curves" (Beta PDF) and "Best Guess" (Posterior Mean) to see the data from different perspectives.
* **Algorithmic Hints:** Get advice from two classic bandit algorithms—**Upper Confidence Bound** and **Epsilon-Greedy**—to compare your strategy against theirs.
* **In-Depth Explanations:** A dedicated pane explains the core mathematical concepts ($ \text{Beta Distribution}, \text{UCB Formula}$, etc.) with live stats from your game session.

---

<h2 id="core-concepts">Core Concepts Demonstrated</h2>

<h3 align="center">A/B Testing Framework</h3>

> The concept is simple and powerful: you create two or more versions of something (an ad, a webpage, a button), show them to different segments of your audience, and let the data tell you which one performs better. It’s a controlled experiment that takes the guesswork out of decision-making.

> In a traditional A/B test, you must commit to a fixed “exploration” period. You might decide to show Version A to some % of your users and Version B to the rest until you reach statistical significance.

<h3 align="center">The Multi-Armed Bandit Problem</h3>

> This is a classic thought experiment where a gambler must choose which slot machine ("one-armed bandit") to play, each with a different hidden payout rate. The goal is to maximize winnings by quickly identifying the best machine. This serves as a powerful analogy for many real-world problems like A/B testing, clinical trials, and resource allocation.

<h3 align="center">Bayesian Inference & The Beta-Bernoulli Model</h3>

> The game uses a **Bayesian approach** to learn about the chests. Instead of just calculating a simple win rate, we maintain a **probability distribution of our belief** for each chest's true payout rate. We start with an uncertain belief, and with each click, we update that belief using the new evidence. This is Bayes' Theorem in action:
> $$ P(\theta | D) = \frac{P(D | \theta) \cdot P(\theta)}{P(D)} $$
> Where θ is our belief about the payout rate and D is the new data (evidence).

<h3 align="center">The Explore-Exploit Tradeoff</h3>

> This is the fundamental dilemma of the game:
> * **Exploitation:** Do you keep opening the chest that has given you the most treasure so far? This maximizes your immediate, known rewards.
> * **Exploration:** Do you try other, less-known chests to gather more data, just in case one of them is secretly the best one? This invests resources for a potentially higher long-term reward.

---

<h2 id="how-to-run">How to Run Locally</h2>

To run this application on your local machine, please follow these steps.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Vignesh-Thiagarajan-DS/Bayesian-Hunter-AB-Testing-Game.git](https://github.com/Vignesh-Thiagarajan-DS/Bayesian-Hunter-AB-Testing-Game.git)
    cd Bayesian-Hunter-AB-Testing-Game
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
The application should now be open in your web browser!

---

<h2 id="tech-stack">Technology Stack</h2>

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core backend logic and computation. |
| **Streamlit** | Building the interactive web application UI. |
| **Pandas & NumPy** | Data manipulation and numerical operations. |
| **SciPy** | Statistical calculations (Beta distribution). |
| **Altair** | Declarative statistical visualizations. |