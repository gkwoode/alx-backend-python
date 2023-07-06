#!/usr/bin/env pyton3
""" Type Checking """

from typing import Tuple, Any

def zoom_array(lst: Tuple[Any, ...], factor: int = 2) -> Tuple[Any, ...]:
    zoomed_in: Tuple[Any, ...] = [
        item for item in lst
        for i in range(factor)
    ]
    return tuple(zoomed_in)


array = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)