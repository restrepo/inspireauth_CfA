"""Arrange reproduce.py's results into the tables and series of the boards.

Usage: python reproduce/tables.py results.json page_data.json
"""
import json
import sys

from reproduce import CONTEXT, COUNTRY_INFO, RANKS, WORLD

ISO3 = {c['name']: c['iso3'] for c in COUNTRY_INFO}


def main(res_path, out_path):
    res = json.load(open(res_path, encoding='utf-8'))
    cc = res['countries']
    active = res['active_countries']
    tables = []

    def add(key, title, cols, values):
        tables.append({'key': key, 'title': title, 'cols': cols,
                       'rows': [{'country': c, 'values': values(c)} for c in active]})

    add('authors', 'Authors', ['Total authors', 'Active authors', 'Total PMI', 'Active PMI'],
        lambda c: [cc[c]['authors'], cc[c]['active_authors'], cc[c]['authors_pmi'], cc[c]['active_pmi']])
    add('publications', 'Publications', ['Total', 'PMI', 'Per author'],
        lambda c: [cc[c]['papers'], cc[c]['papers_pmi'], cc[c]['papers_per_author']])
    add('citations', 'Citations', ['Total', 'PMI', 'Per author'],
        lambda c: [cc[c]['citations'], cc[c]['citations_pmi'], cc[c]['citations_per_author']])
    add('hindex', 'h-index', ['h-index', 'PMI', 'Per author'],
        lambda c: [cc[c]['h_index'], cc[c]['h_pmi'], cc[c]['h_per_author']])
    rank_cols = ['Senior', 'Junior', 'Staff', 'Postdoc', 'PhD', 'Master', 'Undergrad', 'Visitor', 'Other']
    add('ranks_authors', 'Declared ranks by country', rank_cols,
        lambda c: [res['ranks_authors'][c][k] for k in RANKS])
    add('ranks_papers', 'Papers by rank at publication', rank_cols,
        lambda c: [res['ranks_papers'][c][k] for k in RANKS])

    out = {k: res[k] for k in ['current_year', 'n_records', 'n_authors', 'n_papers', 'region_total_papers',
                                'gender_known', 'authors_with_rank', 'collab_region', 'collab_world', 'world',
                                'gender_by_year', 'gender_by_rank', 'correlations', 'mobility',
                                'phd_destination', 'region_papers_per_year']}
    out.update({'COUNTRIES': active, 'WORLD': WORLD, 'ISO3': ISO3, 'tables': tables,
                'context': {c: {'pop': CONTEXT[c][0], 'rd': CONTEXT[c][1], 'hdi': CONTEXT[c][2]} for c in active},
                'metrics': {c: cc[c] for c in active}})
    json.dump(out, open(out_path, 'w', encoding='utf-8'))
    print(f"{len(active)} countries with papers; {res['n_authors']} authors, {res['n_papers']} papers")


if __name__ == '__main__':
    main(*sys.argv[1:3])
