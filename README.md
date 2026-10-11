# Delta City 3D

`index.html` is the whole game in one file. Open it in a browser, or host it with GitHub Pages.

## Hosting on GitHub Pages
1. Put `index.html` at the top level of the repository.
2. In the repository: Settings, Pages, Source "Deploy from a branch", Branch `main`, folder `/ (root)`, Save.
3. After a minute or two the game is at `https://<your-user-name>.github.io/<repository-name>/`.

## The `source` folder
`index.html` is built from these files. They are not needed to play, only to change the game.

- `source/town/town.src.html` – the drawing engine, every building design, and each state's street plan.
- `source/town/bank_tail.js`, `immigration_tail.js`, `gov_tail.js` – the insides of the banks, Immigration, and the government buildings.
- `source/town/walker_tail.js` – the characters and their recorded movement.
- `source/town/build_asaba.py` – joins everything into `index.html` and holds the game's own logic (map, routes, car, doors, chooser).
- `source/models/*.json` – the converted models: airport terminal, car, Henry, Zoey (`party2`), Tracy (`club`).
- `source/character/woman.json` – Violet.
- `source/anim/anims.json` – the recorded movements.
- `source/models/pack_*.py`, `source/anim/*.py` – the converters that made those files from the original downloads.

To rebuild: keep the folder layout the build script expects (it reads the models and movements by path), then run `python3 build_asaba.py` inside `source/town`.
