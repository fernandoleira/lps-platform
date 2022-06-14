import click
from flask.cli import AppGroup
from api import db
from api.models import *
from api.seeds import seed_database, export_seed
from api.mail import send_alert_mail

api_cli = AppGroup('api')

# DATABASE COMMANDS
@api_cli.command('seed_db')
def seed_db():
    print("======== STARTING DATABASE SEED ========")
    seed_database(db)
    print("======== SEED COMPLETED ========")


@api_cli.command('reset_db')
def reset_db():
    LocatorPoint.query.delete()
    Unit.query.delete()
    ApiKey.query.delete()
    User.query.delete()
    db.session.commit()
    print("======== RESET DATABASE ========")


@api_cli.command('export_db')
def export_db():
    print("======== EXPORTING DATABASE SEED ========")
    export_seed()
    print("======== EXPORT COMPLETED ========")


# DATA SEED COMMANDS
@api_cli.command('create_user')
@click.argument('username_inp')
def create_user(username_inp):
    check_username = User.query.filter_by(username=username_inp).first()
    if check_username is None:
        new_user = User(username_inp, f"{username_inp}@email.com", 13057668986, "password")
        db.session.add(new_user)
        db.session.commit()
        print("======== USER CREATED ========")
        print(new_user)
    else:
       print("======== ERROR ========") 


# MAIL SERVER COMMANDS
@api_cli.command('test_mail')
def test_mail():
    user = User.query.filter_by(username="fernandoleira").first()
    locator_point = LocatorPoint.query.filter_by(point_id="a413e8de-fcf9-4f9c-8023-6bd2c2dc43e7").first()
    send_alert_mail(locator_point, user)