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
import json

def getImage(text):
    soup = bs4.BeautifulSoup(text, "lxml")
    imgTag = soup.select('#comic img')
    image = {}
    image['title'] = imgTag[0].get('alt')
    image['url'] = 'http:{0}'.format(imgTag[0].get('src'))
    image['text'] = imgTag[0].get('title')
    return image


def buildMessage(username, image, weather):
    # Create the message
    msg = MIMEMultipart()
    msg['Subject'] = image['title']
    msg['From'] = username
    msg['To'] = username
    weather_message = '\n\nToday\'s weather:\n' + weather
    text = MIMEText(image['text'] + '\n' + weather_message)
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


def kelv_to_fahr(temp):
    return (temp - 273.15) * 1.8 + 32


def get_weather():
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=4406282&APPID=d72e6d9498368991dd8d6a255023287c')
    weather_data = json.loads(r.text)['main']

    weather_string = ''
    weather_string += 'Now : {0:.1f} \u00B0F\n'.format(kelv_to_fahr(weather_data['temp']))
    weather_string += 'Low : {0:.1f} \u00B0F\n'.format(kelv_to_fahr(weather_data['temp_min']))
    weather_string += 'High: {0:.1f} \u00B0F\n'.format(kelv_to_fahr(weather_data['temp_max']))

    return weather_string


def main():
    get_weather()
    # Get the username and password
    username = input("Username: ")
    password = input("Password: ")

    try:
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

        # Get Weather data for today
        weather = get_weather()

        # Create the message
        message = buildMessage(username, image, weather)

        # Send the comic
        sendComic(username, password, message)

        # Delete the old image
        os.remove(os.path.basename(image['url']))
    except Exception as e:
        # Attempt to send a warning that everything broke
        # Set up the SMTP server
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(username, password)

        msg = 'Subject: ERROR: auto-xkcd\n'
        msg += 'Something went wrong with auto-xkcd.\n'
        msg += 'Exception thrown: {}\n'.format(e)

        # Send the message
        smtpObj.sendmail(username, username, msg)

        # Close the SMTP connection
        smtpObj.quit()

if __name__ == "__main__":
    main()
