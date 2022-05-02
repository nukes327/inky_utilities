#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Fetch data from darksky API and save to a file.

Todo:
    Implement call limit checking

"""

import json
import requests
import toml
import logging
import logging.config

import lib

lib.load_logging()
logger = logging.getLogger(__name__)
logger.info("Logging configuration loaded")


with open("config/utils.toml", "r") as conffile:
    try:
        config = toml.load(conffile)
    except Exception as inst:
        lib.validate_config()
        config = toml.load(conffile)
logger.info("Utility configuration loaded")

darksky = config["apis"]["darksky"]
key = darksky["secret"]
lat = darksky["latitude"]
lon = darksky["longitude"]

if key != "Replace me":
    logger.debug(f"\nKey: {key}\nLatitude: {lat}\nLongitude: {lon}")
    res = requests.get(f"https://api.darksky.net/forecast/{key}/{lat},{lon}?exclude=minutely,hourly,daily")
else:
    logger.error("No darksky API key present in configuration")
    exit(-1)

with open("forecast.json", "w+") as forecast:
    logger.debug(repr(forecast))
    json.dump(json.loads(res.content), forecast)
