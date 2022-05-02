#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple utility functions for use in other files."""


def clamp(value: int, minimum: int, maximum: int) -> int:
    """
    Clamps a value to the given range.

    :param int input: Value to be clamped.
    :param int minimum: Low end of clamp range.
    :param int maximum: High end of clamp range.

    :return: Clamped value.
    :rtype: int
    """
    return max(minimum, min(value, maximum))
