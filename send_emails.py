#!/usr/bin/env python
#coding=utf-8

import argparse
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import email
import email.parser
import subprocess
import io
import csv
import getpass

parser = argparse.ArgumentParser()
parser.add_argument('--template', default='templates/survey_reminder.txt')
parser.add_argument('--emails-csv', required=True)
parser.add_argument('--send', default='no', choices=['yes','no']) 

args = parser.parse_args()

with open(args.template) as fid:
    template = fid.read() 

sender = {'mail' : 'Bartosz Telenczuk <telenczuk@unic.cnrs-gif.fr>',
        'firstname' : 'Bartosz'}

students = csv.DictReader(open(args.emails_csv))

parser = email.parser.Parser()
messages = []
email_addresses = []
for student in students: 
    email_txt = template.format(firstname=student['firstname'])
    msg = parser.parsestr(email_txt)
    msg['From'] = sender['mail']
    msg['To'] = student['mail']
    print(msg)
    msg.set_charset('utf-8')
    messages.append((sender['mail'], student['mail'], msg))
    email_addresses.append(student['mail'])

r = 'No'
if args.send == 'yes':
    print("\n" + "\n".join(email_addresses))
    r = input('Do you really want to send messages to these recipients (if yes type "Yes")? ')
    r = r.lower()

if r == 'yes':
    import smtplib
    smtp_host = 'smtp.webfaction.com'
    username = 'bartosz'
    password = getpass.getpass()

    server = smtplib.SMTP(smtp_host)
    server.login(username, password)
    server.starttls()
    for from_addr, to_addr, msg in messages:
        print('Sending to ' + to_addr)
        server.sendmail(from_addr, to_addr, msg.as_string())
