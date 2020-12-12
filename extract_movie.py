import os
import pandas as pd
import requests

LOCAL_BASE_PATH = os.path.abspath(os.getcwd())
LINKS_PATH = os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'dataset', 'links.csv'))

API_KEY = '5ade2ff'
API_KEY = '1ad91603'
URL = 'http://www.omdbapi.com/'

PARAMS = {
    'i': '',
    'apikey': API_KEY,
    'plot': 'full'
}

def getInfo(id, count):
    PARAMS['i'] = str(id).rjust(9, 't')
    api_url = URL + '?' + '&'.join(list(map(lambda key_value : str(key_value[0]) + '=' + str(key_value[1]), PARAMS.items())))
    #api_url = 'https://zrekoj.github.io/hybrid-recommender-system/movies/5192124.json'
    r = requests.get(api_url)
    if r.status_code == 200:
        print(count, id)
        f = open(os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'movies', str(id) + ".json")),'w')
        f.write(r.text)
        f.close()
        return 1
    else:
        print(count, r.text)
        return 0

links = pd.read_csv(LINKS_PATH)
to_movies = os.listdir(os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'movies')))
to_movies = list(map(lambda extracted: extracted.split('.')[0], to_movies))
from_movies = list(map(lambda key: str(key).rjust(7, '0'), links['imdbId'].tolist()))

from_count = len(from_movies)
to_count = len(to_movies)
count = 0

for i in from_movies:
    if i not in to_movies:
        count = count + getInfo(i, count)

print('Total movies:', from_count)
print('Initial extracted:', to_count)
print('Added new:', count)