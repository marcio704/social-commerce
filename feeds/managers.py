from django.conf import settings

from feeds.base import Manager, FanoutPriority
from feeds.feeds import NormalUserFeed, UserFeed, AggregatedUserFeed,\
    FirebaseNormalUserFeed, FirebaseUserFeed, FirebaseAggregatedUserFeed
from feeds.activities import get_activity
from feeds.models import UserFollowUser
from feeds.verbs import UserFollowUser as UserFollowUserVerb, UserFollowBrand,\
    UserFollowStore, UserAddPost, UserAddProduct
from feeds.firebase.managers import FirebaseManager


# TODO: Put this as an environment variable on django settings when development is finished
is_firebase = True


class UserManager(FirebaseManager):
    feed_classes = dict(
        normal=FirebaseNormalUserFeed if is_firebase else NormalUserFeed,
        aggregated=FirebaseAggregatedUserFeed if is_firebase else AggregatedUserFeed,
    )
    user_feed_class = FirebaseUserFeed if is_firebase else UserFeed

    def get_user_follower_ids(self, user_id):
        """
        Gets users ids from all current user followers
        :param user_id:
        :return:
        """
        ids = UserFollowUser.objects.filter(target=user_id).values_list('user_id', flat=True)
        return {FanoutPriority.HIGH: ids}

    def follow_user_fanout(self, user_id, target_user_id):
        """
        Get 'following user' activity and set it to the feeds through manager
        :param user_id:
        :param target_user_id:
        :return:
        """
        activity = get_activity(user_id, target_user_id, UserFollowUserVerb)

        # Add user activity to the user feed, and starts the fanout
        self.add_user_activity(user_id, activity)

    def follow_brand_fanout(self, user_id, target_brand_id):
        """
        Get 'following brand' activity and set it to the feeds through manager
        :param user_id:
        :param target_brand_id:
        :return:
        """
        activity = get_activity(user_id, target_brand_id, UserFollowBrand)

        # Add user activity to the user feed, and starts the fanout
        self.add_user_activity(user_id, activity)

    def follow_store_fanout(self, user_id, target_store_id):
        """
        Get 'following store' activity and set it to the feeds through manager
        :param user_id:
        :param target_store_id:
        :return:
        """
        activity = get_activity(user_id, target_store_id, UserFollowStore)

        # Add user activity to the user feed, and starts the fanout
        self.add_user_activity(user_id, activity)

    def add_post_fanout(self, user_id, target_post_id):
        """
        Get 'adding post' activity and set it to the feeds through manager
        :param user_id:
        :param target_post_id:
        :return:
        """
        activity = get_activity(user_id, target_post_id, UserAddPost)

        # Add user activity to the user feed, and starts the fanout
        self.add_user_activity(user_id, activity)

    def add_product_fanout(self, user_id, target_product_id):
        """
        Get 'adding product' activity and set it to the feeds through manager
        :param user_id:
        :param target_product_id:
        :return:
        """
        activity = get_activity(user_id, target_product_id, UserAddProduct)

        # Add user activity to the user feed, and starts the fanout
        self.add_user_activity(user_id, activity)

    # def remove_followers(self, user_id):
    #     activity = get_activity(user_id, None, Inactivate)
    #
    #     # removes the user's activities from the followers feeds
    #     self.remove_user_activity(user_id, activity)


user_manager = UserManager()
