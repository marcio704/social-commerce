from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from feeds.managers import user_manager
from feeds.models import UserFollowUser, UserFollowBrand, UserFollowStore
from models.models import Post, Clooset


@receiver(post_save, sender=UserFollowUser)
def update_feed_on_follow_user(sender, instance, created, **kwargs):
    """
    Updates current user's feed and all followers' feed after following someone
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if not created:
        return

    try:
        user_manager.follow_user_fanout(instance.user.id, instance.target.id)
    except Exception as e:
        print("Exception on saving changes to feed."
              "Activity: follow_user."
              "Follower: {0}."
              "Followed: {1}"
              "Message: {2}".format(instance.user.id, instance.target.id, e))


@receiver(post_save, sender=UserFollowBrand)
def update_feed_on_follow_brand(sender, instance, created, **kwargs):
    """
    Updates current user's feed and all followers' feed after following some brand
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if not created:
        return

    try:
        user_manager.follow_brand_fanout(instance.user.id, instance.target.id)
    except Exception as e:
        print("Exception on saving changes to feed."
              "Activity: follow_brand."
              "Follower: {0}."
              "Followed: {1}"
              "Message: {2}".format(instance.user.id, instance.target.id, e))


@receiver(post_save, sender=UserFollowStore)
def update_feed_on_follow_store(sender, instance, created, **kwargs):
    """
    Updates current user's feed and all followers' feed after following some store
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if not created:
        return

    try:
        user_manager.follow_store_fanout(instance.user.id, instance.target.id)
    except Exception as e:
        print("Exception on saving changes to feed."
              "Activity: follow_store."
              "Follower: {0}."
              "Followed: {1}"
              "Message: {2}".format(instance.user.id, instance.target.id, e))


@receiver(post_save, sender=Post)
def update_feed_on_add_post(sender, instance, created, **kwargs):
    """
    Updates current user's feed and all followers' feed after adding a new post
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if not created:
        return

    try:
        user_manager.add_post_fanout(instance.author.id, instance.id)
    except Exception as e:
        print("Exception on saving changes to feed."
              "Activity: add_post."
              "Author: {0}."
              "Post: {1}"
              "Message: {2}".format(instance.author.id, instance.id, e))


@receiver(post_save, sender=Clooset)
def update_feed_on_add_product(sender, instance, created, **kwargs):
    """
    Updates current user's feed and all followers' feed after adding a product to his/her clooset
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if not created:
        return

    try:
        user_manager.add_product_fanout(instance.user.id, instance.product.id)
    except Exception as e:
        print("Exception on saving changes to feed."
              "Activity: follow_store."
              "User: {0}."
              "Product: {1}"
              "Message: {2}".format(instance.user.id, instance.product.id, e))
