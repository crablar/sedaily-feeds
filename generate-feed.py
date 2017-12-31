import os
from pathlib import Path
from urllib import urlopen
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import euclidean_distances
import textract
import diffbot

diffbot_token = '347a6722701beff34951a7cc865e7295'
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
    print "FAILLLLL"
    return "FAIL"

#print get_transcript('react-router-flux-and-web-debates-with-michael-jackson')

def get_article_content (url):
    result = diffbot_client.api('article', url)
    return result

article = get_article_content("https://cointelegraph.com/news/bitcoin-ethereum-bitcoin-cash-ripple-iota-litecoin-dash-monero-price-analysis-dec-30")

# Load user

# For each episode user listened to, extract the transcript and add to corpus

# For each article

# 