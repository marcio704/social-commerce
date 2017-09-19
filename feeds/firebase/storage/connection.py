from feeds.utils import FirebaseConnection

connection_pool = None


def get_firebase_connection(server_name='default'):
    """
    Gets the specified Firebase connection
    """
    # global connection_pool
    #
    # if connection_pool is None:
    #     connection_pool = setup_firebase()
    #
    # pool = connection_pool[server_name]

    return FirebaseConnection().db


# def setup_firebase():
#     '''
#     Starts the connection pool for all configured redis servers
#     '''
#     pools = {}
#     for name, config in settings.STREAM_REDIS_CONFIG.items():
#         pool = redis.ConnectionPool(
#             host=config['host'],
#             port=config['port'],
#             password=config.get('password'),
#             db=config['db'],
#             decode_responses=True
#         )
#         pools[name] = pool
#     return pools
