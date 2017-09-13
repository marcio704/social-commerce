from django.conf import settings
from django.db import models

from models.models import Brand, Store


class BaseModel(models.Model):

    class Meta:
        abstract = True


class UserFollowUser(BaseModel):
    """
    A simple table mapping who a user is following.
    For example, if user is Kyle and Kyle is following Alex,
    the target would be Alex.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_set')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} --> {1}".format(self.user.first_name, self.target.first_name)

    class Meta:
        unique_together = (("user", "target"), )


class UserFollowStore(BaseModel):
    """
    A simple table mapping what store a user is following.
    For example, if user is Kyle and Kyle is following the store BelezaNaWeb,
    the target would be BelezaNaWeb.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False)
    target = models.ForeignKey(Store, null=False, blank=False, related_name='store_followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} --> {1}".format(self.user.first_name, self.target.name)

    class Meta:
        unique_together = (("user", "target"), )


class UserFollowBrand(BaseModel):
    """
    A simple table mapping what store a user is following.
    For example, if user is Kyle and Kyle is following the brand Nike,
    the target would be Nike.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False)
    target = models.ForeignKey(Brand, null=False, blank=False, related_name='brand_followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} --> {1}".format(self.user.first_name, self.target.name)

    class Meta:
        unique_together = (("user", "target"), )
