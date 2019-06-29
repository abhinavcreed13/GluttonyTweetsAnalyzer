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

class TestConnector:

    def __init__(self):
        # CouchConnector
        _conn = CouchConnector('config/connectors.ini')
        #while (1):
        # r= _conn.buffer_tweets_object()

        # # AurinConnector - to get data from Aurin json file
        #
        # _aurin = AurinConnector('config/connectors.ini')
        # print(_aurin.get_data())

    def getTweets(self):
        _conn= CouchConnector('config/connectors.ini')
        return _conn.buffer_tweets_object()
