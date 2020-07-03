import smtplib
from utils import driver
import glob
import os
from email.mime.application import MIMEApplication

'''
    get test_name and create html file with the result of this test
'''
def create(test_name):
    html = """<html>"""
    html += "<h1>{}</h1>".format(test_name)
    html += '<table border="1"><tr><th style="width:50px">description</th><th style="width:50px">result</th></tr>'
    for test_result in driver.global_tests_result:
        if test_result['name'] == test_name:    #the requested test
            for result in test_result['results']:
                html += "<tr><td>{}</td>".format(result[1])
                html += "<td>{}</td></tr>".format(result[0])
    html += "</table></html>"

    # Create directory
    try:
        os.mkdir("..\\" + driver.tests_folders_names)
    except FileExistsError:
        print("add test result to exists folder")

    file_ = open("..\\" + driver.tests_folders_names + "\\" + test_name + '.html', 'w')
    file_.write(html)
    file_.close()
    return html


'''
    send email that contains all the files with the results of the requested tests
'''
def send_email():
    from email.mime.multipart import MIMEMultipart
    me = "keepersAutomation@gmail.com"
    you = "yamushkach@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "keepers Automation Result"
    msg['From'] = me
    msg['To'] = you

    mylist = [f for f in glob.glob(os.path.join("..\\" + driver.tests_folders_names, '*.html'))]
    # Create the body of the message
    for file in mylist:
        file_path = os.path.join(file)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition', 'attachment', filename=file.split("\\")[-1])
        msg.attach(attachment)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(me, 'keepers123')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()

