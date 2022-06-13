import os
from flask import render_template, current_app
from flask_mail import Message
from api import mail


# Send alert emails when new locator pouints are received
def send_alert_mail(locator_point, user):
    msg = Message()
    msg.subject = "New Alert Point"
    msg.html = render_template("mail.html", point=locator_point, google_api_key=current_app.config['GOOGLE_CLOUD_API_KEY'])
    msg.add_recipient(user.email)
    
    with current_app.open_resource(os.path.join("static", "img", "logo_menu.png")) as fp:
        msg.attach("logo_menu.png", "image/png", fp.read())

    mail.send(msg)
