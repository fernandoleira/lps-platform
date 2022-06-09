from redis import Redis

class RedisClient(object):

    redis_client = Redis()
    
    def init_app(self, app):
        redis_client = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=0, password=None, socket_timeout=None)
    
    def add_locator_points(self, locator_points):
        pass