# inspireauth_CfA

INSPIRE-HEP author records for **Africa**, and the boards of their scientific indicators in high-energy
physics, cosmology and astroparticle physics. This is the African counterpart of
[restrepo/inspireauth](https://github.com/restrepo/inspireauth), which holds the Latin American data of
*Statistical Analysis of Scientific Metrics in High Energy, Cosmology, and Astroparticle Physics in
Latin America* (M. Morales-Alvarado, F. Quevedo, M. Ramos-Hamud, D. Restrepo). It uses the same code
and the same counting rules, for the 54 African countries.

**Boards:** <https://restrepo.github.io/inspireauth_CfA/>. Each board is a self-contained page,
which also works offline.

## The data

`data/inspire_Africa.json.gz` is a gzipped JSON list with one record per author and institution, in
the schema of restrepo/inspireauth (see its README). It contains every author of the INSPIRE-HEP papers
with at most 10 authors of each African institution, with their INSPIRE profile (positions,
identifiers, advisors), each paper's rank and affiliation at publication, and a gender inferred from
the first name with [genderize-offline](https://pypi.org/project/genderize-offline/). Read it with:

```python
import gzip, json
with gzip.open('data/inspire_Africa.json.gz', 'rt', encoding='utf-8') as f:
    records = json.load(f)
```

`data/countries.json` lists the 54 countries (ISO codes, INSPIRE-HEP name), with population and R&D
(% of GDP, average since 1996) from the World Bank, and HDI (average 1990–2022) from UNDP.
`data/world_papers.csv` holds the global INSPIRE-HEP output used for the regional share (up to 2021).

## Updating

Publishing a GitHub release whose tag starts with `v` runs
[`update-data.yml`](.github/workflows/update-data.yml). The workflow:

1. downloads the data again;
2. builds the board;
3. attaches both to the release;
4. opens a pull request that puts them on `main`;
5. adds the board to GitHub Pages.

By hand:

```bash
pip install -r reproduce/requirements.txt
python build/context.py                      # data/countries.json (World Bank, UNDP, INSPIRE names)
python build/build_inspire.py                # data/inspire_Africa.json.gz (tens of minutes; cached in build/cache/)
python reproduce/reproduce.py data/inspire_Africa.json.gz out/results.json
python reproduce/tables.py out/results.json out/page_data.json
python reproduce/export_dashboard.py out/page_data.json out/dash/
python reproduce/standalone.py out/dash/ out/board.html
```

The repository includes a skill for Claude Code (`.claude/skills/africa-boards`), so you can ask for
new indicators in plain language after cloning it.

## Licence

Data from INSPIRE-HEP (CC0), the World Bank (CC BY 4.0) and UNDP. Genders come from the World Gender
Name Dictionary 2.0 (CC0); they are name-based estimates, not self-reported gender.
