#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Display an analog clock face on an inky display."""

from PIL import Image, ImageDraw, ImageFont  # type: ignore
from typing import Tuple
import math
import time
import json
import pprint
from random import randint


def get_time() -> None:
    """Fetch the current system time."""
    pass


def draw_fancy_hand(center: Tuple[int, int], length: int, time: int, image: Image) -> None:
    """Draw a hand of given length on the image.

    Args:
        center: Center point of the clock face
        length: The length of the hand in pixels
        time:   Integer from 0 to 59, corresponding to valid points on clock
        image:  Image file to draw on to

    """
    draw = ImageDraw.Draw(image)
    time_offset = time - 15
    outer_x = math.cos(math.radians(6 * time_offset)) * length + center[0]
    outer_y = math.sin(math.radians(6 * time_offset)) * length + center[1]

    diamond_left_x = math.cos(math.radians(6 * time_offset - 4)) * (length - 4) + center[0]
    diamond_left_y = math.sin(math.radians(6 * time_offset - 4)) * (length - 4) + center[1]

    diamond_right_x = math.cos(math.radians(6 * time_offset + 4)) * (length - 4) + center[0]
    diamond_right_y = math.sin(math.radians(6 * time_offset + 4)) * (length - 4) + center[1]

    inner_x = math.cos(math.radians(6 * time_offset)) * (length - 8) + center[0]
    inner_y = math.sin(math.radians(6 * time_offset)) * (length - 8) + center[1]

    draw.line([(center[0], center[1]), (outer_x, outer_y)], fill=1)
    draw.polygon(
        [(outer_x, outer_y), (diamond_right_x, diamond_right_y), (inner_x, inner_y), (diamond_left_x, diamond_left_y),],
        fill=2,
        outline=1,
    )


def draw_simple_hand(center: Tuple[int, int], length: int, time: int, color: int, image: Image) -> None:
    """Draw a simple hand of a given length and color on the image.

    Args:
        center: Center point of the clock face
        length: The length of the hand in pixels
        time:   Integer from 0 to 59 corresponding to valid points on clock
        image:  Image file to draw on to

    """
    draw = ImageDraw.Draw(image)
    time_offset = time - 15

    outer_x = math.cos(math.radians(6 * time_offset)) * length + center[0]
    outer_y = math.sin(math.radians(6 * time_offset)) * length + center[1]

    draw.line([(center[0], center[1]), (outer_x, outer_y)], fill=color)


def draw_face(center: Tuple[int, int], radius: int, image: Image) -> None:
    """Draw the face of the clock.

    Args:
        center: Center point of the clock face
        radius: Radius of the clock face
        image:  Image to draw on to

    """
    draw = ImageDraw.Draw(image)
    ir = radius - radius / 10
    med = radius + 4

    draw.ellipse(
        [(center[0] - med, center[1] - med), (center[0] + med, center[1] + med)], outline=1, width=2,
    )

    for r in range(12):
        if not r % 3:
            pass
        else:
            base_x = math.cos((r * math.pi) / 6)
            base_y = math.sin((r * math.pi) / 6)
            draw.line(
                [
                    (base_x * ir + center[0], base_y * ir + center[1]),
                    (base_x * radius + center[0], base_y * radius + center[1]),
                ],
                fill=1,
            )

    for r in range(4):
        base_x = math.cos((r * math.pi) / 2)
        base_y = math.sin((r * math.pi) / 2)
        draw.line(
            [
                (base_x * ir + center[0], base_y * ir + center[1]),
                (base_x * radius + center[0], base_y * radius + center[1]),
            ],
            fill=1,
            width=3,
        )
        draw.line(
            [
                (base_x * (ir + 1) + center[0], base_y * (ir + 1) + center[1]),
                (base_x * (radius - 1) + center[0], base_y * (radius - 1) + center[1]),
            ],
            fill=2,
        )


def draw_pin(center: Tuple[int, int], radius: int, image: Image) -> None:
    """Draw the center pin the hands attach to.

    Args:
        center: Center point of the pin
        radius: Radius of the pin
        image:  Image to draw on to

    """
    draw = ImageDraw.Draw(image)
    draw.ellipse(
        [(center[0] - radius, center[1] - radius), (center[0] + radius, center[1] + radius),], outline=1, fill=2,
    )


