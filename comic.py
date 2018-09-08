#!/usr/bin/python3
import json
import requests


def get_comic_info():
    api_string = "http://xkcd.com/info.0.json"
    res = requests.get(api_string)
    xkcd_info = json.loads(res.text)
    minimal_info = {
            'title': xkcd_info['title'],
            'alt': xkcd_info['alt'],
            'img': xkcd_info['img'],
            }
    return minimal_info


def download_comic(img):
    res = requests.get(img['img'])
    img_filename = "/tmp/" + img['title'] + '.png'
    with open(img_filename, 'wb') as img_file:
        for chunk in res.iter_content(100000):
            img_file.write(chunk)
    return img_filename


def get_newest_xkcd():
    xkcd_info = get_comic_info()
    filename = download_comic(xkcd_info)

    # Modify the img's path to be the local version
    xkcd_info['img'] = filename
    return xkcd_info
