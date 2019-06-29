#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
import configparser
import json
import traceback

class AurinConnector:

    aurin_config = None
    data_files_meta = {}

    def __init__(self,config_path):
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            self.aurin_config = config['aurin']
            for data_key in self.aurin_config.keys():
                data_val = self.aurin_config[data_key]
                arr = data_val.split(":")
                self.data_files_meta[arr[0]] = arr[1]
            print(self.data_files_meta)
        except Exception as e:
            traceback.print_str()

    def get_data(self, dataset_name):
        with open(self.data_files_meta[dataset_name]) as data_file:
            return json.loads(data_file.read())

    def get_coordinates_info(self):
        with open(self.data_files_meta['coordinates_data']) as data_file:
            return json.loads(data_file.read())
