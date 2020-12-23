import os
import pandas as pd
import json
import time


LOCAL_BASE_PATH = os.path.abspath(os.getcwd())
MOVIES_DIR_CSV = os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'movies'))

to_movies = os.listdir(MOVIES_DIR_CSV)
to_movies = list(map(lambda extracted: extracted.split('.')[0], to_movies))

dictionary = {}


for index, movie_id in enumerate(to_movies):
    print(str(index + 1) + '/' + str(len(to_movies)), movie_id)
    with open(os.path.abspath(os.path.join(MOVIES_DIR_CSV, movie_id + '.json'))) as read:
        text = read.read()
        text = json.loads(text)
        text = text['Plot']
        dictionary[str(movie_id)] = text

f = open(os.path.abspath(os.path.join(MOVIES_DIR_CSV, "plot.json")),'w')
f.write(json.dumps(dictionary))
f.close()
