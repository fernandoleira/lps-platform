from lps import ma


class UnitSchema(ma.Schema):
    class Meta:
        fields = ('unit_id', 'unit_name')

class LocatorPointSchema(ma.Schema):
    class Meta:
        fields = ('point_id', 'title', 'description', 'type', 'lon', 'lat', 'created_at', 'unit_id')
