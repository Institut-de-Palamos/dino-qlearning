# 03. Q-learning tabular

La taula `Q(s, a)` guarda com de bona sembla cada acció `a` en cada estat `s`. Al principi tots els valors són zero: l'agent encara no té experiència.

## Escollir una acció

L'agent utilitza una estratègia epsilon-greedy:

1. Amb probabilitat `epsilon`, escull una acció aleatòria (exploració).
2. La resta de vegades, escull una acció amb el valor Q més alt (explotació).

Quan comença una partida, `epsilon` és alt. Després de cada partida baixa una mica, però no menys de `0.05`, perquè l'agent continuï provant alternatives.

## Actualitzar la taula

Després de cada pas, l'entorn retorna recompensa `r`, estat següent `s'` i si la partida ha acabat. L'actualització és:

$$
Q(s,a) \leftarrow Q(s,a) + \alpha\left[r + \gamma\max_{a'}Q(s',a') - Q(s,a)\right]
$$

- `alpha` (`0.1`) determina quant aprenem d'aquesta experiència.
- `gamma` (`0.95`) determina la importància de recompenses futures.
- `max Q(s', a')` és el millor valor estimat des de l'estat següent.

Si la partida acaba, no hi ha futur en aquell episodi i el terme futur és zero. Aquesta regla es comprova específicament als tests.

## Bucle d'entrenament

Per cada partida, `train.py` reinicia el joc. Després repeteix: tria una acció, executa un pas, actualitza la taula i continua amb el nou estat. També desa la puntuació més alta vista durant la partida i la mostra al resum. Aquesta puntuació del joc és diferent de la recompensa acumulada, que és el senyal utilitzat per aprendre. La partida s'atura en una col·lisió o en arribar al límit de passos.

Les taules desades amb la versió anterior (dues accions i estats de quatre camps) es migren en carregar-les: els valors de `WAIT` i `JUMP` es conserven, el valor inicial de `DUCK` és zero, i l'estat nou comença amb el dinosaure no ajupit. En desar, s'escriu el format nou.