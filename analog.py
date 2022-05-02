#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Display an analog clock face on an inky display."""

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Union, Optional, Literal
from utils.utils import clamp
import math
import time
import json
import pprint
from random import randint
import logging


_FACE_MODE = Literal["simple", "fancy", "numbered"]
_HANDS_MODE = Literal["simple", "fancy"]


class Clock(object):
    """An object representing an Analog Clock for drawing purposes.

    :param int radius: Radius of the clock face
    :param face:
        The style to use for the clock face (backplate).
        Can be "simple", "fancy", or "numbered".
        Defaults to "fancy".
    :type face: str, optional
    :param hands:
        The style to use for the clock hands.
        Can be "simple" or "fancy".
        Defaults to "fancy".
    :type hands: str, optional
    :param hand_count:
        The number of hands to draw from 0 to 3.
        Hands are drawn in order from hour to minute to second.
        Defaults to 3, input out of range will be clamped.
    :type hand_count: int, optional

    :raises ValueError: if the value for face or hands is invalid.
    """

    def __init__(
        self, radius: int, *, face: _FACE_MODE = "fancy", hands: _HANDS_MODE = "fancy", hand_count: int = 3
    ) -> None:
        super(Clock, self).__init__()

        self.__radius = radius
        self.__diameter = radius * 2
        self.__center = (radius, radius)

        self.__image: Image.Image
        self.__image_draw: ImageDraw.ImageDraw
        self.__manual: bool
        self.__time: time.struct_time

        if face not in ("simple", "fancy", "numbered"):
            raise ValueError('face must be "simple", "fancy", or "numbered"')
        if hands not in ("simple", "fancy"):
            raise ValueError('hands must be "simple" or "fancy"')

        self.__face = face
        self.__hands = hands
        self.__hand_count = clamp(hand_count, 0, 3)

        self.__logger = logging.getLogger(__name__)
        self.__logger.debug(self.__dict__)

    def __repr__(self) -> str:
        return f"Clock(radius={self.__radius})"

    def _draw(self) -> None:
        self.__image = Image.new("P", (self.__diameter, self.__diameter))
        self.__image_draw = ImageDraw.Draw(self.__image)

        self._draw_face()
        self._draw_hands()

    def _draw_face(self) -> None:
        self.__image_draw.ellipse([(0, 0), (self.__diameter, self.__diameter)], outline=1, width=2)

        if self.__face == "fancy":
            pass

        if self.__face == "numbered":
            raise NotImplementedError("Numerical faceplate not yet supported.")

    def _draw_hands(self) -> None:
        pass

    def _update_time(self) -> None:
        self.__time = time.localtime(time.time())

    def set_fixed_time(self, fixed_time: time.struct_time) -> None:
        """Set a fixed time to use for this clock.

        :param fixed_time:
            A fixed time to use for this clock.
            This will prevent the clock from updating to localtime whenever redrawn.
        :type time: time.struct_time
        """
        self.__manual = True
        self.__time = fixed_time

    def unset_fixed_time(self) -> None:
        """Unset the clock's fixed time, allowing it to update to localtime again."""
        self.__manual = False

    def set_style(
        self,
        *,
        face: Optional[_FACE_MODE] = None,
        hands: Optional[_HANDS_MODE] = None,
        hand_count: Optional[int] = None,
    ) -> None:
        """Modify style settings for the clock.

        :param face:
            The style to use for the clock face (backplate).
            Can be "simple", "fancy", or "numbered".
            Defaults to "fancy".
        :type face: str, optional
        :param hands:
            The style to use for the clock hands.
            Can be "simple" or "fancy".
            Defaults to "fancy".
        :type hands: str, optional
        :param hand_count:
            The number of hands to draw from 0 to 3.
            Hands are drawn in order from hour to minute to second.
            Defaults to 3, input out of range will be clamped.
        :type hand_count: int, optional
        """
        if face is not None:
            self.__face = face
        if hands is not None:
            self.__hands = hands
        if hand_count is not None:
            self.__hand_count = clamp(hand_count, 0, 3)

    def get_image(self) -> Image.Image:
        """Update the clock image if a fixed time has not been set, and return the image.

        :return: Image containing the freshly redrawn clock.
        :rtype: PIL.Image.Image
        """
        if not self.__manual:
            self._update_time()
        self._draw()
        return self.__image


def draw_fancy_hand(center: Tuple[int, int], length: int, time: Union[int, float], image: Image.Image) -> None:
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
        [(outer_x, outer_y), (diamond_right_x, diamond_right_y), (inner_x, inner_y), (diamond_left_x, diamond_left_y)],
        fill=2,
        outline=1,
    )


def draw_simple_hand(center: Tuple[int, int], length: int, time: int, color: int, image: Image.Image) -> None:
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


def draw_face(center: Tuple[int, int], radius: int, image: Image.Image) -> None:
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
        if not r % 3:  # Skip the fancier divisions to avoid redraws
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

    for r in range(4):  # 3, 6, 9, 12 - Draw the fancier divisions
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


def draw_pin(center: Tuple[int, int], radius: int, image: Image.Image) -> None:
    """Draw the center pin the hands attach to.

    Args:
        center: Center point of the pin
        radius: Radius of the pin
        image:  Image to draw on to

    """
    draw = ImageDraw.Draw(image)
    draw.ellipse(
        [(center[0] - radius, center[1] - radius), (center[0] + radius, center[1] + radius)], outline=1, fill=2
    )


def draw_date(now: time.struct_time, image: Image.Image, size: int = 16) -> None:
    """Draw date information to the screen.

    Args:
        now:   Struct_time with time to display
        image: Image to draw to
        size:  Font size of the date

    """
    font = ImageFont.truetype("resources/alagard.ttf", size=size)
    draw = ImageDraw.Draw(image)
    draw.text((4, 4), time.strftime("%b %d\n%a\n%Y"), font=font, fill=1)


def draw_weather(image: Image.Image, size: int = 16) -> None:
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
