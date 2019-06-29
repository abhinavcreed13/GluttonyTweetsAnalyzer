#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
import logging
from sys import stderr


class BoundingBox:
    def __init__(self, bbox):
        sw, ne = bbox.split()
        self._sw = tuple(float(pos) for pos in sw.split(','))
        self._ne = tuple(float(pos) for pos in ne.split(','))

    def contains(self, coordinate):
        if type(coordinate) is dict:
            coordinate = coordinate['coordinates']
        return self._sw[0] < coordinate[0] < self._ne[0] and \
            self._sw[1] < coordinate[1] < self._ne[1]

    def as_locations(self):
        return (*self._sw, *self._ne)


def deep_filter_json(json, keep_keys):
    if keep_keys is True:
        return json
    return {
        k: deep_filter_json(v, keep_keys[k]) for k, v in json.items() if k in keep_keys
    }


def configure_logging(logfile, log_level=logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    format_str = '%(asctime)s (%(levelname)s) - %(name)s: %(message)s'

    if logfile is not None:
        file_handler = logging.FileHandler(filename=logfile, encoding='utf-8',
                                           mode='a')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(format_str))
        logger.addHandler(file_handler)

    # log info or higher messages to stderr
    stderr_handler = logging.StreamHandler(stderr)
    stderr_handler.setLevel(log_level)
    stderr_handler.setFormatter(logging.Formatter(format_str))
    logger.addHandler(stderr_handler)
