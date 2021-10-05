from flask import current_app
from twilio.rest import Client


# Send alert sms when new locator pouints are received
def send_alert_sms(locator_point, user):
    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    map_image_src = "https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=16&size=500x500&maptype=roadmap&markers=icon:https://raw.githubusercontent.com/fernandoleira/lps-platform/main/lps/static/img/red_marker.png%7C{lat},{lon}&format=png32&key={google_api_key}".format(
        lat=str(locator_point.lat), lon=str(locator_point.lon), google_api_key=current_app.config['GOOGLE_CLOUD_API_KEY']
    )

    alert_message = client.messages.create(
        body="New Alert Point Detected!",
        media_url=map_image_src,
        from_=current_app.config['TWILIO_PHONE_NUMBER'],
        to='+{}'.format(user.phone_number)
    )

    print(alert_message.sid)
