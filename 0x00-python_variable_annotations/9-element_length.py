#!/usr/bin/env python3
""" Function's parameters """

from typing import Iterable, List, Sequence, Tuple

def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Return list of tuples, one tuple for each element of lst,
        each tuple containing the element and its length.
    """
    return [(i, len(i)) for i in lst]