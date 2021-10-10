from flask import cli
from flask.cli import FlaskGroup
from lps import create_app, db
from lps.models import *
from lps.seeds import seed_database, export_seed
from lps.mail_utils import send_alert_mail

app = create_app()
cli = FlaskGroup(create_app=create_app)


# DATABASE COMMANDS
@cli.command("seed_db")
def seed_db():
    print("======== STARTING DATABASE SEED ========")
    seed_database(db)
    print("======== SEED COMPLETED ========")


@cli.command("reset_db")
def reset_db():
    LocatorPoint.query.delete()
    Unit.query.delete()
    ApiKey.query.delete()
    User.query.delete()
    db.session.commit()
    print("======== RESET DATABASE ========")


@cli.command("export_db")
def export_db():
    print("======== EXPORTING DATABASE SEED ========")
    export_seed()
    print("======== EXPORT COMPLETED ========")


# MAIL SERVER COMMANDS
@cli.command("test_mail")
def test_mail():
    send_alert_mail("")


if __name__ == '__main__':
    cli()