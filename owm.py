#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Fetch data from openweathermap API and save to a file.

Todo:
    Call limit checking
    Ensure only fetching data required

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

owm = config["apis"]["openweathermap"]
key = owm["secret"]
lat = owm["latitude"]
lon = owm["longitude"]

if key != "Replace me":
    logger.debug(f"\nKey: {key}\nLatitude: {lat}\nLongitude: {lon}")
    res = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily&appid={key}")
else:
    logger.error("No OpenWeatherMap API key present in configuration")
    exit(-1)

with open("forecast.json", "w+") as forecast:
    logger.debug(repr(forecast))
    json.dump(json.loads(res.content), forecast)
