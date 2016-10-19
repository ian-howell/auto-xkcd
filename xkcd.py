#!/usr/bin/python3
from time import sleep
from datetime import date
import smtplib
import requests
import bs4
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def getImage(text):
    soup = bs4.BeautifulSoup(text, "lxml")
    imgTag = soup.select('#comic img')
    image = {}
    image['title'] = imgTag[0].get('alt')
    image['url'] = 'http:{0}'.format(imgTag[0].get('src'))
    image['text'] = imgTag[0].get('title')
    return image


def buildMessage(username, image):
    # Create the message
    msg = MIMEMultipart()
    msg['Subject'] = image['title']
    msg['From'] = username
    msg['To'] = username
    text = MIMEText(image['text'])
    imgFile = open(os.path.basename(image['url']), 'rb').read()
    imageAttach = MIMEImage(imgFile, name=os.path.basename(image['url']))
    msg.attach(imageAttach)
    msg.attach(text)
    return msg


def sendComic(username, password, msg):
    # Set up the SMTP server
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(username, password)

    # Send the message
    smtpObj.send_message(msg)

    # Close the SMTP connection
    smtpObj.quit()


def doEverything(username, password, oldImgTitle):
    # Get the page
    res = requests.get('http://xkcd.com')

    # Parse out the comic
    image = getImage(res.text)

    # Make sure we have a new image
    while (image['title'] == oldImgTitle):
        # Wait an hour, then try again
        sleep(60 * 60)

        # Get the page
        res = requests.get('http://xkcd.com')

        # Parse out the comic
        image = getImage(res.text)

    print("Got a new comic!")
    print(image['title'])

    # Download the image
    res = requests.get(image['url'])
    imgFile = open(os.path.basename(image['url']), 'wb')
    for chunk in res.iter_content(100000):
        imgFile.write(chunk)
    imgFile.close()

    # Create the message
    message = buildMessage(username, image)

    # Send the comic
    sendComic(username, password, message)

    # Delete the old image
    os.remove(os.path.basename(image['url']))

    # Return the new image title
    return image['title']


def main():
    # Get the username and password
    username = input("Username: ")
    password = input("Password: ")

    oldImgTitle = ''
    oldDay = 0

    while (True):
        curDay = date.today().isoweekday()
        if curDay in [1, 3, 5] and curDay != oldDay:
            # Save the current day
            oldDay = curDay

            # Do everything, then save the new image title
            oldImgTitle = doEverything(username, password, oldImgTitle)
        else:
            # Otherwise, try again tomorrow
            sleep(60*60*24)


if __name__ == "__main__":
    main()
