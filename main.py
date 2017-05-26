#!/usr/bin/python3
from comic import get_newest_xkcd
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sender import send_comic
from weather import format_weather, get_current_weather

def main():
    email_addr = input("Email address: ")
    password = input("Password: ")
    api_key = input("API key: ")
    city_id = input("City ID: ")

    xkcd_info = get_newest_xkcd()
    weather_info = get_current_weather(api_key, city_id)

    message = build_message(email_addr, xkcd_info, weather_info)

    send_comic(email_addr, password, message)

def build_message(email_addr, xkcd_info, weather_info):
    # Load the image to be sent
    img_file = open(xkcd_info['img'], 'rb').read()

    # Set up the body of the email (text)
    formatted_weather = format_weather(weather_info)
    email_body = "\n{}\n".format(xkcd_info['alt'])
    email_body += "\n{}".format(formatted_weather)

    # Set up the email
    message = MIMEMultipart()
    message['Subject'] = xkcd_info['title']
    message['To'] = email_addr
    message['From'] = email_addr
    message.attach(MIMEImage(img_file))
    message.attach(MIMEText(email_body))

    return message

if __name__ == "__main__":
   main()
