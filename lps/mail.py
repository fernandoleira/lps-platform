from lps import mail

# TODO
def send_alert_mail(locator_point):
    msg = Message()
    msg.html = "<h1>This is a Test</h1>"
    msg.add_recipient("fer.leira@hotmail.com")
    
    mail.send(msg)
