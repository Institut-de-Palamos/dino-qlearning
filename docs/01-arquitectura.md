# 01. Arquitectura

El projecte separa l'algorisme de l'entorn per tal que puguem estudiar Q-learning sense haver de llegir codi de browser.

```text
train.py
  | estat, acció, recompensa
  v
qlearning.py  <---->  states.py

train.py
  | reset() / step(action)
  v
browser_env.py
  | Playwright, teclat i Runner.instance_
  v
dino/index.html
```

## Responsabilitats

- `qlearning.py` conté una taula de valors i dues operacions: escollir una acció i aprendre d'una transició.
- `states.py` transforma mesures contínues del joc en una tupla petita que es pot utilitzar com a clau de la taula.
- `browser_env.py` amaga els detalls del navegador. Per a l'entrenament només ofereix `reset()` i `step(action)`.
- `train.py` implementa el bucle: observar, actuar, rebre resultat, aprendre i repetir.

Aquesta frontera facilita canviar el browser o substituir-lo per un entorn simulat sense reescriure l'agent.
