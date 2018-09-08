#!/usr/bin/python3
from comic import get_newest_xkcd
from configparser import ConfigParser
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sender import send_email
import sys
from weather import format_weather, get_current_weather


def main():
    config = ConfigParser()
    if len(sys.argv) == 2:
        config.read(sys.argv[1])
    else:
        # Use the default
        config.read('config.ini')

    email = config['EMAIL']
    weather = config['WEATHER']
    sections = config['SECTIONS']

    message_content = {}
    if sections['comic'] == 'on':
        try:
            message_content['xkcd_info'] = get_newest_xkcd()
        except Exception as e:
            message_content['xkcd_info'] = e
    if sections['weather'] == 'on':
        try:
            message_content['weather_info'] = get_current_weather(
                weather['api_key'], weather['city_id'])
        except Exception as e:
            message_content['weather_info'] = e

    message = build_message(email['address'], message_content)
    send_email(email, message)


def build_message(email_addr, message_content):
    # Set up the email
    message = MIMEMultipart()
    message['Subject'] = 'The Morning Report'

    email_body = ''
    if 'xkcd_info' in message_content.keys():
        if isinstance(message_content['xkcd_info'], Exception):
            email_body += ("Something went wrong when trying to download "
                           "the latest xkcd. Here is the stacktrace:\n")
            email_body += str(message_content['xkcd_info'])
        else:
            xkcd_info = message_content['xkcd_info']
            message.replace_header('Subject', xkcd_info['title'])
            email_body += "\n{}\n".format(xkcd_info['alt'])

            # Load the image to be sent
            img_file = open(xkcd_info['img'], 'rb').read()
            message.attach(MIMEImage(img_file))

    if 'weather_info' in message_content.keys():
        if isinstance(message_content['weather_info'], Exception):
            email_body += ("Something went wrong when trying to download "
                           "weather info. Here is the stacktrace:\n")
            email_body += str(message_content['weather_info'])
        else:
            weather_info = message_content['weather_info']

            # Set up the body of the email (text)
            formatted_weather = format_weather(weather_info)
            email_body += "\n{}".format(formatted_weather)

    message['To'] = email_addr
    message['From'] = email_addr
    message.attach(MIMEText(email_body))

    return message


if __name__ == "__main__":
    main()
