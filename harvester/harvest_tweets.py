#!/usr/bin/env python3
#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#

import configparser
import logging
import sys
from tweet_crawler import TweetCrawler
from utils import configure_logging, BoundingBox
from database import DatabaseConn


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    base_config = config['crawler']
    configure_logging(base_config.get('logfile', None), log_level=int(base_config['loglevel']))
    couch_config = config['couchdb']

    with DatabaseConn(couch_config) as db:
        logger = logging.getLogger('tweet_crawler')

        crawler = TweetCrawler(config['twitter'],
                               BoundingBox(base_config['bbox']),
                               db,
                               logger)
        try:
            crawler.download_tweets()
        except KeyboardInterrupt:
            logger.info('interrupt received; disconnecting')
        except Exception as ex:
            logger.exception(ex)
        finally:
            crawler.disconnect()
            sys.exit(0)


if __name__ == '__main__':
    main()
