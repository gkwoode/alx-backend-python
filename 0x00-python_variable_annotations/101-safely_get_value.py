#!/usr/bin/env python3
""" Type annotations """

def safely_get_value(dct: dict, key: str, default: str = None) -> str:
    """ Return value of key if it exists, otherwise return default """
    if key in dct:
        return dct[key]
    else:
        return default