#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from flask import Flask, request, abort, send_from_directory
from flask_cors import CORS
import os
import configparser
from core.connectors.couch_connector import CouchConnector
from core.API.server_api import ServerAPI

# global setup
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'server/assets')
app = Flask(__name__)
cors = CORS(app)
_connectorConfig = 'config/connectors.ini'
_serverAPIinstance = None
_bufferCouchConnector = CouchConnector(_connectorConfig)

# For serving static files
@app.route('/')
def home():
    return send_from_directory(static_file_dir, 'templates/index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        abort(404)
    return send_from_directory(static_file_dir, path)

# API-endpoints
@app.route('/api/get_tweets_by_bbox', methods=['POST'])
def get_tweets_by_bbox():
    reqObj = request.json
    if reqObj["buffer_mode"] == True:
        return _serverAPIinstance.get_tweets_by_bbox_buffer(reqObj, _bufferCouchConnector)
    else:
        return _serverAPIinstance.get_tweets_by_bbox(reqObj)


@app.route('/api/get_data_from_aurin_by_bbox', methods=['POST'])
def get_data_from_aurin_by_bbox():
    reqObj = request.json
    return _serverAPIinstance.get_data_from_aurin_by_bbox(reqObj)

@app.route('/api/get_customized_aurin_data_by_bbox_gluttony', methods=['POST'])
def get_customized_aurin_data_by_bbox_gluttony():
    reqObj = request.json
    return _serverAPIinstance.get_customized_aurin_data_by_bbox_gluttony(reqObj)

@app.route('/api/get_restaurants_data', methods=['POST'])
def get_restaurants_data():
    reqObj = request.json
    return _serverAPIinstance.get_restaurants_data(reqObj)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config/globals.ini')
    globals = config['globals']
    _serverAPIinstance = ServerAPI(_connectorConfig)

    print('.....Server running on ' + globals['port'] + '.....')
    app.run(host=globals['host'], port=globals['port'])
