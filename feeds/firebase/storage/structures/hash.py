import logging

from feeds.firebase.storage.cache import FirebaseCache

logger = logging.getLogger(__name__)


class BaseFirebaseHashCache(FirebaseCache):
    key_format = 'firebase:base_hash_cache:%s'


class FirebaseHashCache(BaseFirebaseHashCache):
    key_format = 'firebase:hash_cache:%s'

    def get_key(self, *args, **kwargs):
        return self.key

    def count(self):
        """
        Returns the number of elements in the sorted set
        """
        key = self.get_key()
        firebase_result = self.firebase.child(key).shallow().get().pyres
        firebase_count = len(firebase_result)
        return firebase_count

    def contains(self, field):
        """
        Used to see if the given field is present
        """
        key = self.get_key()
        results = self.firebase.child(key).shallow().get().pyres
        return field in results

    def get(self, field):
        fields = [field]
        results = self.get_many(fields)
        result = results[field]
        return result

    def keys(self):
        key = self.get_key()
        keys = self.firebase.child(key).shallow().get().pyres
        return keys

    def delete_many(self, fields):
        results = {}

        for field in fields:
            key = self.get_key(field)
            logger.debug('removing field %s from %s', field, key)
            result = len(self.firebase.child(key).child(field).shallow().get().pyres)
            self.firebase.child(key).child(field).remove()
            results[field] = result

        return results

    def get_many(self, fields):
        key = self.get_key()
        results = {}
        values = self.firebase.child(key).get()

        for value in values.each():
            for field in fields:
                logger.debug('getting field %s from %s', field, key)
                if field == value.key():
                    results[field] = value.val()

        return results

    def set(self, key, value):
        key_value_pairs = [(key, value)]
        results = self.set_many(key_value_pairs)
        result = results[0]
        return result

    def set_many(self, key_value_pairs):
        results = []

        for field, value in key_value_pairs:
            key = self.get_key(field)
            logger.debug('writing hash(%s) field %s to %s', key, field, value)
            result = self.firebase.child(key).set({field: value})
            results.append(result)
        return results
