import datetime
import json
import jwt
from flask import current_app
from redis import Redis


class RedisClient(object):

    db_client = Redis()
    auth_client = Redis()

    def init_app(self, app, redis_password):
        self.db_client = Redis(
            host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=0, password=redis_password, socket_timeout=None, charset='utf-8', decode_responses=True)
        self.auth_client = Redis(
            host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=1, password=redis_password, socket_timeout=None, charset='utf-8', decode_responses=True)

    # LOCATOR POINTS FUNCTIONS
    def add_points(self, locator_points):
        for point in locator_points:
            self.db_client.hset(f'points:{point.point_id}', 'title', point.title)
            self.db_client.hset(f'points:{point.point_id}', 'description', point.description)
            self.db_client.hset(f'points:{point.point_id}', 'point_type', point.point_type)
            self.db_client.hset(f'points:{point.point_id}', 'lat', point.lat)
            self.db_client.hset(f'points:{point.point_id}', 'lon', point.lon)
            self.db_client.hset(f'points:{point.point_id}', 'created_at', point.created_at)
            self.db_client.hset(f'points:{point.point_id}', 'unit_id', point.unit_id)

    def del_points():
        # TODO
        pass

    # LOCATOR POINT FUNCTIONS
    def get_point():
        # TODO
        pass

    def add_point():
        # TODO
        pass

    def del_point():
        # TODO
        pass

    # UNITS FUNCTIONS
    def add_units(self, units):
        for unit in units:
            self.db_client.hset(f'units:{unit.unit_id}', 'name', unit.name)
            self.db_client.hset(f'units:{unit.unit_id}', 'alert_mail', int(unit.alert_mail))
            self.db_client.hset(f'units:{unit.unit_id}', 'alert_sms', int(unit.alert_sms))
            self.db_client.hset(f'units:{unit.unit_id}', 'user_id', unit.user_id)
            self.db_client.hset(f'units:{unit.unit_id}', 'locator_points', json.dumps([point.point_id for point in unit.locator_points]))

    # UNIT FUNCTIONS
    def get_unit(self, unit_id):
        unit = self.db_client.hgetall(f'units:{unit_id}')

        if bool(unit):
            unit['alert_mail'] = bool(int(unit['alert_mail']))
            unit['alert_sms'] = bool(int(unit['alert_sms']))
            unit['unit_id'] = unit_id
            del unit["locator_points"]

        return unit

    def add_unit(self, unit):
        self.db_client.hset(f'units:{unit.unit_id}', 'name', unit.name)
        self.db_client.hset(f'units:{unit.unit_id}', 'alert_mail', int(unit.alert_mail))
        self.db_client.hset(f'units:{unit.unit_id}', 'alert_sms', int(unit.alert_sms))
        self.db_client.hset(f'units:{unit.unit_id}', 'user_id', unit.user_id)
        self.db_client.hset(f'units:{unit.unit_id}', 'locator_points', json.dumps([point.point_id for point in unit.locator_points]))

    def del_unit(self, unit_id):
        self.db_client.delete(f'units:{unit_id}')

    # USER FUNCTIONS
    def get_user(self, user_id):
        return self.db_client.hgetall(f'users:{user_id}')

    def add_user(self, user):
        self.db_client.hset(f'users:{user.user_id}', 'username', user.username)
        self.db_client.hset(f'users:{user.user_id}', 'phone_number', user.phone_number)
        self.db_client.hset(f'users:{user.user_id}', 'email', user.email)
        self.db_client.hset(f'users:{user.user_id}', 'is_admin', int(user.is_admin))
        self.db_client.hset(f'users:{user.user_id}', 'is_super', int(user.is_super))
        self.db_client.hset(f'users:{user.user_id}', 'units', json.dumps([unit.unit_id for unit in user.units]))

    def del_user(self, user_id):
        self.db_client.delete(f'users:{user_id}')

    def blacklist_tocken(self, tocken):
        expiration_param = jwt.get_unverified_header(tocken)['exp'] - datetime.datetime.utcnow()
        self.auth_client.set(f'tockens:{tocken}', 1)
        self.auth_client.expire(f'tockens:{tocken}', expiration_param)
        print(f'tocken {tocken} has been blacklisted')
