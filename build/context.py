"""Write data/countries.json: the 54 African countries with their INSPIRE-HEP name and context.

For each country (ISO 3166 alpha-2 code):
- name: the country name INSPIRE-HEP uses in institution addresses (the World Bank name if INSPIRE
  has no institution there);
- population: World Bank SP.POP.TOTL, latest year available;
- rd_avg: World Bank GB.XPD.RSDV.GD.ZS (R&D expenditure, % of GDP), average of the years available
  from 1996 on (null if none);
- hdi_avg: UNDP Human Development Index, average of 1990-2022 (HDR 2023-24 time series; null if none).

Usage: python build/context.py [data/countries.json]
"""
import csv
import io
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

AFRICA = ['DZ', 'AO', 'BJ', 'BW', 'BF', 'BI', 'CV', 'CM', 'CF', 'TD', 'KM', 'CG', 'CD', 'CI', 'DJ', 'EG', 'GQ',
          'ER', 'SZ', 'ET', 'GA', 'GM', 'GH', 'GN', 'GW', 'KE', 'LS', 'LR', 'LY', 'MG', 'MW', 'ML', 'MR', 'MU',
          'MA', 'MZ', 'NA', 'NE', 'NG', 'RW', 'ST', 'SN', 'SC', 'SL', 'SO', 'ZA', 'SS', 'SD', 'TZ', 'TG', 'TN',
          'UG', 'ZM', 'ZW']
WB = 'https://api.worldbank.org/v2'
HDR = 'https://hdr.undp.org/sites/default/files/2023-24_HDR/HDR23-24_Composite_indices_complete_time_series.csv'


def get(url, raw=False):
    for k in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (inspireauth_CfA build)'})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            time.sleep(0.3)
            return data if raw else json.loads(data)
        except OSError as e:
            print(f'retry {k + 1}: {e}', file=sys.stderr)
            time.sleep(5 * (k + 1))
    raise RuntimeError(url)


def wb_series(indicator, start):
    """{iso3: {year: value}} for every country, from the World Bank API."""
    out = {}
    d = get(f'{WB}/country/all/indicator/{indicator}?format=json&date={start}:2025&per_page=20000')
    for r in d[1] or []:
        if r['value'] is not None:
            out.setdefault(r['countryiso3code'], {})[int(r['date'])] = r['value']
    return out


def main(out_path):
    wb = {c['iso2Code']: c for c in get(f'{WB}/country?format=json&per_page=400')[1]}
    pop = wb_series('SP.POP.TOTL', 2015)
    rd = wb_series('GB.XPD.RSDV.GD.ZS', 1996)
    hdi = {}
    for r in csv.DictReader(io.StringIO(get(HDR, raw=True).decode('latin-1'))):
        vals = [float(r[f'hdi_{y}']) for y in range(1990, 2023) if r.get(f'hdi_{y}')]
        if vals:
            hdi[r['iso3']] = sum(vals) / len(vals)
    countries = []
    for iso2 in AFRICA:
        iso3 = wb[iso2]['id']
        q = urllib.parse.quote(f'addresses.country_code:{iso2}')
        hits = get(f'https://inspirehep.net/api/institutions?size=1&q={q}&fields=addresses.country')['hits']['hits']
        name = next((a.get('country') for h in hits for a in h['metadata'].get('addresses') or [] if a.get('country')),
                    wb[iso2]['name'])
        p = pop.get(iso3, {})
        r = rd.get(iso3, {})
        countries.append({'iso2': iso2, 'iso3': iso3, 'name': name,
                          'population': p[max(p)] if p else None,
                          'rd_avg': round(sum(r.values()) / len(r), 3) if r else None,
                          'hdi_avg': round(hdi[iso3], 3) if iso3 in hdi else None})
        print(iso2, name, countries[-1]['population'], countries[-1]['rd_avg'], countries[-1]['hdi_avg'])
    Path(out_path).write_text(json.dumps(countries, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'data/countries.json')
