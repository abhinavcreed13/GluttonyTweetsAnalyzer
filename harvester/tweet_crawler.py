#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from queue import PriorityQueue
from utils import deep_filter_json
from core.analysis.TwitterAnalysis.MatchedTweets import gluttonyTest, getGluttonyWords
from random import randint
import time
import tweepy


class TweetCrawler(tweepy.StreamListener):
    BULK_KEEP_KEYS = {
        'created_at': True,
        'coordinates': True,
        'geo': True,
        'id': True,
        'text': True,
        'full_text': True,
        'entities': True,
        'place': True,
        'user': {
            'created_at': True,
            'description': True,
            'entities': True,
            'followers_count': True,
            'following': True,
            'friends_count': True,
            'id': True,
            'lang': True,
            'location': True,
            'name': True,
            'screen_name': True,
            'statuses_count': True,
            'time_zone': True,
            'url': True,
            'utc_offset': True
        }
    }

    def __init__(self, config, bbox, db, logger):
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(config['access_token_key'], config['access_token_secret'])
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self._db = db
        self._stream = None
        self._logger = logger
        self._bbox = bbox

        self._seed_terms = self._get_search_terms(config, config.get('seed_search_term_file', None))
        self._seed_size = int(config['seed_size'])
        self._seed_geocode = config['seed_geocode']
        self._queue = PriorityQueue()
        self._tweet_history = set()
        self._user_history = set(int(user_id) for user_id in config.get('blacklist', '').split(','))
        self._valid_tweet_count = 0

        self._gluttony_words = getGluttonyWords()

    def _get_search_terms(self, config, search_term_file):
        if search_term_file is None:
            return { config['seed_search_term'].strip() }

        with open(search_term_file, 'r', encoding='UTF-8') as f:
            return set(filter(lambda s: len(s) > 0, (s.strip() for s in f.readlines())))

    def _seed(self):
        self._logger.info('seeding tweet download queue')
        seeded_tweets = 0
        found_tweets = 0
        for tweet in tweepy.Cursor(self.api.search,
                                   ' OR '.join(self._seed_terms) + ' exclude:retweets',
                                   geocode=self._seed_geocode,
                                   result_type='recent',
                                   count=100,
                                   tweet_mode='extended').items():
            found_tweets += 1
            if self._process_tweet(tweet):
                self._queue_user(tweet.author)
                seeded_tweets += 1
        self._logger.info('seeding complete')
        self._logger.info(('found {} valid tweets from {} users, of which {} were new (out of {} '
                           'tweets downloaded)').format(seeded_tweets, self._queue.qsize(),
                                                        self._valid_tweet_count, found_tweets))

    def _process_tweet(self, tweet, queue_priority=0):
        self._logger.debug('got tweet {} from user {}'.format(tweet.id, tweet.author.id))

        if tweet.id not in self._tweet_history:
            self._tweet_history.add(tweet.id)
            with self._db.bulk_db as db:
                if self._tweet_has_valid_location(tweet) and tweet.id_str not in db:
                    self._logger.debug('valid tweet location; saving tweet {}'.format(tweet.id))

                    tweet_json = deep_filter_json(tweet._json, TweetCrawler.BULK_KEEP_KEYS)
                    tweet_json['_id'] = tweet.id_str

                    # this is a little bit of a hack: since places were ignored for the original
                    # db entries we rely on coordinates rather than allowing use of place
                    if ('coordinates' not in tweet_json or
                        type(tweet_json['coordinates']) is not dict) and \
                            tweet.place is not None:
                        self._logger.debug('saving tweet {} by place'.format(tweet.id))
                        tweet_json['coordinates'] = {
                            'type': 'Point',
                            'coordinates': tweet.place.bounding_box.origin()
                        }

                    self._save_tweet(tweet_json)
                    if self._is_relevant_tweet(tweet_json):
                        self._save_relevant_tweet(tweet_json)

                    self._queue_user(tweet.author, queue_priority)
                    return True
        return self._tweet_has_valid_location(tweet)

    def _save_tweet(self, tweet_json):
        with self._db.bulk_db as db:
            self._valid_tweet_count += 1

            doc = db.create_document(tweet_json)
            if doc.exists():
                self._logger.debug('successfully saved tweet {} to db'.format(tweet_json['_id']))
            else:
                self._logger.warning('failed to save tweet {} to db'.format(tweet_json['_id']))

    def _is_relevant_tweet(self, tweet_json):
        return gluttonyTest(
            tweet_json['full_text'] if 'full_text' in tweet_json else tweet_json['text'],
            self._gluttony_words
        )

    def _save_relevant_tweet(self, tweet_json):
        with self._db.relevant_db as db:
            json = _relevant_tweet_to_doc(tweet_json)
            doc = db.create_document(json)
            if doc.exists():
                self._logger.debug('successfully saved relevant tweet {} to db'.format(json['_id']))
            else:
                self._logger.warning('failed to save relevant tweet {} to db'.format(json['_id']))

    def _tweet_has_valid_location(self, tweet):
        return (tweet.coordinates is not None or
                (tweet.place is not None and tweet.place.place_type == 'poi')) and \
            self._bbox.contains(tweet.coordinates or tweet.place.bounding_box.origin())

    def _queue_user(self, user, priority=0):
        if user.id not in self._user_history:
            self._logger.debug('queued new user {}'.format(user.id))
            self._user_history.add(user.id)
            self._queue.put((priority, -user.id))

    def _process_user(self, user_id):
        with self._db.user_db as db:
            if str(user_id) in db:
                self._logger.debug('skipping previously processed user {}'.format(user_id))
                if bool(randint(0, 3)):
                    return
            else:
                db.create_document({
                    '_id': str(user_id),
                    'user': user_id,
                    'added_at': int(time.time())
                })
                if not self._download_user_tweets(user_id):
                    return

        # the underlying assumption behind using followers is that the average user will be more
        # likely to be followed by people they know, which suggests probable spatial proximity
        # using following instead is likely to expand the search space outside the locality of the
        # original users, as it will move towards certain highly followed accounts
        self._logger.debug('queuing followers for user {}'.format(user_id))
        # limit ourselves to 200 followers, because otherwise users with large numbers of followers
        # will make us hit rate limits
        for follower in tweepy.Cursor(self.api.followers, user_id=user_id, count=200).items(400):
            # queue followers with a low priority, since we don't know if any of them will have
            # tweets with locations
            self._queue_user(follower, priority=1)

    def _download_user_tweets(self, user_id):
        self._logger.debug('downloading tweets for user {}'.format(user_id))
        found_valid_tweet = False
        for page in tweepy.Cursor(self.api.user_timeline,
                                  user_id=user_id,
                                  count=200, 
                                  tweet_mode='extended').pages():
            for tweet in page:
                found_valid_tweet = self._process_tweet(tweet) or found_valid_tweet
            if not found_valid_tweet:
                # give up after a page--if there are no useful tweets in the first 200, just try
                # the next user
                self._logger.info('no tweets with locations found for user {}; moving on'
                    .format(user_id))
                break
        return found_valid_tweet

    def on_status(self, tweet):
        self._logger.debug('received tweet {} from stream'.format(tweet.id))
        # prioritise users from the data stream, as they will be about a more broad topic than
        # the seeded users (due to the search term) and are probably more likely than a follower to
        # have more tweets with locations
        if self._process_tweet(tweet, queue_priority=-1):
            self._logger.info('saved a tweet from user {} via stream'.format(tweet.author.id))

    def on_error(self, status_code):
        if status_code == 420:
            # I'm not totally sure if this is necessary or we can just trust the exponential backoff
            # from Tweepy to avoid reconnecting too often
            # http://docs.tweepy.org/en/3.7.0/streaming_how_to.html#handling-errors
            self._logger.error('stream received status code 420; disconnecting')
            return False
        return True

    def on_exception(self, ex):
        self._logger.exception(ex)

    def _start_streaming(self):
        self._logger.info('opening tweet stream in background')
        self._stream = tweepy.Stream(self.api.auth, self, tweet_mode='extended')
        self._stream.filter(locations=self._bbox.as_locations(), is_async=True)

    def _drain_download_queue(self):
        while True:
            try:
                _, user = self._queue.get(block=True, timeout=None)
                user = -user
                prev_written = self._valid_tweet_count
                self._process_user(user)
                self._logger.info('saved {} tweets from user {}'
                    .format(self._valid_tweet_count - prev_written, user))
            except Exception as ex:
                self._logger.exception(ex)

    def download_tweets(self):
        # start the stream first so that if seeding gets rate limited, we still can find some tweets
        self._start_streaming()
        self._seed()
        self._drain_download_queue()

    def disconnect(self):
        if self._stream is not None:
            self._stream.disconnect()
            self._stream = None


# this is necessary because the relevant tweets database uses a slightly different format
def _relevant_tweet_to_doc(tweet):
    return {
        '_id': tweet['_id'],
        'id': tweet['id'],
        'coordinates': tweet['coordinates'],
        'full_text': tweet['full_text'] if 'full_text' in tweet else tweet['text'],
        'user': {
            'id': tweet['user']['id'],
            'screen_name': tweet['user']['screen_name']
        },
        'created_at': tweet['created_at'],
        'hashtags': tweet['entities']['hashtags']
    }
