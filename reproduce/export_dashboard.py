"""Write the datasets of the boards from tables.py's output.

Usage: python reproduce/export_dashboard.py page_data.json outdir/
"""
import json
import sys
from pathlib import Path


def r3(v):
    return None if v is None else round(v, 3)


def main(page_data, outdir):
    d = json.load(open(page_data, encoding='utf-8'))
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    def dump(name, rows):
        json.dump(rows, open(out / f'{name}.json', 'w', encoding='utf-8'), separators=(',', ':'))
        print(name, len(rows))

    dump('table_cells', [{'id': f"{t['key']}|{r['country']}|{col}", 'table': t['title'], 'country': r['country'],
                          'column': col, 'value': r3(r['values'][j])}
                         for t in d['tables'] for r in t['rows'] for j, col in enumerate(t['cols'])])

    names = {'authors_pmi': 'Authors PMI', 'papers_pmi': 'Publications PMI', 'citations_pmi': 'Citations PMI'}
    scalars = [{'id': f'r2_{k}', 'group': 'R²', 'n': v['n'],
                'label': f"{names[k.split('_vs_')[0]]} vs {'R&D' if k.endswith('rd') else 'HDI'}", 'value': r3(v['r2'])}
               for k, v in d['correlations'].items()]
    scalars += [{'id': 'authors', 'group': 'Dataset', 'label': 'Distinct authors', 'value': d['n_authors']},
                {'id': 'papers', 'group': 'Dataset', 'label': 'Distinct papers', 'value': d['n_papers']},
                {'id': 'region_papers', 'group': 'Dataset', 'label': 'Papers with an African affiliation',
                 'value': d['region_total_papers']},
                {'id': 'rank_authors', 'group': 'Dataset', 'label': 'Authors with a declared rank',
                 'value': d['authors_with_rank']},
                {'id': 'gender_known', 'group': 'Dataset', 'label': 'Authors with gender (p ≥ 0.9)',
                 'value': d['gender_known']},
                {'id': 'countries', 'group': 'Dataset', 'label': 'Countries with papers', 'value': len(d['COUNTRIES'])},
                {'id': 'records', 'group': 'Dataset', 'label': 'Author–institution records', 'value': d['n_records']}]
    dump('scalars', scalars)

    dump('country_metrics', [{'country': c, 'code': d['ISO3'][c], 'population': d['context'][c]['pop'],
                              'rd_avg': d['context'][c]['rd'], 'hdi_avg': d['context'][c]['hdi'],
                              **{k: r3(d['metrics'][c][k]) for k in ['authors', 'active_authors', 'papers', 'citations',
                                                                     'h_index', 'authors_pmi', 'papers_pmi',
                                                                     'citations_pmi']}}
                             for c in d['COUNTRIES']])
    dump('papers_per_year', [{'country': 'All Africa', 'year': int(y), 'papers': n}
                             for y, n in d['region_papers_per_year'].items()]
         + [{'country': c, 'year': int(y), 'papers': n}
            for c in d['COUNTRIES'] for y, n in d['metrics'][c]['papers_per_year'].items()])
    dump('world_share', [{k: r[k] for k in ['year', 'region_papers', 'world_papers', 'region_citations',
                                            'world_citations']} for r in d['world']])
    collab = [{'scope': 'Africa', 'row': a, 'col': b, 'pct': d['collab_region'][i][j]}
              for i, a in enumerate(d['COUNTRIES']) for j, b in enumerate(d['COUNTRIES'])]
    collab += [{'scope': 'World', 'row': a, 'col': b, 'pct': d['collab_world'][i][j]}
               for i, a in enumerate(d['COUNTRIES']) for j, b in enumerate(d['WORLD'])]
    dump('collab', collab)
    dump('mobility', d['mobility'])
    dump('phd_destination', d['phd_destination'])
    dump('gender_year', [{'year': int(y), 'authors': v['n'], 'female_pct': round(v['female_pct'], 2),
                          'ci95': round(v['ci95'], 2)} for y, v in d['gender_by_year'].items()])
    dump('gender_rank', [{'group': k, 'authors': v['n'], 'female_pct': round(v['female_pct'], 1),
                          'ci95': round(v['ci95'], 1)} for k, v in d['gender_by_rank'].items()])


if __name__ == '__main__':
    main(*sys.argv[1:3])
