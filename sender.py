#!/usr/bin/python3
import smtplib

def send_comic(email_addr, password, message):
    # Set up the SMTP server
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(email_addr, password)

    # Send the message
    smtpObj.send_message(message)

    # Close the SMTP connection
    smtpObj.quit()

