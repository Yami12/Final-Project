'''
This file create HTML file and send an email
'''

import smtplib
import glob
import os
from email.mime.application import MIMEApplication
import pathlib

from utils import driver
from utils import utils_funcs as uf


'''
    function: create_html_file
    description: get test_name and create html file with the result of this test
'''
def create_html_file(test_name):
    html = """<html>"""
    html += "<h1 style='text-align: center'>{}</h1>".format(test_name)
    html += '<table border="1"><tr><th style="width:50px">description</th><th style="width:50px">result</th></tr>'
    for test_result in driver.global_tests_result:
        if test_result['name'] == test_name:    #the requested test
            for result in test_result['results']:
                html += "<tr><td>{}</td>".format(result[1])
                html += "<td>{}</td></tr>".format(result[0])
    html += "</table></html>"
    if driver.test_result == True:
        html += "<h1 style='color: green; text-align: center'>PASSED</h1>"
    elif driver.test_result == False:
        html += "<h1 style='color: red; text-align: center'>FAILED</h1>"
    else:
        html += "<h1 style='color: red; text-align: center'>ERROR</h1>"



    # Create directory
    try:
        os.mkdir("..\\" + driver.tests_folders_names)
    except FileExistsError:
        uf.print_log("\cf1 adding test result to exists folder \line")

    uf.print_log("\cf1 write the results to the file \line")
    file_ = open("..\\" + driver.tests_folders_names + "\\" + test_name + '.html', 'w')
    file_.write(html)
    file_.close()

'''
    function: send_email
    description: send email that contains all the files with the results of the requested tests
'''
def send_email(address):
    from email.mime.multipart import MIMEMultipart
    reciepent = "keepersAutomation@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "keepers Automation Result"
    msg['From'] = reciepent
    msg['To'] = address

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
    mail.login(reciepent, 'keepers123')
    mail.sendmail(reciepent, address, msg.as_string())
    mail.quit()

