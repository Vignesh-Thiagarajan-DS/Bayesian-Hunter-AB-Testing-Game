import numpy as np
from scipy.stats import beta

class Bandit:
    def __init__(self, name: str, true_payout_prob: float):
        self.name = name
        self.true_payout_prob = true_payout_prob
        self.alpha = 1
        self.beta = 1
        # NEW: Added back tracking for UCB calculation
        self.pull_count = 0
        self.wins = 0

    def pull(self) -> int:
        return 1 if np.random.random() < self.true_payout_prob else 0

    def update(self, result: int):
        # UPDATED: Now updates all stats
        self.pull_count += 1
        if result == 1:
            self.alpha += 1
            self.wins += 1
        else:
            self.beta += 1
            
    def get_pdf_data(self) -> tuple[np.ndarray, np.ndarray, str]:
        x = np.linspace(0, 1, 200)
        y = beta.pdf(x, self.alpha, self.beta)
        return x, y, self.name

    def get_mean(self) -> float:
        return self.alpha / (self.alpha + self.beta)

    def get_ucb_score(self, total_pulls: int) -> float:
        """NEW: Calculates the UCB1 score for the hint feature."""
        if self.pull_count == 0:
            return float('inf')
        
        mean_payout = self.wins / self.pull_count
        exploration_bonus = np.sqrt(2 * np.log(total_pulls) / self.pull_count)
        return mean_payout + exploration_bonus