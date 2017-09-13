
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

from feeds.managers import user_manager
from feeds.utils import FirebaseConnection


# Create your views here.
def show_feed(request, user_id):
    """
    Show current user's feed
    :param request:
    :param user_id:
    :return:
    """
    feed = user_manager.get_feeds(user_id)['normal']
    activities = list(feed[:25])

    # Google Firebase connection test
    fb = FirebaseConnection()
    fb.db.child('test').set({"Hello": "World", "Hello2": "WOrld"})

    results = {}
    values = fb.db.child('test').get()
    fields = ["Hello2", "a"]
    for value in values.each():
        for field in fields:
            if field == value.key():
                results[field] = value.val()

    return HttpResponse("Activities: {0}".format(activities))
