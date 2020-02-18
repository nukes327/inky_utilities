#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Fetch data from darksky API and save to a file."""

import json
import requests
import toml

with open("config/utils.toml", "r") as conffile:
    config = toml.load(conffile)

darksky = config["apis"]["darksky"]
key = darksky["secret"]
lat = darksky["latitude"]
lon = darksky["longitude"]

if key != "Replace me":
    res = requests.get(f"https://api.darksky.net/forecast/{key}/{lat},{lon}")
else:
    print("While this is open source software a private dev key is required for this util")
    exit(-1)

with open("forecast.json", "w+") as forecast:
    json.dump(json.loads(res.content), forecast)
