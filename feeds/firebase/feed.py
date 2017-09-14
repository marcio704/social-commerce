from stream_framework.feeds.base import BaseFeed
from stream_framework.serializers.activity_serializer import ActivitySerializer

from feeds.firebase.storage.activity import FirebaseActivityStorage
from feeds.firebase.storage.timeline import FirebaseTimelineStorage


class FirebaseFeed(BaseFeed):
    activity_storage_class = FirebaseActivityStorage
    timeline_storage_class = FirebaseTimelineStorage

    activity_serializer = ActivitySerializer

    # : allow you point to a different firebase server as specified in
    # : settings.STREAM_REDIS_CONFIG
    firebase_server = 'default'

    @classmethod
    def get_timeline_storage_options(cls):
        '''
        Returns the options for the timeline storage
        '''
        options = super(FirebaseFeed, cls).get_timeline_storage_options()
        options['firebase_server'] = cls.firebase_server
        return options

    # : clarify that this feed supports filtering and ordering
    filtering_supported = True
    ordering_supported = True
