import os
import pandas as pd
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize.regexp import (WordPunctTokenizer,wordpunct_tokenize)

LOCAL_BASE_PATH = os.path.abspath(os.getcwd())
MOVIES_DIR = os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'movies'))
FREQUENCY_DIR = os.path.abspath(os.path.join(LOCAL_BASE_PATH, 'frequency'))

to_movies = os.listdir(MOVIES_DIR)
to_movies = list(map(lambda extracted: extracted.split('.')[0], to_movies))

def preprocess_text(doc):
    stopset = set(stopwords.words('english'))
    stemmer = SnowballStemmer('english',ignore_stopwords=True)
    tokens = wordpunct_tokenize(doc)
    clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
    stemmed_text = [stemmer.stem(word) for word in clean]
    return stemmed_text

for index, movie_id in enumerate(to_movies):
    print(str(index + 1) + '/' + str(len(to_movies)), movie_id)
    with open(os.path.abspath(os.path.join(MOVIES_DIR, movie_id + '.json'))) as read:
        text = read.read()
        text = json.loads(text)
        text = text['Plot']
        words = preprocess_text(text)
        dictionary = {}
        for word in set(words):
            dictionary[word] = words.count(word)
                
        f = open(os.path.abspath(os.path.join(FREQUENCY_DIR, movie_id + '.json')),'w')
        f.write(json.dumps(dictionary))
        f.close()
