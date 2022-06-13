import uuid
from random import choice
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, Integer, FLOAT, String, TEXT, VARCHAR, BOOLEAN, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from api import db


# User class
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = Column('user_id', UUID(as_uuid=True), primary_key=True)
    username = Column('username', VARCHAR(50), nullable=False, unique=True)
    phone_number = Column('phone_number', VARCHAR(11))
    email = Column('email', VARCHAR(50), nullable=False, unique=True)
    pswd_hash = Column('pswd_hash', String, nullable=False)
    is_admin = Column('is_admin', BOOLEAN)
    is_super = Column('is_super', BOOLEAN)
    units = relationship('Unit', back_populates='user')
    api_keys = relationship('ApiKey', back_populates='user')

    def __init__(self, username, email, phone_number, password, is_admin=False, is_super=False, user_id=None):
        self.user_id = user_id if user_id != None else uuid.uuid4()
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.pswd_hash = generate_password_hash(password, method='sha256')
        self.is_admin = is_admin
        self.is_super = is_super

    def __repr__(self):
        return '<user_id {}>'.format(self.user_id)

    def get_id(self):
        return self.email

    def check_password_hash(self, password):
        return check_password_hash(self.pswd_hash, password)


# Api Key class
class ApiKey(db.Model):
    __tablename__ = 'api_keys'

    api_key = Column('api_key', VARCHAR(20), primary_key=True)
    created_at = Column('created_at', TIMESTAMP(0), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(0), nullable=False)
    expired_at = Column('expired_at', TIMESTAMP(0), nullable=False)
    user = relationship('User', back_populates='api_keys')
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)

    def __init__(self, user_id, api_key=None, created_at=None, updated_at=None):
        self.user_id = user_id 
        if api_key != None:
            self.api_key = api_key
        else:
            self.api_key = self._api_key_generator()
        if created_at != None:
            self.created_at = created_at
        else:
            self.created_at = datetime.now()
        if updated_at != None:
            self.updated_at = updated_at
        else:
            self.updated_at = self.created_at

        self.expired_at = self._get_expiration_timestamp(self.updated_at.timestamp())

    def __repr__(self):
        return '<api_key {}>'.format(self.api_key)

    def _api_key_generator(self):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        new_key = str()

        for i in range(20):
            if i == 4 or i == 9 or i == 14:
                new_key += '-'
            else:
                new_key += choice(chars) 

        return new_key

    def _get_current_timestamp(self):
        return datetime.now().timestamp()

    def _get_expiration_timestamp(self, ts):
        expired_date = datetime.fromtimestamp(ts) + relativedelta(months=+3)
        return expired_date

    def update_api_expiration(self):
        self.updated_at = datetime.now().timestamp()
        self._get_expiration_timestamp(self.updated_at)


# Unit class
class Unit(db.Model):
    __tablename__ = 'units'

    unit_id = Column('unit_id', UUID(as_uuid=True), primary_key=True)
    name = Column('name', VARCHAR(50), nullable=False, unique=True)
    alert_mail = Column('alert_mail', BOOLEAN)
    alert_sms = Column('alert_sms', BOOLEAN)
    user = relationship('User', back_populates='units')
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    locator_points = relationship("LocatorPoint", back_populates="unit")

    def __init__(self, name, user_id, alert_mail, alert_sms, unit_id=None):
        self.unit_id = unit_id if unit_id != None else uuid.uuid4()
        self.name = name
        self.alert_mail = alert_mail
        self.alert_sms = alert_sms
        self.user_id = user_id

    def __repr__(self):
        return '<unit {unit_id}>'.format(unit_id=self.unit_id)


# Locator Point class
class LocatorPoint(db.Model):
    __tablename__ = 'locator_points'

    point_id = Column('point_id', UUID(as_uuid=True), primary_key=True)
    title = Column('title', VARCHAR(50), nullable=False)
    description = Column('description', TEXT)
    point_type = Column('point_type', VARCHAR(50), nullable=False) # Alert, Warning, Info or Ping
    lat = Column('lat', FLOAT, nullable=False)
    lon = Column('lon', FLOAT, nullable=False)
    created_at = Column('created_at', TIMESTAMP(0))
    unit = relationship('Unit', back_populates='locator_points')
    unit_id = Column('unit_id', UUID(as_uuid=True), ForeignKey('units.unit_id'), nullable=False)

    def __init__(self, title, description, point_type, lat, lon, unit_id, point_id=None):
        self.point_id = point_id if point_id != None else uuid.uuid4()
        self.title = title
        self.description = description
        self.point_type = point_type
        self.lat = lat
        self.lon = lon
        self.created_at = self._get_current_timestamp()
        self.unit_id = unit_id

    def __repr__(self):
        return '<locator_point {point_id}>'.format(point_id=self.point_id)

    def _get_current_timestamp(self):
        return datetime.now()
