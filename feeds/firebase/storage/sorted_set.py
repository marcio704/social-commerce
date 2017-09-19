import six
import logging

from stream_framework.utils.functional import lazy
from stream_framework.utils import chunks

from feeds.firebase.storage.structures.hash import BaseFirebaseHashCache
from feeds.firebase.storage.structures.list import BaseFirebaseListCache


logger = logging.getLogger(__name__)


class FirebaseSortedSetCache(BaseFirebaseListCache, BaseFirebaseHashCache):
    sort_asc = False

    def count(self):
        """
        Returns the number of elements in the sorted set
        """
        key = self.get_key()
        firebase_result = len(self.firebase.child(key).shallow().get().pyres)
        firebase_count = lambda: int(firebase_result)
        lazy_factory = lazy(firebase_count, *six.integer_types)
        lazy_object = lazy_factory()
        return lazy_object

    def index_of(self, value):
        """
        Returns the index of the given value
        """
        # TODO: select it ordered from Firebase
        # if self.sort_asc:
        #     redis_rank_fn = self.redis.zrank
        # else:
        #     redis_rank_fn = self.redis.zrevrank
        key = self.get_key()
        result = self.firebase.child(key).get()
        if result:
            result = list(result.keys()).index(value)
        else:
            raise ValueError('Couldnt find item with value %s in key %s' % (value, key))

        return result

    def add(self, score, key):
        score_value_pairs = [(score, key)]
        results = self.add_many(score_value_pairs)
        result = results[0]
        return result

    def add_many(self, score_value_pairs):
        """
        It expects score1, name1
        """
        value_score_pairs = [tuple(reversed(i)) for i in score_value_pairs]

        key = self.get_key()
        scores = list(zip(*score_value_pairs))[0]
        msg_format = 'Please send floats as the first part of the pairs got %s'
        numeric_types = (float,) + six.integer_types
        if not all([isinstance(score, numeric_types) for score in scores]):
            raise ValueError(msg_format % score_value_pairs)
        results = []

        value_score_list = sum(map(list, value_score_pairs), [])
        value_score_chunks = chunks(value_score_list, 200)

        for value, score in value_score_chunks:
            self.firebase.child(key).child(str(value)).set({"score": str(score)})
            logger.debug('adding to %s with value %s and score %s',
                         key, value, score)
            results.append(score)
        return results

    def remove_many(self, values):
        """
        values
        """
        key = self.get_key()
        results = []

        for value in values:
            logger.debug('removing value %s from %s', value, key)
            result = len(self.firebase.child(key).child(value).shallow().get().pyres)
            self.firebase.child(key).child(value).remove()
            results.append(result)
        return results

    def remove_by_scores(self, scores):
        key = self.get_key()
        nodes = self.firebase.child(key)
        if not nodes:
            return []

        results = []
        for score in scores:
            count = 0
            for _value, _score in nodes:
                if _score == score:
                    self.firebase.child(key).child(_value).remove()
                    count += 1

            logger.debug('removing score %s from %s', score, key)
            results.append(count)

        return results

    def contains(self, value):
        """
        Uses zscore to see if the given activity is present in our sorted set
        """
        key = self.get_key()
        result = self.firebase.child(key).child(value).get().pyres
        activity_found = bool(result)
        return activity_found

    # TODO: function not rewrited
    def trim(self, max_length=None):
        """
        Trim the sorted set to max length
        zremrangebyscore
        """
        key = self.get_key()
        pass
    #     if max_length is None:
    #         max_length = self.max_length
    #
    #     # map things to the funny redis syntax
    #     if self.sort_asc:
    #         begin = max_length
    #         end = -1
    #     else:
    #         begin = 0
    #         end = (max_length * -1) - 1
    #
    #     removed = self.redis.zremrangebyrank(key, begin, end)
    #     logger.info('cleaning up the sorted set %s to a max of %s items' %
    #                 (key, max_length))
    #     return removed

    def get_results(self, start=None, stop=None, min_score=None, max_score=None):
        """
        Retrieve results from redis using zrevrange
        O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements returned.
        """
        # if self.sort_asc:
        #     redis_range_fn = self.redis.zrangebyscore
        # else:
        #     redis_range_fn = self.redis.zrevrangebyscore

        # -1 means infinity
        if stop is None:
            stop = -1

        if start is None:
            start = 0

        if stop != -1:
            limit = stop - start
        else:
            limit = -1

        key = self.get_key()
        results = self.firebase.child(key).get().val()

        # TODO: Try to rewrite something like redis
        # some type validations
        # if min_score and not isinstance(min_score, (float, str, six.integer_types)):
        #     raise ValueError(
        #         'min_score is not of type float, int, long or str got %s' % min_score)
        # if max_score and not isinstance(max_score, (float, str, six.integer_types)):
        #     raise ValueError(
        #         'max_score is not of type float, int, long or str got %s' % max_score)
        #
        # if min_score is None:
        #     min_score = '-inf'
        # if max_score is None:
        #     max_score = '+inf'
        #
        # # handle the starting score support
        # results = redis_range_fn(
        #     key, start=start, num=limit, withscores=True, min=min_score, max=max_score)
        return results
