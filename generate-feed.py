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

def get_transcript (slug):
    transcript_file = Path('./transcripts/' + slug + '.pdf')
    if transcript_file.is_file():
        return textract.process('./transcripts/' + slug + '.pdf')
    transcript_file = Path('./transcripts/' + slug + '.txt')
    if transcript_file.is_file():
        path = './transcripts/' + slug + '.txt'
        with open(path, 'r') as transcript_file:
            return transcript_file.read()
    print "failed to get " + slug 
    return "FAIL"
   
# Load user and random links
user = json.load(open('./test_cases/bitcoin_bob.json'))
random_links = json.load(open('./test_cases/sample_articles.json'))

corpus = []

# For each episode user listened to, extract the transcript and add to corpus"
for episode in user["episodes_listened"]:
    episode_content = get_transcript(episode["slug"])
    corpus.append(episode_content)

index_of_first_random_article = len(corpus)

print ("For each article in random links, add to corpus...")
for article in random_links:
    corpus.append(article["text"])

print ("Make tfidf vectors for everything...")
vectorizer = CountVectorizer()
counts = vectorizer.fit_transform(corpus).toarray()
transformer = TfidfTransformer(smooth_idf=False)
tfidf = transformer.fit_transform(counts).toarray()

episode_vectors = tfidf[0:index_of_first_random_article]
link_vectors = tfidf[index_of_first_random_article:len(corpus)]

link_distance_mappings = []

for i in range(0, len(link_vectors)):
    link_title = random_links[i]["title"]
    link_vector = link_vectors[i]
    distances = euclidean_distances([link_vector],episode_vectors)
    distance_sum = sum(distances[0])
    link_distance_mappings.append({"title" : link_title, "distance_sum" : distance_sum})

link_distance_mappings = sorted(link_distance_mappings, key=lambda k: k['distance_sum']) 

# compare the article vector to each of the listened episode vectors. sum the distances
# rank the articles by summed distances
# weight the distances by what percentage of an episode was listened to 