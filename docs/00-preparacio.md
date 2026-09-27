# 00. Preparació

## 1. Crear l'entorn de Python

Un entorn virtual manté les dependències d'aquest projecte separades de les de l'ordinador:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Instal·lar Playwright

El paquet instal·la la biblioteca Python. L'ordre següent descarrega Chromium, el navegador que Playwright controlarà:

```bash
python -m pip install -e .
playwright install chromium
```

## 3. Executar una primera sessió

```bash
python train.py --episodes 5
```

La finestra del navegador és visible per defecte per poder observar les decisions. A Linux sense entorn gràfic, afegeix `--headless`. El nombre de passos màxim per partida es pot ajustar amb `--max-steps`.

Les proves ràpides del Q-learning es poden executar sense obrir Chromium:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Per defecte s'obre la còpia inclosa a `dino/index.html` amb una URL `file://`; no cal Internet. Es pot indicar una altra pàgina compatible amb `--url`, però l'adaptador espera trobar-hi la interfície JavaScript `Runner.instance_` del joc.