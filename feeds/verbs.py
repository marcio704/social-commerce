from stream_framework.verbs import register
from stream_framework.verbs.base import Verb


class UserFollowUser(Verb):
    id = 5
    infinitive = 'user-follow-user'
    past_tense = 'user-followed-user'


register(UserFollowUser)


class UserFollowBrand(Verb):
    id = 6
    infinitive = 'user-follow-brand'
    past_tense = 'user-followed-brand'


register(UserFollowBrand)


class UserFollowStore(Verb):
    id = 7
    infinitive = 'user-follow-store'
    past_tense = 'user-followed-store'


register(UserFollowStore)


class UserAddPost(Verb):
    id = 8
    infinitive = 'user-add-post'
    past_tense = 'user-added-post'


register(UserAddPost)


class UserAddProduct(Verb):
    id = 9
    infinitive = 'user-add-product'
    past_tense = 'user-added-product'

register(UserAddProduct)
