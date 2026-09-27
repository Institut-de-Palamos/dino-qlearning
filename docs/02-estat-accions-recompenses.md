# 02. Estat, accions i recompenses

Abans d'aprendre, cal definir què pot observar i fer l'agent.

## Estat

`browser_env.py` llegeix la distància fins al següent obstacle, el tipus d'obstacle, si el dinosaure està saltant i la velocitat actual. `states.py` agrupa aquests valors en quatre nombres enters:

1. Distància en trams de 50 píxels, limitada a 300 píxels.
2. Tipus d'obstacle: 0 si no n'hi ha, 1 per cactus i 2 per pterodàctil.
3. Estat del salt: 0 a terra i 1 saltant.
4. Velocitat: 0 per sota de 10 i 1 a partir de 10.

Per exemple, `(2, 2, 1, 1)` representa un pterodàctil a una distància aproximada de 100 a 149 píxels, amb el dinosaure saltant i velocitat alta. Agrupar mesures redueix el nombre d'entrades de la taula, tot i que fa perdre precisió.

## Accions

- `WAIT` (`0`): no prémer cap tecla.
- `JUMP` (`1`): prémer espai.

## Recompensa

Cada pas sense col·lisió dona `+1`, perquè sobreviure més temps és millor. Una col·lisió dona `-100` i acaba l'episodi. La recompensa és una decisió de disseny: canviar-la pot fer que l'agent aprengui una conducta diferent.

`browser_env.py` és l'únic lloc que tradueix l'estat del joc i les tecles a aquests valors senzills.