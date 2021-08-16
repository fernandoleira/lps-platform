import csv
from pathlib import Path

from lps.models import *

SEED_FOLDER_PATH = Path("db/")


def import_from_csv(csv_filename):
    with open(SEED_FOLDER_PATH / csv_filename) as csv_file:
        csv_read = csv.DictReader(csv_file, delimiter=',')
        return list(csv_read)


def seed_database(db):
    print("======== STARTING DATABASE SEED ========")
    
    seed_data = import_from_csv("units.csv")
    for obj in seed_data:
        seed = Unit(obj["name"], unit_id=obj["unit_id"])
        db.session.add(seed)
        print(seed)
    db.session.commit()
    
    print()

    seed_data = import_from_csv("points.csv")
    for obj in seed_data:
        seed = LocatorPoint(obj["title"], obj["description"], obj["point_type"], float(obj['lat']), float(obj['lon']), obj['unit_id'], point_id=obj['point_id'])
        db.session.add(seed)
        print(seed)
    db.session.commit()

    print("======== SEED COMPLETED ========")
