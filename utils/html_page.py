import smtplib


def create(test_results):
    html = """<html><table border="1">
    <tr><th style="width:50px">flow</th><th style="width:50px">test</th><th style="width:50px">result</th></tr>"""
    for result in test_results:
        html += "<tr><td>{}</td>".format(result[0])
        html += "<td>{}</td>".format(result[1])
        html += "<td>{}</td></tr>".format(result[2])
    html += "</table></html>"

    file_ = open('tests_result.html', 'w')
    file_.write(html)
    file_.close()
    return html


def send_email():
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    me = "keepersAutomation@gmail.com"
    you = "yamushkach@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "keepers Automation Result"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    html = create([[1,2,3],[4,5,6]])

    msg.attach(MIMEText(html, 'html'))
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(me, 'keepers123')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()


