from django.contrib import admin

from .models import UserFollowUser, UserFollowStore, UserFollowBrand

admin.site.register((UserFollowUser, UserFollowStore, UserFollowBrand))
