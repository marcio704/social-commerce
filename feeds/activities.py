import datetime

from stream_framework.activity import Activity


def get_activity(follower_user_id, followed_object_id, action):
    """
    Gets Stream framework Activity to be published on one or more feeds
    :param follower_user_id:
    :param followed_object_id:
    :param action:
    :return:
    """
    activity = Activity(
        follower_user_id,
        action,
        followed_object_id,
        followed_object_id,
        time=datetime.datetime.now(),
        # extra_context=dict(item_id=pin.item_id)
    )
    return activity
