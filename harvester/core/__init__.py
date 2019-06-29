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

class CouchConnector:
    couch_client = None
    connector_config = None
    buffer_count = 0

    def __init__(self, config_path):
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            self.connector_config = config['couchdb']
            self.couch_client = CouchDB(self.connector_config['username'],
                                   self.connector_config['password'],
                                url=self.connector_config['url'], connect=True)
        except Exception as e:
            print('init')
            print(str(e))


    def buffer_tweets_object(self):
        try:
            ddoc = DesignDocument(self.couch_client[self.connector_config['database']], '_design/dataview')
            # Construct a View
            view = View(ddoc, 'get_data')
            #print("limit:"+self.connector_config['buffer']+","+"buffer:"+str(self.buffer_count))
            rows = view(include_docs=True, limit=int(self.connector_config['buffer']), skip=self.buffer_count)['rows']
            self.buffer_count = self.buffer_count + int(self.connector_config['buffer'])
            return rows
        except Exception as e:
            print('get_tweets')
            print(str(e))

    def release_connection(self):
        try:
            self.couch_client.disconnect()
        except Exception as e:
            print(str(e))
