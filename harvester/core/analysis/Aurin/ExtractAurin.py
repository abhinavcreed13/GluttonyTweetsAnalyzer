#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from core.connectors.aurin_connector import AurinConnector

class ExtractAurin:

    _aurinConnector = None

    def __init__(self, config_key):
        self._aurinConnector = AurinConnector(config_key)

    def getData(self, aurin_data_key):
        return self._aurinConnector.get_data(aurin_data_key)

    def getCoordinatesData(self):
        return self._aurinConnector.get_coordinates_info()


