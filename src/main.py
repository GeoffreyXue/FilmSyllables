from SyllableVisualizer import SyllableVisualizer
from TranscriptScraper import TranscriptScraper

films_to_scrape = [
    ('The Social Network', r'https://imsdb.com/scripts/Social-Network,-The.html'),
    # ('The Matrix', r'https://imsdb.com/scripts/Matrix,-The.html'),
    # ('Ghostbusters', r'https://imsdb.com/scripts/Ghostbusters.html'),
    ('Frozen', r'https://imsdb.com/scripts/Frozen-(Disney).html')
    
]

ts = TranscriptScraper()
paths = ts.scrape_films("scraped", films_to_scrape)
ts.finish()

for i in range(len(paths)):
    sv = SyllableVisualizer(paths[i])
    sv.convert_and_save("output/v1", films_to_scrape[i][0])