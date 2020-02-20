#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Fetch data from darksky API and save to a file."""

import json
import requests
import toml
import logging

logging.config.fileConfig("config/logging.ini")
logger = logging.getLogger(__name__)
logger.info("Logging configuration loaded")


with open("config/utils.toml", "r") as conffile:
    config = toml.load(conffile)
logger.info("Configuration loaded")

darksky = config["apis"]["darksky"]
key = darksky["secret"]
lat = darksky["latitude"]
lon = darksky["longitude"]

if key != "Replace me":
    logger.debug(f"\nKey: {key}\nLatitude: {lat}\nLongitude: {long}")
    res = requests.get(f"https://api.darksky.net/forecast/{key}/{lat},{lon}")
else:
    logger.error("No developer API key present")
    exit(-1)

with open("forecast.json", "w+") as forecast:
    logger.debug(repr(forecast))
    json.dump(json.loads(res.content), forecast)
