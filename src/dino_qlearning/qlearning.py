"""The tabular Q-learning algorithm, independent of any game or browser."""

import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

from dino_qlearning.states import State

WAIT = 0
JUMP = 1
DUCK = 2


class QLearningAgent:
    def __init__(
        self,
        action_count: int = 3,
        learning_rate: float = 0.1,
        discount: float = 0.95,
        exploration: float = 1.0,
        seed: int | None = None,
    ) -> None:
        self.action_count = action_count
        self.learning_rate = learning_rate
        self.discount = discount
        self.exploration = exploration
        self.q_values: dict[State, list[float]] = defaultdict(
            lambda: [0.0] * self.action_count
        )
        self.random = random.Random(seed)

    def choose_action(self, state: State) -> int:
        """Explore sometimes; otherwise choose an action with the best value."""
        if self.random.random() < self.exploration:
            return self.random.randrange(self.action_count)

        values = self.q_values[state]
        best_value = max(values)
        best_actions = [index for index, value in enumerate(values) if value == best_value]
        return self.random.choice(best_actions)

    def learn(
        self,
        state: State,
        action: int,
        reward: float,
        next_state: State,
        done: bool,
    ) -> None:
        """Apply one Bellman update to Q(state, action)."""
        future_value = 0.0 if done else max(self.q_values[next_state])
        old_value = self.q_values[state][action]
        target = reward + self.discount * future_value
        self.q_values[state][action] = old_value + self.learning_rate * (target - old_value)