import logging

from feeds.base import Manager


logger = logging.getLogger(__name__)


class FirebaseManager(Manager):

    def fanout(self, user_ids, feed_class, operation, operation_kwargs):
        """
        This functionality is called from within stream_framework.tasks.fanout_operation

        :param user_ids: the list of user ids which feeds we should apply the
            operation against
        :param feed_class: the feed to run the operation on
        :param operation: the operation to run on the feed
        :param operation_kwargs: kwargs to pass to the operation

        """
        # with self.metrics.fanout_timer(feed_class):
        separator = '===' * 10
        logger.info('%s starting fanout %s', separator, separator)
        # batch_context_manager = feed_class.get_timeline_batch_interface()
        msg_format = 'starting batch interface for feed %s, fanning out to %s users'
        logger.info(msg_format, feed_class, len(user_ids))
        # operation_kwargs['batch_interface'] = batch_interface

        for user_id in user_ids:
            logger.debug('now handling fanout to user %s', user_id)
            feed = feed_class(user_id)
            operation(feed, **operation_kwargs)
        logger.info('finished fanout for feed %s', feed_class)

        # fanout_count = len(operation_kwargs['activities']) * len(user_ids)
        # self.metrics.on_fanout(feed_class, operation, fanout_count)
