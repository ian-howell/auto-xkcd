import smtplib
import requests
import bs4
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# Set up the SMTP server
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()

# Get the username and password
username = input("Username: ")
password = input("Password: ")
smtpObj.login(username, password)

oldImgTitle = ''

while (True):
    # Get the page
    res = requests.get('http://xkcd.com')

    # Parse out the comic
    soup = bs4.BeautifulSoup(res.text, "lxml")
    imgTag = soup.select('#comic img')

    imgTitle = imgTag[0].get('alt')
    if (imgTitle != oldImgTitle):
        print("Got a new comic!")
        print(imgTitle)

        # Reset the old title so that we only do this once
        oldImgTitle = imgTitle

        # Get the image and mouseover text
        imgUrl = 'http:{0}'.format(imgTag[0].get('src'))
        imgMouseove = imgTag[0].get('title')

        # Download the image
        res = requests.get(imgUrl)
        imgFile = open(os.path.basename(imgUrl), 'wb')
        for chunk in res.iter_content(100000):
            imgFile.write(chunk)
        imgFile.close()

        # Create the message
        msg = MIMEMultipart()
        msg['Subject'] = imgTitle
        msg['From'] = username
        msg['To'] = username
        text = MIMEText(imgMouseove)
        imgFile = open(os.path.basename(imgUrl), 'rb').read()
        image = MIMEImage(imgFile, name=os.path.basename(imgUrl))
        msg.attach(image)
        msg.attach(text)

        # Send the message
        smtpObj.sendmail('Pi', username, msg.as_string())

        # Delete the old image
        os.remove(os.path.basename(imgUrl))
