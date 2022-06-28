import csv
from pathlib import Path
from datetime import datetime
from api.models import User, Unit, LocatorPoint, ApiKey
from api.schemas import UserSchema, UnitSchema, LocatorPointSchema, ApiKeySchema


def import_from_csv(csv_filename, seed_path):
    fn = Path(seed_path).joinpath(csv_filename)
    if fn.is_file():
        with open(fn) as csv_file:
            csv_read = csv.DictReader(csv_file, delimiter=',')
            return list(csv_read)
    else:
        return []


def export_to_csv(model_dict, seed_path, csv_filename="out.csv"):
    if len(model_dict) > 0:
        fn = Path(seed_path).joinpath(csv_filename)
        with open(fn, "w") as csv_filename:
            csv_filename.write(",".join(model_dict[0].keys()) + '\n')

            for i in range(len(model_dict)):
                csv_filename.write(
                    ",".join([str(elm) for elm in model_dict[i].values()]) + '\n')

        return True

    else:
        return False


def seed_database(db, seed_path):
    # Users
    seed_data = import_from_csv("users.csv", seed_path)
    for obj in seed_data:
        if obj["is_admin"] == 'FALSE':
            is_admin = False
        else:
            is_admin = True
        if obj["is_super"] == 'FALSE':
            is_super = False
        else:
            is_super = True
        seed = User(obj["username"], obj["email"], obj["phone_number"], obj["password"], is_admin=is_admin, is_super=is_super, user_id=obj['user_id'])
        db.session.add(seed)
        print(seed)
    db.session.commit()

    print()

    # Api Key
    seed_data = import_from_csv("api_keys.csv", seed_path)
    for obj in seed_data:
        seed = ApiKey(obj["user_id"], api_key=obj["api_key"])
        db.session.add(seed)
        print(seed)
    db.session.commit()

    print()

    # Units
    seed_data = import_from_csv("units.csv", seed_path)
    for obj in seed_data:
        if obj["alert_sms"] == 'FALSE':
            alert_sms = False
        else:
            alert_sms = True
        if obj["alert_mail"] == 'FALSE':
            alert_mail = False
        else:
            alert_mail = True
        seed = Unit(obj["name"], obj["user_id"], alert_mail, alert_sms, unit_id=obj["unit_id"])
        db.session.add(seed)
        print(seed)
    db.session.commit()

    print()

    # Locator Points
    seed_data = import_from_csv("points.csv", seed_path)
    for obj in seed_data:
        seed = LocatorPoint(obj["title"], obj["description"], obj["point_type"], float(
            obj['lat']), float(obj['lon']), obj['unit_id'], point_id=obj['point_id'])
        db.session.add(seed)
        print(seed)
    db.session.commit()


def export_seed(seed_path):
    # Units
    units_q = Unit.query.all()
    units = UnitSchema(many=True).dump(units_q)
    export_check = export_to_csv(units, seed_path, "units.csv")
    if export_check:
        print("--> Units export has been completed to 'units.csv'")
    else:
        print("--> An error has occurred exporting Units")

    # Locator Points
    points_q = LocatorPoint.query.all()
    points = LocatorPointSchema(many=True).dump(points_q)
    export_check = export_to_csv(points, seed_path, "points.csv")
    if export_check:
        print("--> Locator Points export has been completed to 'points.csv'")
    else:
        print("--> An error has occurred exporting Locator Points")

    # Users
    users_q = User.query.all()
    users = UserSchema(many=True).dump(users_q)
    export_check = export_to_csv(users, seed_path, "users.csv")
    if export_check:
        print("--> Users export has been completed to 'users.csv'")
    else:
        print("--> An error has occurred exporting Users")

    # Api Keys
    api_keys_q = ApiKey.query.all()
    api_keys = ApiKeySchema(many=True).dump(api_keys_q)
    export_check = export_to_csv(api_keys, seed_path, "api_keys.csv")
    if export_check:
        print("--> Api Keys export has been completed to 'api_keys.csv'")
    else:
        print("--> An error has occurred exporting Api Keys")
