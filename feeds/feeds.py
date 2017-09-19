from stream_framework.aggregators.base import RecentVerbAggregator
from stream_framework.feeds.redis import RedisFeed
from stream_framework.feeds.aggregated_feed.redis import RedisAggregatedFeed

from feeds.firebase.feed import FirebaseFeed, FirebaseAggregatedFeed


# Redis feeds
class NormalUserFeed(RedisFeed):
    key_format = 'feed:normal:%(user_id)s'


class AggregatedUserFeed(RedisAggregatedFeed):
    aggregator_class = RecentVerbAggregator
    key_format = 'feed:aggregated:%(user_id)s'


class UserFeed(NormalUserFeed):
    key_format = 'feed:user:%(user_id)s'


# Firebase feeds
class FirebaseNormalUserFeed(FirebaseFeed):
    key_format = 'feed:normal:%(user_id)s'


class FirebaseAggregatedUserFeed(FirebaseAggregatedFeed):
    aggregator_class = RecentVerbAggregator
    key_format = 'feed:aggregated:%(user_id)s'


class FirebaseUserFeed(FirebaseNormalUserFeed):
    key_format = 'feed:user:%(user_id)s'
