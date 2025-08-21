# bandit.py
import numpy as np
from scipy.stats import beta

class Bandit:
    """
    Represents a single treasure chest (a 'bandit arm').
    
    Args:
        name (str): The name or identifier for the bandit.
        true_payout_prob (float): The actual, hidden probability of a payout.
    """
    def __init__(self, name: str, true_payout_prob: float):
        self.name = name
        self.true_payout_prob = true_payout_prob
        # Start with a non-informative prior: Beta(alpha=1, beta=1)
        self.alpha = 1
        self.beta = 1

    def pull(self) -> int:
        """
        Simulates pulling the bandit's arm (opening the chest).
        Returns 1 for a win (treasure), 0 for a loss (empty).
        """
        return 1 if np.random.random() < self.true_payout_prob else 0

    def update(self, result: int):
        """
        Updates the Beta distribution parameters based on the result.
        
        Args:
            result (int): 1 for a win, 0 for a loss.
        """
        if result == 1:
            self.alpha += 1
        else:
            self.beta += 1
            
    def get_pdf_data(self) -> tuple[np.ndarray, np.ndarray, str]:
        """
        Generates the data needed to plot the Beta distribution's PDF.

        Returns:
            A tuple containing x-values, y-values, and the bandit's name.
        """
        x = np.linspace(0, 1, 200)
        y = beta.pdf(x, self.alpha, self.beta)
        return x, y, self.name