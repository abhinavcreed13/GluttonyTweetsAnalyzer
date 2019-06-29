#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from core.connectors.couch_connector import CouchConnector
from core.connectors.aurin_connector import AurinConnector

class ExtractTweets:
    def buffer_tweets(selfs, couch_connector):
        """
        get tweets from couch DB
        :param couch_connector: Couch DB conncetor
        :return: 100 tweets per request
        """
        #testing couch connector
        tweets=couch_connector.buffer_tweets_object()
        return tweets




