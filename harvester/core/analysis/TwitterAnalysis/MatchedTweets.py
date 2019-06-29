#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from core.analysis.TwitterAnalysis.Tweet import Tweet
import re
from os.path import join, dirname
from nltk.tokenize import WordPunctTokenizer
from collections import Counter
from nltk.corpus import stopwords

def getGluttonyWords():
    with open(join(dirname(__file__), '..', 'Resources', 'words_matters.txt'), 'r') as f:
        return [line.strip() for line in f.readlines()]


def formListOfTweets(tweets):
    """
    converting the twitter object from Couch DB to the format of Tweet Class with the object containing id, text,
    coordinates and hashtags

    :param tweets: The tweets from COuch DB
    :return: List[Tweet(id,text,coordinates,hashtags)]
    """
    list_of_tweets = []

    for tweet in tweets:
        try:
            text = tweet["doc"]["full_text"]
        except:
            text = tweet["doc"]["text"]
        list_of_tweets.append(Tweet(tweet["id"],
                                    text,
                                    tweet["doc"]["coordinates"]["coordinates"],
                                    tweet["doc"]["entities"]["hashtags"],
                                    tweet["doc"]["user"]["screen_name"],
                                    tweet["doc"]["user"]["id"],
                                    tweet["doc"]["created_at"]))
    return list_of_tweets


def cleanTweetText(text):
    """
    cleans the tweet's text content
    :param text: The text of the tweet
    :return: cleaned tweet
    """
    user_removed = re.sub(r'@[A-Za-z0-9]+', '', text)
    link_removed = re.sub('https?://[A-Za-z0-9./]+', '', user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    lower_case_tweet = number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    clean_tweet = (' '.join(words)).strip()
    return clean_tweet

def gluttonyTest(text, gluttony_words):
    preprocessedText=re.sub("#","",cleanTweetText(text).lower())
    list_of_words=preprocessedText.split(" ")
    for word in list_of_words:
        if word in gluttony_words:
            return True
        else:
            return False


def getReduceTweets(corpus_tweets):
    tweets=formListOfTweets(corpus_tweets)
    gluttony_words=getGluttonyWords()
    matched_tweets=[]
    for tweet in tweets:
        # print(tweet.text)
        if gluttonyTest(tweet.text, gluttony_words):
            matched_tweets.append(tweet)
    return matched_tweets
