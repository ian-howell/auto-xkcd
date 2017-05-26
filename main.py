#!/usr/bin/python3
from comic import get_newest_xkcd
from weather import get_current_weather

def main():
    username = input("Username: ")
    password = input("Password: ")
    api_key = input("API key: ")
    city_id = input("City ID: ")

    xkcd_info = get_newest_xkcd()
    weather_info = get_current_weather(api_key, city_id)

if __name__ == "__main__":
   main()
