from typing import NamedTuple
from environs import Env


class Cfg(NamedTuple):
    __env = Env()
    __env.read_env()

    BOT_TOKEN = __env.str('BOT_TOKEN')
    WH_HOST = __env.str('WH_HOST')
    BOT_PATH = f"/wh/{BOT_TOKEN}"
    APP_PORT = __env.int('APP_PORT')
    APP_DEBUG = __env.bool('APP_DEBUG')
    LOG_LEVEL = __env.str('LOG_LEVEL')
    REDIS_DSN = __env.str('REDIS_DSN')
    ADMINS = __env.list('ADMIN_ID')
    MONGODB_DATABASE = __env.str('MONGODB_DATABASE')
    MONGODB_USERNAME = __env.str('MONGODB_USERNAME')
    MONGODB_PASSWORD = __env.str('MONGODB_PASSWORD')
    MONGODB_HOSTNAME = __env.str('MONGODB_HOSTNAME')
    MONGODB_PORT = __env.str('MONGODB_PORT')
    MONGODB_URI = 'mongodb://'
    if MONGODB_USERNAME and MONGODB_PASSWORD:
        MONGODB_URI += f"{MONGODB_USERNAME}:{MONGODB_PASSWORD}@"
    MONGODB_URI += f"{MONGODB_HOSTNAME}:{MONGODB_PORT}"
