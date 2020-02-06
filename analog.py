#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Display an analog clock face on an inky display."""

from PIL import Image, ImageDraw, ImageFont  # type: ignore
from typing import Tuple
import math
import time
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
    draw.polygon([(outer_x, outer_y), (diamond_right_x, diamond_right_y),
                  (inner_x, inner_y), (diamond_left_x, diamond_left_y)], fill=2, outline=1)


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

    draw.ellipse([(center[0] - med, center[1] - med), (center[0] + med, center[1] + med)], outline=1, width=2)

    for r in range(12):
        if not r % 3:
            pass
        else:
            base_x = math.cos((r * math.pi) / 6)
            base_y = math.sin((r * math.pi) / 6)
            draw.line([(base_x * ir + center[0], base_y * ir + center[1]),
                       (base_x * radius + center[0], base_y * radius + center[1])], fill=1)

    for r in range(4):
        base_x = math.cos((r * math.pi) / 2)
        base_y = math.sin((r * math.pi) / 2)
        draw.line([(base_x * ir + center[0], base_y * ir + center[1]),
                   (base_x * radius + center[0], base_y * radius + center[1])], fill=1, width=3)
        draw.line([(base_x * (ir + 1) + center[0], base_y * (ir + 1) + center[1]),
                   (base_x * (radius - 1) + center[0], base_y * (radius - 1) + center[1])], fill=2)


def draw_pin(center: Tuple[int, int], radius: int, image: Image) -> None:
    """Draw the center pin the hands attach to.

    Args:
        center: Center point of the pin
        radius: Radius of the pin
        image:  Image to draw on to

    """
    draw = ImageDraw.Draw(image)
    draw.ellipse([(center[0] - radius, center[1] - radius), (center[0] + radius, center[1] + radius)],
                 outline=1, fill=2)


def draw_date(x: int, y: int, now: time.struct_time, image: Image, size: int = 10) -> None:
    """Draw date information to the screen.

    Args:
        x:     X of top left corner of date
        y:     Y of top left corner of date
        size:  Font size of the date
        image: Image to draw to

    """
    font = ImageFont.truetype('resources/alagard.ttf', size=size)
    draw = ImageDraw.Draw(image)
    datestring = time.strftime('%a %d\n%b %y')
    draw.text((x, y), datestring, font=font, fill=1)


if __name__ == '__main__':
    palette = 3 * [255]
    palette += 3 * [0]
    palette += [166, 152, 1]
    palette += 759 * [0]

    img = Image.new("P", (212, 104), color=0)

    draw_face((106, 52), 46, img)

    now = time.localtime(time.time())
    minute = now.tm_min
    hour = ((now.tm_hour % 12) + (minute / 60)) * 5
    draw_fancy_hand((106, 52), 46, minute, img)
    draw_fancy_hand((106, 52), 30, hour, img)

    # second = now.tm_sec
    second = randint(0, 59)
    while((second == minute) or (second == hour)):
        second = randint(0, 59)

    draw_simple_hand((106, 52), 42, second, 2, img)

    draw_pin((106, 52), 2, img)

    draw_date(6, 6, now, img, 16)

    img.putpalette(palette)
    img.save('analog.png')
    try:
        from inky import InkyPHAT  # type: ignore
    except RuntimeError:
        pass
    except ModuleNotFoundError:
        pass
    else:
        inky_display = InkyPHAT('yellow')
        img.rotate(180)
        inky_display.set_image(img)
        inky_display.set_border(inky_display.BLACK)
        inky_display.show()
