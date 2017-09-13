from feeds.utils import FirebaseConnection


class FirebaseCache(object):

    '''
    The base for all firebase data structures
    '''
    key_format = 'firebase:cache:%s'

    def __init__(self, key, firebase=None, firebase_server='default'):
        # write the key
        self.key = key
        # handy when using fallback to other data sources
        self.source = 'firebase'
        # the redis connection, self.redis is lazy loading the connection
        self._firebase = firebase
        # the redis server (see get_redis_connection)
        self.firebase_server = firebase_server

    def get_firebase(self):
        '''
        Only load the firebase connection if we use it
        '''
        if self._firebase is None:
            self._firebase = FirebaseConnection().db
        return self._firebase

    def set_firebase(self, value):
        '''
        Sets the firebase connection
        '''
        self._firebase = value

    firebase = property(get_firebase, set_firebase)

    def get_key(self):
        return self.key

    def delete(self):
        key = self.get_key()
        self.firebase.db.child.remove(key)
