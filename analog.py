#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Display an analog clock face on an inky display."""

from PIL import Image, ImageDraw, ImagePalette  # type: ignore
from typing import Tuple


def get_time() -> None:
    """Fetch the current system time."""
    pass


def draw_hand(length: int, angle: float, center: Tuple[int, int], image: Image) -> None:
    """Draw a hand of given length on the image.

    Args:
        length: The length of the hand in pixels
        angle:  Angle to rotate the hand by
        center: Center point of the clock face
        image:  Image file to draw on to

    """
    draw = ImageDraw.Draw(image)
    draw.line((center[0], center[1], 104, 52), 1) 


if __name__ == '__main__':
    palette = 768 * [0]
    palette[0] = 255
    palette[1] = 255
    palette[2] = 255
    palette[6] = 255
    img = Image.new("P", (212, 104), color=0)
    draw_hand(52, 0.0, (52, 52), img)
    img.putpalette(palette)
    img.save('analog.png')
