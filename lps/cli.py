from flask_mail import Message
from lps import app, db, mail
from lps.models import *
from lps.seeds import seed_database, export_seed
from lps.mail import *


# DATABASE COMMANDS
@app.cli.command("seed_db")
def seed_db():
    print("======== STARTING DATABASE SEED ========")
    seed_database(db)
    print("======== SEED COMPLETED ========")


@app.cli.command("reset_db")
def reset_db():
    LocatorPoint.query.delete()
    Unit.query.delete()
    ApiKey.query.delete()
    User.query.delete()
    db.session.commit()
    print("======== RESET DATABASE ========")


@app.cli.command("export_db")
def export_db():
    print("======== EXPORTING DATABASE SEED ========")
    export_seed()
    print("======== EXPORT COMPLETED ========")


# MAIL SERVER COMMANDS
@app.cli.command("test_mail")
def test_mail():
    send_alert_mail("")
