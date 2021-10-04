from flask import current_app
from twilio.rest import Client


# Send alert sms when new locator pouints are received
def send_alert_sms(locator_point, user):
    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="New Alert Point Detected!",
        from_=current_app.config['TWILIO_PHONE_NUMBER'],
        to='+{}'.format(user.phone_number)
    )

    print(message.sid)
