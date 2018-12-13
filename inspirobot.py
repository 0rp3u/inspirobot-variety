#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

"""
    Variety quote plugin sourcing quotes from inspirobit.me
    This script is placed in '~/.config/variety/plugins' and then activated from inside Variety's
    Preferences Quotes menu
    If script fails, you need to run: pip install requests
"""

import logging
import random
from threading import Thread
import requests

from locale import gettext as _
from variety.Util import Util
from variety.plugins.IQuoteSource import IQuoteSource
from io import BytesIO


logger = logging.getLogger("variety")


def fetchAndSaveImages(image_mame):
        r = requests.get('https://source.unsplash.com/' + image_mame + '/1600x900')

        if(r.status_code == 200):
            with open('.config/variety/Fetched/' + image_mame + '.jpg', 'wb') as file:
                image_bytes = BytesIO(r.content)
                file.write(image_bytes.getvalue())
                image_bytes.close()
        else:
             logger.warning(r.content)


class GoodreadsSource(IQuoteSource):
    """
        Retrives quotes from inspirobot.me.
        Attributes:
            quotes(list): list containing the quotes
    """

    def __init__(self):
        super(IQuoteSource, self).__init__()
        self.quotes = []

    @classmethod
    def get_info(cls):
        return {
            "name": "inspirobot",
            "description": _("AI generated quotes from inspirobot.me"),
            "author": "0rpheu",
            "version": "0.1"
        }

    def supports_search(self):
        return False

    def activate(self):
        if self.active:
            return
        self.active = True

    def deactivate(self):
        self.active = False


    def fetch_inspirobot_quotes(self):
        quotes = []
        response = requests.get('https://inspirobot.me/api?generateFlow=1')
        json_object = response.json()
        for row in json_object['data']:
            if row['type'] == "quote":
                quotes.append(
                {
                    "quote": row['text'],
                    "author": "",
                    "sourceName": "inspirobot.me",
                    "link": " https://inspirobot.me"
                }
            )
            elif row['type'] == "transition":
                logger.warning('thread to fetch image ' + 'https://source.unsplash.com/' + row['image'] + '/1600x900')
                thread = Thread(target = fetchAndSaveImages, args = (row['image'],))
                thread.start()
            
        return quotes
       

    def get_for_author(self, author):
        return []

    def get_for_keyword(self, keyword):
        return []

    def get_random(self):
        return self.fetch_inspirobot_quotes()