def draw_date(now: time.struct_time, image: Image, size: int = 16) -> None:
    """Draw date information to the screen.

    Args:
        now:   Struct_time with time to display
        image: Image to draw to
        size:  Font size of the date

    """
    font = ImageFont.truetype("resources/alagard.ttf", size=size)
    draw = ImageDraw.Draw(image)
    draw.text((4, 4), time.strftime("%b %d\n%a\n%Y"), font=font, fill=1)


def draw_weather(image: Image, size: int = 16) -> None:
    """Draw some local weather information to the screen.

    Args:
        image: The image to draw to

    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Input values:\nImage:\t{image}\nSize:\t{size}")
    try:
        with open("forecast.json", "r") as infile:
            forecast = json.load(infile)
    except FileNotFoundError:
        logger.error("No forecast data found in directory.")
        return

    logger.debug(f"Forecast JSON loaded:\n{pprint.pformat(forecast)}")
    now = forecast["currently"]
    draw.ImageDraw.Draw(image)
    font = ImageFont.truetype("resources/alagard.ttf", size=size)
    tw, th = draw.textsize(now["temperature"], font)
    atw, ath = draw.textsize(now["apparentTemperature"], font)
    ww, wh = draw.textsize(now["summary"], font)
    wl = max(128, 212 - ww)
    logger.debug(f"Calculated text variables:\n"
                 f"Temp width, height: {tw}, {th}\n"
                 f"Apparent temp width, height: {atw}, {ath}\n"
                 f"Weather width, height: {ww}, {wh}\n"
                 f"Weather left edge: {wl}"
    )
    draw.text((wl, 4), now["summary"], font=font, fill=1, align="right")
    draw.text((212 - tw, 20), now["temperature"], font=font, fill=1, align="right")
    draw.text((212 - atw, 36), now["apparentTemperature"], font=font, fill=1, align="right")

    icons = {
        "overcast": "cloud",
        "flurries": "snow",
        "snow": "snow",
        "sunny": "sun",
        "cloudy": "cloud",
        "drizzle": "rain",
        "rain": "rain",
        "windy": "wind",
    }

    try:
        weather_icon = icons[now["summary"]]
    except Exception:
        pass
    else:
        weather_image = Image.open(f"resources/icon-{weather_icon}.png")
        image.paste(weather_image, (212 - weather_image.height, 104 - weather_image.width), create_mask(weather_image))


def create_mask(source: Image, mask: Tuple[int, int, int] = (0, 1, 2)) -> Image:
    """Create an image mask for pasting purposes.

    Args:
        source: Image to create the mask from
        mask:   Tuple containing colormap indices to be masked

    Returns:
        An image mask for the source image

    Attribution:
        Written by folks at Pimoroni

    """
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)
    return mask_image


if __name__ == "__main__":
    palette = 3 * [255]
    palette += 3 * [0]
    palette += [166, 152, 1]
    palette += 759 * [0]

    clock_center = 90

    img = Image.new("P", (212, 104), color=0)

    draw_face((clock_center, 52), 46, img)

    now = time.localtime(time.time())
    minute = now.tm_min
    hour = ((now.tm_hour % 12) + (minute / 60)) * 5
    draw_fancy_hand((clock_center, 52), 46, minute, img)
    draw_fancy_hand((clock_center, 52), 30, hour, img)

    # second = now.tm_sec
    second = randint(0, 59)
    while (second == minute) or (second == hour):
        second = randint(0, 59)

    draw_simple_hand((clock_center, 52), 42, second, 2, img)

    draw_pin((clock_center, 52), 2, img)

    draw_date(now, img)

    draw_weather(img)

    img.putpalette(palette)
    img.save("analog.png")
    try:
        from inky import InkyPHAT  # type: ignore
    except RuntimeError:
        pass
    except ModuleNotFoundError:
        pass
    else:
        inky_display = InkyPHAT("yellow")
        inky_display.set_image(img.rotate(180))
        inky_display.set_border(inky_display.BLACK)
        inky_display.show()
