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
import time
from database import DatabaseConn
from utils import configure_logging


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    base_config = config['crawler']
    configure_logging('user_db.log', log_level=20)
    couch_config = config['couchdb']

    with DatabaseConn(couch_config) as db_conn:
        logger = logging.getLogger('create_user_db')
        with db_conn.bulk_db as bulk_db, db_conn.user_db as user_db, open('users.txt') as f:
            for doc in bulk_db:
                if type(doc['user']) is int:
                    if 'added_at' in doc:
                        logger.info('deleting misplaced user %d' % doc['user'])
                        doc.delete()
                else:
                    user = doc['user']['id']
                    doc_id = str(user)
                    if doc_id not in user_db:
                        logger.info('adding new user %d' % user)
                        user_db.create_document({
                            '_id': doc_id,
                            'user': user,
                            'added_at': int(time.time())
                        })
