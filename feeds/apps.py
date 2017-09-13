# encoding: utf-8

from django.apps import AppConfig


class FeedsConfig(AppConfig):
    name = 'feeds'

    def ready(self):
        import feeds.signals # noga
