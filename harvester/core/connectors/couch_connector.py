#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from cloudant.client import CouchDB
from cloudant.view import View
from cloudant.design_document import DesignDocument
import configparser
import traceback

class CouchConnector:
    couch_client = None
    connector_config = None
    sins_config_map = {}
    buffer_count = 0

    def __init__(self, config_path):
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            self.connector_config = config['couchdb']

            self.sins_config = config['sins']
            for data_key in self.sins_config.keys():
                data_val = self.sins_config[data_key]
                arr = data_val.split(":")
                self.sins_config_map[arr[0]] = (arr[1], arr[2], arr[3], arr[4])

            print(self.sins_config_map)
            self.couch_client = CouchDB(self.connector_config['username'],
                                        self.connector_config['password'],
                                        url=self.connector_config['url'], connect=True)
        except Exception as e:
            print('init')
            traceback.print_exc()
            print(str(e))

    def buffer_tweets_object(self, sin_key):
        try:
            #print('buffer_tweets_object')
            sin_config_tup = self.sins_config_map[sin_key]
            #print(sin_config_tup)
            ddoc = DesignDocument(self.couch_client[sin_config_tup[0]], sin_config_tup[1])
            # Construct a View
            view = View(ddoc, sin_config_tup[2])
            # print("limit:"+self.connector_config['buffer']+","+"buffer:"+str(self.buffer_count))
            rows = view(include_docs=True, limit=int(sin_config_tup[3]), skip=self.buffer_count)['rows']
            self.buffer_count = self.buffer_count + int(sin_config_tup[3])
            #print(rows)
            return rows
        except Exception as e:
            print('get_tweets')
            print(str(e))

    def release_connection(self):
        try:
            self.couch_client.disconnect()
        except Exception as e:
            traceback.print_exc()
            print(str(e))
