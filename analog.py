#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Display an analog clock face on an inky display."""

from PIL import Image, ImageDraw  # type: ignore
from typing import Tuple
import math
import time


def get_time() -> None:
    """Fetch the current system time."""
    pass


def draw_hand(center: Tuple[int, int], length: int, time: int, image: Image) -> None:
    """Draw a hand of given length on the image.

    Args:
        center: Center point of the clock face
        length: The length of the hand in pixels
        time:   Integer from 0 to 59, corresponding to valid points on clock
        image:  Image file to draw on to

    Todo:
        Fancier hand display

    """
    draw = ImageDraw.Draw(image)
    time_offset = time - 15
    outer_x = math.cos(math.radians(6 * time_offset)) * length + center[0]
    outer_y = math.sin(math.radians(6 * time_offset)) * length + center[1]
    draw.line([(center[0], center[1]), (outer_x, outer_y)], fill=1)


def draw_face(center: Tuple[int, int], radius: int, image: Image) -> None:
    """Draw the face of the clock.

    Args:
        center: Center point of the clock face
        image:  Image to draw on to

    """
    draw = ImageDraw.Draw(image)
    ir = radius - round(radius / 10)

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


if __name__ == '__main__':
    palette = 3 * [255]
    palette += 3 * [0]
    palette += [166, 152, 1]
    palette += 759 * [0]

    img = Image.new("P", (212, 104), color=0)

    now = time.localtime(time.time())
    hour = (now.tm_hour % 12) * 5
    minute = now.tm_min
    draw_hand((52, 52), 48, minute, img)
    draw_hand((52, 52), 24, hour, img)

    draw_face((52, 52), 50, img)
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
        inky_display.set_image(img)
        inky_display.set_border(inky_display.BLACK)
        inky_display.show()
