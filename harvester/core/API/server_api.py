#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
import configparser
import traceback

from flask import jsonify

from core.analysis.Aurin.ExtractAurin import ExtractAurin
from core.analysis.Aurin.formPlaceObjects import formListPlaceObjects
from core.connectors.aurin_connector import AurinConnector
from core.connectors.couch_connector import CouchConnector


class ServerAPI:
    _connector_config = None
    _global_config = None

    def __init__(self, connector_config):
        self._connector_config = connector_config
        config = configparser.ConfigParser()
        config.read('config/globals.ini')
        self._global_config = config['globals']

    def get_tweets_by_bbox(self, api_obj):
        print('get_tweets_by_bbox')
        valid_tweets = []
        _allowed_iterations = int(self._global_config['allowed_iterations'])
        _iterations = 0
        try:
            _couchConnector = CouchConnector(self._connector_config)
            _couchConnector.buffer_count = api_obj['buffer_count']

            def buffering_without_continuation():
                tweets = _couchConnector.buffer_tweets_object(api_obj['sin_key'])
                for tweet in tweets:
                    # print(tweet)
                    tweet_coords_arr = tweet['doc']['coordinates']['coordinates']
                    # print(api_obj['region_bbox'])
                    if self.check_tweet_with_bbox(tweet_coords_arr, api_obj['region_bbox']):
                        valid_tweets.append(tweet)

            while len(valid_tweets) < api_obj['minimum_tweets']:
                #print('buffering_without_continuation->' + str(len(valid_tweets)))
                buffering_without_continuation()
                _iterations = _iterations + 1
                if _iterations > _allowed_iterations:
                    break

            _couchConnector.release_connection()

            return jsonify({'data': valid_tweets, 'error': None})

        except Exception as ex:
            traceback.print_exc()
            return jsonify({'data': None, 'error': 'Exception Occurred'})

    def get_tweets_by_bbox_buffer(self, api_obj, _couch_connector):
        try:
            print('get_tweets_by_bbox')
            valid_tweets = []
            _allowed_iterations = int(self._global_config['allowed_iterations'])
            _iterations = 0

            def buffering_with_continuation():
                print(api_obj['sin_key'])
                tweets = _couch_connector.buffer_tweets_object(api_obj['sin_key'])
                for tweet in tweets:
                    # print(tweet)
                    tweet_coords_arr = tweet['doc']['coordinates']['coordinates']
                    # print(api_obj['region_bbox'])
                    if self.check_tweet_with_bbox(tweet_coords_arr, api_obj['region_bbox']):
                        valid_tweets.append(tweet)

            while len(valid_tweets) < api_obj['minimum_tweets']:
                print('buffering_with_continuation->' + str(len(valid_tweets)))
                buffering_with_continuation()
                _iterations = _iterations + 1
                if _iterations > _allowed_iterations:
                    break

            return jsonify({'data': valid_tweets, 'error': None})

        except Exception as ex:
            traceback.print_exc()
            return jsonify({'data': None, 'error': 'Exception Occurred'})

    def get_data_from_aurin_by_bbox(self, api_obj):
        print('get_data_from_aurin_by_bbox')
        valid_data = []
        try:
            _aurin_connector = AurinConnector(self._connector_config)

            data_obj = _aurin_connector.get_data(api_obj['dataset_name'])
            for feature in data_obj['features']:

                if 'boundedBy' in feature['properties']:
                    aurin_bbox = feature['properties']['boundedBy']
                    if self.aurin_data_with_bbox(aurin_bbox, api_obj['region_bbox']):
                        valid_data.append(feature)

                elif 'geometry' in feature:
                    aurin_coor = feature['geometry']['coordinates']
                    # print(feature)
                    # print(aurin_coor)
                    if self.aurin_data_with_coords(aurin_coor, api_obj['region_bbox']):
                        valid_data.append(feature)

            return jsonify({'data': valid_data, 'error': None})

        except Exception as ex:
            traceback.print_exc()
            return jsonify({'data': None, 'error': 'Exception Occurred'})

    def get_customized_aurin_data_by_bbox_gluttony(self, api_obj):
        print('get_customized_aurin_data_by_bbox_gluttony')
        try:
            _extract_aurin = ExtractAurin(self._connector_config)
            health_dict = _extract_aurin.getData(api_obj['dataset_name'])
            coordinates_dict = _extract_aurin.getCoordinatesData()
            # print(health_dict)
            # print(coordinates_dict)
            place_objects = formListPlaceObjects(dict(health_dict), dict(coordinates_dict))
            # evaluate(matched_tweet_objects, place_objects)
            # reduced_places = getReducedPlaces(place_objects)
            places = []
            for place_object in place_objects:
                if self.aurin_data_with_bbox(place_object.bounding_box, api_obj['region_bbox']):
                    places.append(vars(place_object))
            return jsonify({'data': places, 'error': None})
        except:
            traceback.print_exc()

    def check_tweet_with_bbox(self, tweet_coords_arr, bbox):
        x_coor = tweet_coords_arr[0]
        y_coor = tweet_coords_arr[1]
        if (x_coor >= bbox['xmin']) and (x_coor <= bbox['xmax']):
            if (y_coor >= bbox['ymin']) and (y_coor <= bbox['ymax']):
                return True
        return False

    def aurin_data_with_bbox(self, aurin_bbox, bbox):
        aurin_xmin = aurin_bbox[0]
        aurin_ymin = aurin_bbox[1]
        aurin_xmax = aurin_bbox[2]
        aurin_ymax = aurin_bbox[3]
        if (aurin_xmin >= bbox['xmin']) and (aurin_xmax <= bbox['xmax']):
            if (aurin_ymin >= bbox['ymin']) and (aurin_ymax <= bbox['ymax']):
                return True
        return False

    def aurin_data_with_coords(self, aurin_coors, bbox):
        try:
            aurin_xcoor = aurin_coors[0]
            aurin_ycoor = aurin_coors[1]
        except:
            try:
                # might be double array
                aurin_xcoor = aurin_coors[0][0]
                aurin_ycoor = aurin_coors[0][1]
            except:
                traceback.print_exc()
                return False
        if (aurin_xcoor >= bbox['xmin']) and (aurin_xcoor <= bbox['xmax']):
            if (aurin_ycoor >= bbox['ymin']) and (aurin_ycoor <= bbox['ymax']):
                return True
        return False
