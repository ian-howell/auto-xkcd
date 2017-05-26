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

    text = MIMEText('\n' + image['text'] + '\n\n' + weather)
    img_filename = '/tmp/' + os.path.basename(image['url'])
    imgFile = open(img_filename, 'rb').read()
    imageAttach = MIMEImage(imgFile, name=img_filename)
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


def get_weather(key, city_id):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=' + city_id + '&APPID=' + key)
    weather_data = json.loads(r.text)

    city_name = weather_data['name']
    current_temp = kelv_to_fahr(weather_data['main']['temp'])
    weather_string = 'Current temperature in ' + city_name + ': {0:.1f} \u00B0F\n'.format(current_temp)

    return weather_string


def main():
    # Get the username and password
    username = input("Username: ")
    password = input("Password: ")
    api_key = input("API key: ")
    city_id = input("City ID: ")

    try:
        # Get the page
        res = requests.get('http://xkcd.com')

        # Parse out the comic
        image = getImage(res.text)

        print("Got a new comic!")
        print(image['title'])

        # Download the image
        res = requests.get(image['url'])
        img_filename = '/tmp/' + os.path.basename(image['url'])
        imgFile = open(img_filename, 'wb')
        for chunk in res.iter_content(100000):
            imgFile.write(chunk)
        imgFile.close()

        # Get Weather data for today
        weather = get_weather(api_key, city_id)

        # Create the message
        message = buildMessage(username, image, weather)

        # Send the comic
        sendComic(username, password, message)

        # Delete the old image
        os.remove(img_filename)
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
