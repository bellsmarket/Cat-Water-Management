#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
import os
from time import sleep
import Adafruit_DHT
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


MAIL_ADDRESS = 'bellsmarketweb@gmail.com'
PASSWORD = 'bellsmarket'
to_address = "bellsmarketweb@gmail.com"
from_address = "bellsmarketweb@gmail.com"



def send_mail(body_msg = "Hello", subject = "test"):
  msg = MIMEText(body_msg)
  msg['Subject'] = subject
  msg['From'] = from_address
  msg['To'] = to_address
  msg['Date'] = formatdate()


  smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
  smtpobj.ehlo()
  smtpobj.starttls()
  smtpobj.ehlo()
  smtpobj.login(MAIL_ADDRESS, PASSWORD)

  smtpobj.sendmail(from_address, to_address, msg.as_string())
  smtpobj.close()

def h(body = "Hello"):
  print(body)

if __name__ == '__main__':
    h()
    send_mail()
