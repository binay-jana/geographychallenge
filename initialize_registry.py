import redis
import registry
from constants import local_settings
from libraries.my_sql_connection import MySQLConnection
from libraries.repositories.questions import Questions


def load_registry():
    """ Initialize and load the global registry
    """
    r = registry.get_registry()
    if r.is_locked():
        return
    init_mysql(r)
    # init_sentry(r)
    init_redis(r)
    init_db_objects(r)
    r.lock()


def init_mysql(r):
    r['MY_SQL'] = MySQLConnection()


def init_redis(r):
    r['REDIS'] = redis.StrictRedis(
        host=local_settings.redis_host,
        port=local_settings.redis_port,
        db=local_settings.redis_db
    )


def init_db_objects(r):
    r['QUESTIONS'] = Questions
