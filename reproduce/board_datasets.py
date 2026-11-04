"""Titles and descriptions of the board's datasets (shown in the board's Sources section)."""

DATASETS = {
    'table_cells': ('Indicator tables', 'Each indicator of each African country with papers: authors, publications, '
                    'citations, h-index (totals, per million inhabitants and per author) and declared ranks.'),
    'scalars': ('Dataset totals and R²', 'Totals of the dataset and the R² of the fits against R&D and HDI.'),
    'country_metrics': ('Country metrics and context', 'Per country: population and R&D (World Bank), HDI (UNDP), '
                        'and the authors, papers, citations and h-index.'),
    'papers_per_year': ('Articles per year', 'Articles of each country, and of Africa as a whole, by publication year.'),
    'world_share': ('Africa vs global output', 'African papers and citations per year beside the global output of '
                    'INSPIRE-HEP (citable papers with ten or fewer authors, up to 2021).'),
    'collab': ('Collaboration matrices', "Share of a country's articles co-authored with another country."),
    'mobility': ('Ranks and where they published', 'Authors with a declared rank in a country, by the rank and region '
                 'under which they published.'),
    'phd_destination': ('Where African PhDs go', 'Current or latest later position of the authors who held a PhD '
                        'position in an African country.'),
    'gender_year': ('Female fraction per year', 'Female fraction of the authors who published each year, with its '
                    '95% margin; genders inferred with genderize-offline (World Gender Name Dictionary 2.0).'),
    'gender_rank': ('Female fraction by rank', 'Authors holding a declared rank in a year in which they published, '
                    'with the female fraction and its 95% margin.'),
}
