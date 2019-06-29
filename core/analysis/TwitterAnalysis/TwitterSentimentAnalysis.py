#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from core.analysis.TwitterAnalysis.Tweet import Tweet
from core.analysis.WrathAnalysis.SentimentAnalyzerEngine import sentimentAnalyzerEngine
import re
from nltk.tokenize import WordPunctTokenizer
import operator
from itertools import islice
from collections import Counter

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


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

def formListOfTweets(tweets):
    """
    converting the twitter object from Couch DB to the format of Tweet Class with the object containing id, text,
    coordinates and hashtags

    :param tweets: The tweets from COuch DB
    :return: List[Tweet(id,text,coordinates,hashtags)]
    """
    list_of_tweets = []
    for tweet in tweets:
        list_of_tweets.append(Tweet(tweet["id"], tweet["doc"]["full_text"], tweet["doc"]["coordinates"]["coordinates"],
                                    tweet["doc"]["entities"]["hashtags"]))
    return list_of_tweets

def getHashtagsCounts(list_of_tweets):
    dict_of_hastags={}
    for tweet in list_of_tweets:
        for hashtag in tweet.hashtags:
            if hashtag["text"].lower() in dict_of_hastags:
                dict_of_hastags[hashtag["text"].lower()]+=1
            else:
                dict_of_hastags[hashtag["text"].lower()]=1
    return dict_of_hastags
def getMostPopularHashtags(dict_of_hashtags:dict, n):
    return dict(Counter(dict_of_hashtags).most_common(n))

def checkWrathOnHashtags(tweet):
    """
    check if wrath words are present on tweet hashtags
    :param tweet: Tweet(id,text,coordinates,hashtags)
    :return: Boolean
    """
    for hashtag in tweet.hashtags:
        if hashtag in list(dict.fromkeys(open("core/analysis/Resources/positive.txt", 'r').read().split(','))):
            return True

def checkWrathOnText(tweet):
    """
    check if wrath words are present on tweet text
    :param tweet: Tweet(id,text,coordinates,hashtags)
    :return: Boolean
    """
    if sentimentAnalyzerEngine(cleanTweetText(tweet.text)):
        return True

def reduceTweets(list_of_tweets):
    """
    reducing List[Tweet(id,text,coordinates,hashtags)] based on wrath
    :param list_of_tweets: List[Tweet(id,text,coordinates,hashtags)]
    :return: List[Tweet(id,text,coordinates,hashtags)]
    """
    list_of_classified_tweets = []
    for tweet in list_of_tweets:
        if checkWrathOnHashtags(tweet):
            list_of_classified_tweets.append(tweet)
        elif checkWrathOnText(tweet):
            list_of_classified_tweets.append(tweet)
        else:
            pass
    return list_of_classified_tweets

def topHashtags(tweets,n):
    return getMostPopularHashtags(getHashtagsCounts(formListOfTweets(tweets)),n)

def tweetsSentimentAnalysis(tweets):
    """
    performing wrath analysis on tweets from Couch DB
    :param tweets: list of tweets from Couch DB
    :return: wrath Tweet objects
    """
    return reduceTweets(formListOfTweets(tweets))
