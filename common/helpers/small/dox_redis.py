from redis import Redis

from django.conf import settings


def _connection():
    redis_conf = settings.REDIS.get('default')
    connection = {'host': redis_conf['HOST'], 'port': redis_conf['PORT'], 'db': redis_conf['INDEX_DB']}
    return connection


redis = Redis(**_connection())
