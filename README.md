# Blackjack Card Counting Simulation

This repository contains a Python implementation of a Blackjack card counting simulation. The simulation is designed to test the effectiveness of various card counting strategies in Blackjack, particularly under different conditions of the game. It includes custom rules such as the ability to avoid betting when the count is unfavorable, as well as varying betting amounts based on the true count.

## Features

- **Custom Blackjack Rules**:
  - Blackjack pays 3:2.
  - Dealer stands on soft 17.
  - Doubling allowed on any initial hand.
  - Re-splitting aces is allowed.
  - No early surrender.

- **Card Counting Strategy**:
  - Uses the Hi-Opt II card counting system.
  - Adjusts bets based on the true count:
    - No bet when true count is ≤ 0.
    - Double the base bet when the true count is between 1 and 3.
    - Bet 5 times the base bet when the true count is ≥ 4.

- **Simulation Capabilities**:
  - Simulates multiple series of games.
  - Calculates the expected value of the bankroll, total amount wagered, and return on investment (ROI).
  - Configurable number of games and series for in-depth analysis.

## Requirements

- Python 3.x
- NumPy

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/blackjack-simulation.git
cd blackjack-simulation
Install the required dependencies:
pip install numpy
