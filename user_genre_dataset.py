import os
import pandas as pd
import json
from random import randrange

LOCAL_BASE_PATH = os.path.abspath(os.getcwd())
RATINGS_CSV = os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'dataset', 'ratings.csv'))
MOVIES_CSV = os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'dataset', 'movies.csv'))

ratings = pd.read_csv(RATINGS_CSV)
movies = pd.read_csv(MOVIES_CSV)

users_rated = list(ratings['userId'].unique())

json_file = {}

def getRandomIndex(length, percentage=50):
    return length * randrange(percentage) // 100

for user_rated in users_rated:
    print("User: ", user_rated)
    user_ratings = ratings.loc[ratings['userId'] == user_rated]
    counting_table = {}
    for index, row in user_ratings.iterrows():
        rating = row['rating']
        genres = str(movies.loc[movies['movieId'] == row['movieId']]['genres'].tolist()[0])
        for genre in genres.split('|'):
            accumulator = counting_table.get(genre, [0, 0.0])
            accumulator[0] = accumulator[0] + 1
            accumulator[1] = accumulator[1] + rating
            counting_table[genre] = accumulator
    counting_table = {k: v[1] / v[0] for k, v in counting_table.items()}
    result = list(counting_table.items())
    result.sort(reverse=True, key=lambda genre_rating : genre_rating[1])

    json_file[str(user_rated)] = {}
    like = list(map(lambda genre_rating : genre_rating[0], result[0:getRandomIndex(len(result))]))
    dislike = list(map(lambda genre_rating : genre_rating[0], result[len(result) - getRandomIndex(len(result)):len(result)]))

    for i in like:
        if i in dislike:
            print("Error")
            exit(1)

    json_file[str(user_rated)]['like'] = like
    json_file[str(user_rated)]['dislike'] = dislike

f = open(os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'dataset', "user_genre.json")),'w')
json.dump(json_file, f)
f.close()