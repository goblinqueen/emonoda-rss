#!/usr/bin/env python3.4

import requests
from nma_settings import api_key


def notify(anime_name, title):
    req = {'apikey': api_key,
           'application': "bear fetcher",
           'event': anime_name + ' fetched!',
           'description': title,
           'content-type': 'text/html'
           }

    return requests.post("https://www.notifymyandroid.com/publicapi/notify", data=req)
