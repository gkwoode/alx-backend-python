#!/usr/bin/env python3
""" Basic annotations - to_kv """
  
from typing import Union, Tuple

def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ Return tuple of string and float """
    return (k, float(v ** 2))