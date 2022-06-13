import csv
from pathlib import Path
from datetime import datetime
from api.models import *
from api.schemas import *


SEED_FOLDER_PATH = Path("db/seeds/")


def import_from_csv(csv_filename):
    with open(SEED_FOLDER_PATH / csv_filename) as csv_file:
        csv_read = csv.DictReader(csv_file, delimiter=',')
        return list(csv_read)


def export_to_csv(model_dict, csv_filename="out.csv"):
    if len(model_dict) > 0:
        with open(SEED_FOLDER_PATH / csv_filename, "w") as csv_filename:
            csv_filename.write(",".join(model_dict[0].keys()) + '\n')
            
            for i in range(len(model_dict)):
                csv_filename.write(",".join([str(elm) for elm in model_dict[i].values()]) + '\n')

        return True
    
    else:
        return False


def seed_database(db):
    # Users
    seed_data = import_from_csv("users.csv")
    for obj in seed_data:
        seed = User(obj["username"], obj["email"], obj["phone_number"], obj["password"], is_admin=bool(obj["is_admin"]), is_super=bool(obj["is_super"]), user_id=obj['user_id'])
        db.session.add(seed)
        print(seed)
    db.session.commit()

    print()

    # Api Key
    seed_data = import_from_csv("api_keys.csv")
    for obj in seed_data:
        seed = ApiKey(obj["user_id"], api_key=obj["api_key"])
        db.session.add(seed)
        print(seed)
    db.session.commit()
    
    print()

    # Units
    seed_data = import_from_csv("units.csv")
    for obj in seed_data:
        seed = Unit(obj["name"], obj["user_id"], bool(obj["alert_mail"]), bool(obj["alert_sms"]), unit_id=obj["unit_id"])
        db.session.add(seed)
        print(seed)
    db.session.commit()
    
    print()

    # Locator Points
    seed_data = import_from_csv("points.csv")
    for obj in seed_data:
        seed = LocatorPoint(obj["title"], obj["description"], obj["point_type"], float(obj['lat']), float(obj['lon']), obj['unit_id'], point_id=obj['point_id'])
        db.session.add(seed)
        print(seed)
    db.session.commit()


def export_seed():
    # Units
    units_q = Unit.query.all()
    units = UnitSchema(many=True).dump(units_q)
    export_check = export_to_csv(units, "units.csv")
    if export_check:
        print("--> Units export has been completed to 'units.csv'")
    else:
        print("--> An error has occurred exporting Units")

    # Locator Points
    points_q = LocatorPoint.query.all()
    points = LocatorPointSchema(many=True).dump(points_q)
    export_check = export_to_csv(points, "points.csv")
    if export_check:
        print("--> Locator Points export has been completed to 'points.csv'")
    else:
        print("--> An error has occurred exporting Locator Points")

    # Users
    users_q = User.query.all()
    users = UserSchema(many=True).dump(users_q)
    export_check = export_to_csv(users, "users.csv")
    if export_check:
        print("--> Users export has been completed to 'users.csv'")
    else:
        print("--> An error has occurred exporting Users")

    # Api Keys
    api_keys_q = ApiKey.query.all()
    api_keys = ApiKeySchema(many=True).dump(api_keys_q)
    export_check = export_to_csv(api_keys, "api_keys.csv")
    if export_check:
        print("--> Api Keys export has been completed to 'api_keys.csv'")
    else:
        print("--> An error has occurred exporting Api Keys")
