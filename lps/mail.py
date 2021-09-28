from flask import render_template
from flask_mail import Message
from lps import mail


# Send alert emails when new locator pouints are received
def send_alert_mail(locator_point, user):
    msg = Message()
    msg.subject = "New Alert Point"
    msg.html = render_template("mail.html", point=locator_point)
    msg.add_recipient(user.email)
    
    mail.send(msg)
