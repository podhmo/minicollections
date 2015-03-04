# -*- coding:utf-8 -*-
from evilunit import test_target
import unittest


@test_target("minicollections:taggedtuple")
class Tests(unittest.TestCase):
    def test_prepare_named_tuple_is_just_tuple(self):
        from collections import namedtuple
        A = namedtuple("A", "name value")
        B = namedtuple("B", "name value")
        self.assertEqual(A("foo", 20), B("foo", 20))

    def test_with_type(self):
        A = self._makeOne("A", "name value")
        B = self._makeOne("B", "name value")
        self.assertNotEqual(A("foo", 20), B("foo", 20))

    def test_but_accessor_is_valueless(self):
        A = self._makeOne("A", "name value")
        B = self._makeOne("A", "name point")
        self.assertEqual(A("foo", 20), B("foo", 20))
