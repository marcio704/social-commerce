
import pyrebase
from django.conf import settings


class FirebaseConnection(object):
    db = None

    def __init__(self):
        """
        Sets firebase connection
        """
        firebase = pyrebase.initialize_app(settings.FB_CONFIG)
        db = firebase.database()
        self.db = db
