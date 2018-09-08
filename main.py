#!/usr/bin/python3
from comic import get_newest_xkcd
from configparser import ConfigParser
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sender import send_email
import sys
from weather import format_weather, get_current_weather


def main(args):
    config = ConfigParser()
    config.read(args[1])

    email = config['EMAIL']
    weather = config['WEATHER']

    try:
        message_content = {}
        message_content['xkcd_info'] = get_newest_xkcd()
        message_content['weather_info'] = get_current_weather(
            weather['api_key'], weather['city_id'])

        message = build_message(email['address'], message_content)

        send_email(email['address'], email['password'], message)
    except Exception as e:
        error_message = build_error(email['address'], email['password'], e)
        send_email(email['address'], email['password'], error_message)


def build_message(email_addr, message_content):
    # Unpack the message content
    xkcd_info = message_content['xkcd_info']
    weather_info = message_content['weather_info']

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


def build_error(email_addr, password, e):
    raw_except = str(type(e))
    idx_1 = raw_except.find('\'') + 1
    idx_2 = raw_except.find('\'', idx_1)
    exception_name = raw_except[idx_1:idx_2]

    error_message = "A {} was caught\n".format(exception_name)
    error_message += "Exception message: {}".format(e)

    message = MIMEText(error_message)
    message['Subject'] = "Subject: Caught a {}\n".format(exception_name)
    message['To'] = email_addr
    message['From'] = email_addr

    return message


if __name__ == "__main__":
    main(sys.argv)
