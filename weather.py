#!/usr/bin/python3
import json
import requests


def get_current_weather(key, city):
    api_string = _build_url(key, city)
    weather_info = _get_weather_info(api_string)
    return weather_info


def format_weather(weather_info):
    degree_char = '\u00B0'
    formatted = "Current temperature in {}".format(weather_info['city'])
    formatted += ": {:.1f} {}F\n".format(weather_info['temp'], degree_char)
    return formatted


def _get_weather_info(api_string):
    res = requests.get(api_string)
    weather_info = json.loads(res.text)
    minimal_info = {
            'city': weather_info['name'],
            'temp': _kelv_to_fahr(weather_info['main']['temp']),
            }
    return minimal_info


def _kelv_to_fahr(temp):
    return (temp - 273.15) * 1.8 + 32


def _build_url(key, city):
    city_id = "id={}".format(city)
    app_id = "APPID={}".format(key)
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    return "{}?{}&{}".format(base_url, city_id, app_id)
