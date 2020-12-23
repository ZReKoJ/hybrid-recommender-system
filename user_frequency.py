import os
import pandas as pd
import json
from random import randrange

LOCAL_BASE_PATH = os.path.abspath(os.getcwd())
RATINGS_CSV = os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'dataset', 'ratings.csv'))
LINKS_CSV = os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'dataset', 'links.csv'))
FREQUENCY_DIR = os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'frequency'))
USER_FREQUENCY_DIR = os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'user_frequency'))

ds_ratings = pd.read_csv(RATINGS_CSV, dtype = str)
ds_links = pd.read_csv(LINKS_CSV, dtype = str)

users_rated = list(ds_ratings['userId'].unique())

json_file = {}

for index, user_rated in enumerate(users_rated):
    print(str(index + 1) + '/' + str(len(users_rated)), user_rated)
    user_movies = list(
        map(
            lambda movie_id : str(ds_links.loc[ds_links['movieId'] == str(movie_id), 'imdbId'].values[0]), 
            ds_ratings.loc[ds_ratings['userId'] == str(user_rated), 'movieId'].tolist()
        )
    )
    freqDict_list = {}

    for user_movie in user_movies:
        with open(os.path.abspath(os.path.join(FREQUENCY_DIR, user_movie + '.json'))) as read:
            text = read.read()
            freqDict_list[str(user_movie)] = json.loads(text)

    f = open(os.path.abspath(os.path.join(USER_FREQUENCY_DIR, str(user_rated) + ".json")),'w')
    json.dump(freqDict_list, f)
    f.close()