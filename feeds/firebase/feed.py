import logging

from stream_framework.feeds.base import BaseFeed
from stream_framework.feeds.aggregated_feed.base import AggregatedFeed
from stream_framework.serializers.aggregated_activity_serializer import AggregatedActivitySerializer
from stream_framework.serializers.activity_serializer import ActivitySerializer

from feeds.firebase.storage.activity import FirebaseActivityStorage
from feeds.firebase.storage.timeline import FirebaseTimelineStorage

logger = logging.getLogger(__name__)


class FirebaseFeed(BaseFeed):
    activity_storage_class = FirebaseActivityStorage
    timeline_storage_class = FirebaseTimelineStorage

    activity_serializer = ActivitySerializer

    # : allow you point to a different firebase server as specified in
    # : settings.STREAM_REDIS_CONFIG
    firebase_server = 'default'

    @classmethod
    def get_timeline_storage_options(cls):
        """
        Returns the options for the timeline storage
        """
        options = super(FirebaseFeed, cls).get_timeline_storage_options()
        options['firebase_server'] = cls.firebase_server
        return options

    # : clarify that this feed supports filtering and ordering
    filtering_supported = True
    ordering_supported = True


class FirebaseAggregatedFeed(AggregatedFeed):
    timeline_serializer = AggregatedActivitySerializer
    activity_serializer = ActivitySerializer
    timeline_storage_class = FirebaseTimelineStorage
    activity_storage_class = FirebaseActivityStorage

    # TODO: continue from here
    def _update_from_diff(self, new, changed, deleted):
        """
        Sends the add and remove commands to the storage layer based on a diff
        of

        :param new: list of new items
        :param changed: list of tuples (from, to)
        :param deleted: list of things to delete
        """
        msg_format = 'now updating from diff new: %s changed: %s deleted: %s'
        logger.debug(msg_format, *map(len, [new, changed, deleted]))
        to_remove, to_add = self._translate_diff(new, changed, deleted)

        # remove those which changed
        with self.get_timeline_batch_interface() as batch_interface:
            if to_remove:
                self.remove_many_aggregated(
                    to_remove, batch_interface=batch_interface)

        # now add the new ones
        with self.get_timeline_batch_interface() as batch_interface:
            if to_add:
                self.add_many_aggregated(
                    to_add, batch_interface=batch_interface)

        logger.debug(
            'removed %s, added %s items from feed %s', len(to_remove), len(to_add), self)

        # return the merge of these two
        new_aggregated = new[:]
        if changed:
            new_aggregated += list(zip(*changed))[1]

        self.on_update_feed(to_add, to_remove)
        return new_aggregated
