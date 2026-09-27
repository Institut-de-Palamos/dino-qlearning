"""The tabular Q-learning algorithm, independent of any game or browser."""

import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

from dino_qlearning.states import State

WAIT = 0
JUMP = 1


class QLearningAgent:
    def __init__(
        self,
        action_count: int = 2,
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

    def save(self, path: str | Path) -> None:
        """Save the table and learning settings as a readable JSON file."""
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": 1,
            "action_count": self.action_count,
            "learning_rate": self.learning_rate,
            "discount": self.discount,
            "exploration": self.exploration,
            "q_values": [
                {"state": list(state), "values": values}
                for state, values in sorted(self.q_values.items())
            ],
        }
        destination.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def load(self, path: str | Path) -> None:
        """Load a previously saved table and its learning settings."""
        source = Path(path)
        data: dict[str, Any] = json.loads(source.read_text(encoding="utf-8"))
        if data.get("version") != 1:
            raise ValueError(f"Unsupported Q-table version in {source}")
        if data["action_count"] != self.action_count:
            raise ValueError(
                f"The saved table has {data['action_count']} actions; "
                f"this agent expects {self.action_count}."
            )

        loaded_values: dict[State, list[float]] = {}
        for entry in data["q_values"]:
            state = tuple(entry["state"])
            values = entry["values"]
            if len(state) != 4 or len(values) != self.action_count:
                raise ValueError(f"Invalid Q-table entry in {source}: {entry}")
            loaded_values[state] = [float(value) for value in values]

        self.learning_rate = float(data["learning_rate"])
        self.discount = float(data["discount"])
        self.exploration = float(data["exploration"])
        self.q_values = defaultdict(
            lambda: [0.0] * self.action_count,
            loaded_values,
        )