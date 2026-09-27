# 04. Adaptador Playwright

`browser_env.py` implementa l'entorn amb dues funcions simples:

- `reset()` inicia una partida i retorna el primer estat.
- `step(action)` envia l'acció, espera una fracció de segon i retorna `(estat, xoc, puntuació)`. No decideix la recompensa: aquesta regla pertany a `train.py`. Per `DUCK`, manté premuda la fletxa avall durant l'observació i després l'allibera.

Per observar el joc, l'adaptador consulta `Runner.instance_` a la pàgina. D'aquí llegeix la posició del dinosaure, el següent obstacle, la velocitat i si hi ha hagut una col·lisió. Envia la tecla espai per saltar. Cap d'aquests detalls arriba a `qlearning.py`.

Per defecte, Playwright obre `dino/index.html` des del disc local. Aquesta còpia exposa `Runner.instance_`, amb `playing`, `crashed`, `tRex.jumping`, `tRex.ducking`, `currentSpeed`, els obstacles de `horizon.obstacles` i el mètode `restart()`. La puntuació es calcula amb la mateixa conversió del marcador del joc a partir de `distanceRan`. L'adaptador fa servir aquests detalls només aquí. Si es canvia la còpia o la seva API, caldrà adaptar només `browser_env.py`. La finestra es mostra per defecte; `--headless` la manté oculta.