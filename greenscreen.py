#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Cleanup script to make transparency work for inky hats.

Attribution:
    This script is courtesy of user mikeyp on pimoroni forums.

Notes:
    Fixes issues with GIMP's transparency export by using a green screen method.

    Any pixels that should be transparent are first painted green using
    the fourth color of the colormap.

    Once the image is saved in the assets directory this script can be run to clean
    any images of greenscreen, leaving behind transparency.

WARNING:
    PIL completely CLOBBERS any tEXt tags that were in the image from a quick test
    This is potentially a MAJOR issue, more testing needs to be done

Todo:
    Modify this script so it doesn't clobber tEXt chunks that were added to the image

"""


from PIL import Image
import glob

for ui_elem in glob.glob("resources/*.png"):
    img = Image.open(ui_elem)
    img.save(ui_elem, transparency=3, optimize=1)  # type: ignore
