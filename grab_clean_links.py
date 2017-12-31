import json
from pprint import pprint
import os
from pathlib import Path
from urllib import urlopen
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import euclidean_distances
import textract
import diffbot

diffbot_token = os.environ['DIFFBOT_TOKEN']
diffbot_client = diffbot.Client(token=diffbot_token)

results = []

with open("./test_cases/article_list.txt") as f:
    urls = f.readlines()
    for url in urls:
        result = diffbot_client.api('article', url)
        title = result["objects"][0]["title"]
        text = result["objects"][0]["text"]
        results.append({"title":title,"text":text})

with open('./test_cases/sample_articles.json', 'w') as outfile:
    json.dump(results, outfile)