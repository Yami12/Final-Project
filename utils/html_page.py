import smtplib
from utils import driver

def create(test_name):
    html = """<html><table border="1">"""
    html += "<h1>{}</h1>".format(test_name)
    html += '<tr><th style="width:50px">description</th><th style="width:50px">result</th></tr>'
    for test_result in driver.global_tests_result:
        if test_result['name'] == test_name:
            for result in test_result['results']:
                html += "<tr><td>{}</td>".format(result[0])
                html += "<td>{}</td></tr>".format(result[1])
    html += "</table></html>"

    file_ = open(test_name + '.html', 'w')
    file_.write(html)
    file_.close()
    return html


def send_email(tests_names):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    me = "keepersAutomation@gmail.com"
    you = "yamushkach@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "keepers Automation Result"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message
    for test_name in tests_names:
        html = create(test_name)
        msg.attach(MIMEText(html, 'html'))
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(me, 'keepers123')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()