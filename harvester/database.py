#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from cloudant.client import CouchDB
from contextlib import AbstractContextManager, contextmanager
from threading import RLock


class DatabaseError(Exception):
    pass


class DatabaseConn(AbstractContextManager):
    def __init__(self, config):
        self._config = config

        self._db = CouchDB(config['username'],
                           config['password'],
                           url=config['url'],
                           connect=True)
        self._bulk_db = None
        self._bulk_db_lock = RLock()
        self._user_db = None
        self._user_db_lock = RLock()
        self._relevant_db = None
        self._relevant_db_lock = RLock()

    @property
    @contextmanager
    def bulk_db(self):
        if self._bulk_db is None:
            self._bulk_db = self._get_or_create_db(self._config['database'])
        with self._bulk_db_lock:
            yield self._bulk_db

    @property
    @contextmanager
    def user_db(self):
        if self._user_db is None:
            self._user_db = self._get_or_create_db(self._config['user_db'])
        with self._user_db_lock:
            yield self._user_db

    @property
    @contextmanager
    def relevant_db(self):
        if self._relevant_db is None:
            self._relevant_db = self._get_or_create_db(self._config['relevant_db'])
        with self._relevant_db_lock:
            yield self._relevant_db

    def _get_or_create_db(self, db_name):
        if db_name in self._db:
            return self._db[db_name]

        db = self._db.create_database(db_name)
        if db.exists():
            return db
        raise DatabaseError('failed to create database {}'.format(db_name))

    def __enter__(self):
        self._db.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._db.disconnect()
