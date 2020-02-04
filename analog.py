#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Display an analog clock face on an inky display."""

from PIL import Image, ImageDraw  # type: ignore
from typing import Tuple


def get_time() -> None:
    """Fetch the current system time."""
    pass


def draw_hand(length: int, angle: float, center: Tuple[int, int], image: Image) -> None:
    """Draw a hand of given length on the image.

    Args:
        length: The length of the hand in pixels
        angle:  Angle to rotate the hand by in radians
        center: Center point of the clock face
        image:  Image file to draw on to

    Todo:
        Fancier hand display

    """
    draw = ImageDraw.Draw(image)
    draw.line((center[0], center[1], 104, 52), 1)


if __name__ == '__main__':
    palette = 3 * [255]
    palette += 3 * [0]
    palette += [166, 152, 1]
    palette += 759 * [0]

    img = Image.new("P", (212, 104), color=0)
    draw_hand(52, 0.0, (52, 52), img)
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
        inky_display.show()
