# flake8: noqa
from .Image import Image
from .ImageFont import ImageFont
from typing import Sequence, Tuple, Union, Optional

class ImageDraw:
    def __init__(self) -> None: ...
    def ellipse(
        self,
        xy: Union[Sequence[Union[Tuple[float, float], Tuple[int, int]]], Sequence[Union[int, float]]],
        fill: Optional[int] = None,
        outline: Optional[int] = None,
        width: int = 1,
    ) -> None: ...
    def line(
        self,
        xy: Union[Sequence[Union[Tuple[int, int], Tuple[float, float]]], Sequence[Union[int, float]]],
        fill: Optional[int] = None,
        width: int = 0,
        joint: Optional[str] = None,
    ) -> None: ...
    def polygon(
        self,
        xy: Union[Sequence[Union[Tuple[int, int], Tuple[float, float]]], Sequence[Union[int, float]]],
        fill: Optional[int] = None,
        outline: Optional[int] = None,
        width: int = 1,
    ) -> None: ...
    def regular_polygon(
        self,
        bounding_circle: Union[
            Tuple[int, int, int],
            Tuple[float, float, float],
            Tuple[Tuple[int, int], int],
            Tuple[Tuple[float, float], float],
        ],
        n_sides: int,
        rotation: Union[int, float] = 0,
        fill: Optional[int] = None,
        outline: Optional[int] = None,
    ) -> None: ...
    def text(
        self,
        xy: Union[Tuple[int, int], Tuple[float, float]],
        text: str,
        font: Optional[ImageFont] = None,
        fill: Optional[int] = None,
        align: Optional[str] = "left",
    ) -> None: ...
    def rectangle(
        self,
        xy: Union[Sequence[Union[Tuple[int, int], Tuple[float, float]]], Sequence[Union[int, float]]],
        fill: Optional[int] = None,
        outline: Optional[int] = None,
        width: int = 1,
    ) -> None: ...
    def rounded_rectangle(
        self,
        xy: Union[Sequence[Union[Tuple[int, int], Tuple[float, float]]], Sequence[Union[int, float]]],
        radius: int = 0,
        fill: Optional[int] = None,
        outline: Optional[int] = None,
        width: int = 1,
    ) -> None: ...
    def textsize(self, text: str, font: Optional[ImageFont] = None) -> Tuple[int, int]: ...

def Draw(im: Image) -> ImageDraw: ...
