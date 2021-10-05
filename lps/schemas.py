from lps import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username', 'email', 'password', 'is_admin', 'is_super')


class ApiKeySchema(ma.Schema):
    class Meta:
        fields = ('api_key', 'user_id', 'created_at', 'updated_at', 'expired_at')


class UnitSchema(ma.Schema):
    class Meta:
        fields = ('unit_id', 'name', 'user_id', 'alert_mail', 'alert_sms')


class LocatorPointSchema(ma.Schema):
    class Meta:
        fields = ('point_id', 'title', 'description', 'point_type', 'lon', 'lat', 'created_at', 'unit_id')
