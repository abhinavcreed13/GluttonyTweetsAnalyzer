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
from nltk.tokenize import WordPunctTokenizer
from collections import Counter
from nltk.corpus import stopwords




def getTweets(tweet_corpus):
    with open(tweet_corpus) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    tweets = [x.strip() for x in content]
    return tweets

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

def update(word_count_in_corpus,tweet):
    preprocessedText=re.sub("#","",cleanTweetText(tweet.text).lower())
    stop_words = set(stopwords.words('english'))
    list_of_words=preprocessedText.split(" ")
    for word in list_of_words:
        if word in stop_words:
            pass
        else:
            if word in word_count_in_corpus:
                word_count_in_corpus[word]+=1
            else:
                word_count_in_corpus[word]=1
    return word_count_in_corpus


def getPopularWords(corpus_tweets,n):
    tweets=formListOfTweets(corpus_tweets)
    word_count_in_corpus={}
    for tweet in tweets:
        # print(tweet.text)
        word_count_in_corpus=update(word_count_in_corpus,tweet)
        # print(word_count_in_corpus)
    return dict(Counter(word_count_in_corpus).most_common(n))

