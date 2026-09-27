# Q-learning amb Chrome Dino

Exemple didàctic de Q-learning tabular amb Python. L'agent juga amb la còpia local de Chrome Dino a `dino/index.html` mitjançant Playwright; no cal obrir cap pàgina externa. L'algorisme no importa ni coneix Playwright: només treballa amb estats, accions i recompenses.

## Preparació

Cal Python 3.10 o superior. Des de l'arrel del projecte:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
playwright install chromium
```

## Entrenament

```bash
python train.py --episodes 30
```

Per amagar la finestra del navegador:

```bash
python train.py --episodes 30 --headless
```

Es pot canviar l'adreça del joc o la llavor aleatòria amb `--url` i `--seed`. L'agent comença explorant molt i redueix gradualment aquesta exploració. El resum de cada partida mostra la puntuació màxima del Dino i la recompensa acumulada de l'agent per separat.

## Com està organitzat

- `src/dino_qlearning/qlearning.py`: selecció d'accions i actualització Q.
- `src/dino_qlearning/states.py`: conversió de mesures a estats discrets.
- `src/dino_qlearning/browser_env.py`: connexió Playwright, lectura del joc, teclat i recompenses.
- `train.py`: bucle d'entrenament que uneix agent i entorn.
- `docs/`: explicació pas a pas per a l'aula.

Comença per [docs/00-preparacio.md](docs/00-preparacio.md) i continua en ordre.