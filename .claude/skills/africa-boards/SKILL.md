---
name: africa-boards
description: Work with this repository's African HEP data (data/inspire_Africa.json.gz from INSPIRE-HEP, 54 countries) and its boards - rebuild the data, compute the indicators (authors, papers, citations, h-index, ranks, mobility, PhD destinations, collaborations, gender, R&D and HDI correlations), build the self-contained HTML board, add new indicators or tabs, or answer a question from the data. Use whenever someone working in a clone of restrepo/inspireauth_CfA asks for any of these.
---

# African HEP boards

Run from the repository root with Python ≥ 3.10, after `pip install -r reproduce/requirements.txt`.

## Pipeline

```bash
python build/context.py                                  # countries.json: ISO codes, INSPIRE names, World Bank, UNDP
python build/build_inspire.py [--countries ZA GH ...]     # data/inspire_Africa.json.gz; --countries for a quick test
python reproduce/reproduce.py data/inspire_Africa.json.gz out/results.json [--year YYYY]
python reproduce/tables.py out/results.json out/page_data.json
python reproduce/export_dashboard.py out/page_data.json out/dash/
python reproduce/standalone.py out/dash/ out/board.html
```

- **The download** makes several thousand requests to INSPIRE-HEP and takes tens of minutes. Run it in
  the background. It is cached in `build/cache/`: use a new `--cache` folder per date, because an old
  cache returns old data.
- **Counting rules:** those of restrepo/inspireauth (see `reproduce/reproduce.py`).
- **Countries without papers** are left out of the tables, matrices and charts.

## Add an indicator

1. **Compute it** in `reproduce.py` `main()`, as `out['<key>'] = …`.
2. **Copy it through** in `tables.py`, by adding the key to the list copied into `out`.
3. **Export it** in `export_dashboard.py`, with `dump('<key>', rows)`, where `rows` is a list of flat
   dicts.
4. **Title it** in `reproduce/board_datasets.py`.
5. **Draw it** in `reproduce/dashboard/index.html`:
   - a card in a tab `<section>`;
   - a `<div class="chart" data-draw="name" data-source="<key>">`;
   - `dash.draw('name', (el) => …)` with d3 v7, copying an existing drawer.
6. **Rebuild and check:** run the pipeline again, open `out/board.html`, and check that every tab
   draws with no console errors.

A one-off question needs no board: read the data with a short script and state the counting rule used.

## Publish

Work on a branch and open a pull request, never on `main`.

- **The data:** `data/inspire_Africa.json.gz` is an ordinary git file. Never commit an uncompressed JSON
  or use Git LFS.
- **The boards:** releases tagged `v*` rebuild the data and the board, and add it to GitHub Pages
  (`gh-pages` branch, `reproduce/pages_index.py`).
