# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from .langhelpers import as_python_code
from functools import partial
from collections import namedtuple


def tagged_tuple(name, attributes):
    """like a collections.namedtuple. but, tagged"""
    C = namedtuple(name, "{} {}".format(name, attributes))
    return partial(C, name)

