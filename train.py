"""Train the tabular agent by playing repeated Chrome Dino episodes."""

import argparse
from pathlib import Path

from dino_qlearning.browser_env import BrowserDinoEnv, DEFAULT_GAME_URL
from dino_qlearning.qlearning import QLearningAgent


def train(
    episodes: int,
    max_steps: int,
    url: str,
    headless: bool,
    seed: int,
    store: str | None = None,
) -> None:
    agent = QLearningAgent(seed=seed)
    store_path = Path(store) if store is not None else None

    if store_path is not None and store_path.exists():
        agent.load(store_path)
        print(f"Taula Q carregada de {store_path}")

    with BrowserDinoEnv(url=url, headless=headless) as environment:
        for episode in range(1, episodes + 1):
            state = environment.reset()
            episode_reward = 0.0
            max_score = 0
            done = False

            for _ in range(max_steps):
                action = agent.choose_action(state)
                next_state, reward, done, score = environment.step(action)
                agent.learn(state, action, reward, next_state, done)
                state = next_state
                episode_reward += reward
                max_score = max(max_score, score)

                if done:
                    break

            agent.exploration = max(0.05, agent.exploration * 0.97)
            result = "xoc" if done else "límit de passos"
            print(
                f"Partida {episode:03}: {result}; "
                f"puntuació màxima={max_score}; "
                f"recompensa={episode_reward:.1f}; "
                f"exploració={agent.exploration:.2f}"
            )

    if store_path is not None:
        agent.save(store_path)
        print(f"Taula Q desada a {store_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Entrena Q-learning al joc Dino.")
    parser.add_argument("--episodes", type=int, default=30, help="Nombre de partides.")
    parser.add_argument("--max-steps", type=int, default=500, help="Passos màxims per partida.")
    parser.add_argument("--url", default=DEFAULT_GAME_URL, help="URL del joc Dino.")
    parser.add_argument("--headless", action="store_true", help="Amaga la finestra del navegador.")
    parser.add_argument("--seed", type=int, default=7, help="Llavor per repetir l'experiment.")
    parser.add_argument(
        "--store",
        nargs="?",
        const="models/q_table.json",
        default=None,
        metavar="FITXER.json",
        help="Carrega i desa la taula Q (per defecte: models/q_table.json).",
    )
    arguments = parser.parse_args()

    train(
        episodes=arguments.episodes,
        max_steps=arguments.max_steps,
        url=arguments.url,
        headless=arguments.headless,
        seed=arguments.seed,
        store=arguments.store,
    )


if __name__ == "__main__":
    main()