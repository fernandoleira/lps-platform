import csv
from pathlib import Path

from lps.models import *
from lps.schemas import *


SEED_FOLDER_PATH = Path("db/")


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
    # Units
    seed_data = import_from_csv("units.csv")
    for obj in seed_data:
        seed = Unit(obj["name"], unit_id=obj["unit_id"])
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
