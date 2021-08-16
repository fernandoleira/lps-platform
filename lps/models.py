from datetime import datetime
from sqlalchemy import Column, Integer, FLOAT, VARCHAR, TEXT, TIMESTAMP, Sequence, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from lps import db


class Unit(db.Model):
    __tablename__ = 'units'

    unit_id = Column('unit_id', UUID(as_uuid=True), primary_key=True)
    name = Column('name', VARCHAR(50), nullable=False, unique=True)

    def __init__(self, name, unit_id=uuid.uuid4()):
        self.unit_id = unit_id
        self.name = name

    def __repr__(self):
        return '<unit {unit_id}>'.format(unit_id=self.unit_id)


class LocatorPoint(db.Model):
    __tablename__ = 'locator_points'

    point_id = Column('point_id', UUID(as_uuid=True), primary_key=True)
    title = Column('title', VARCHAR(50), nullable=False)
    description = Column('description', TEXT)
    point_type = Column('point_type', VARCHAR(50), nullable=False)
    lat = Column('lat', FLOAT, nullable=False)
    lon = Column('lon', FLOAT, nullable=False)
    created_at = Column('created_at', TIMESTAMP(0))
    unit_id = Column('unit_id', UUID(as_uuid=True), ForeignKey('units.unit_id'), nullable=False)

    def __init__(self, title, description, point_type, lat, lon, unit_id, point_id=uuid.uuid4()):
        self.point_id = point_id
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
