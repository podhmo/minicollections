# -*- coding:utf-8 -*-
import logging
from minicollections import valueobject
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)
Person = valueobject("Person", [("name", str, "foo"), ("age", int, 0)])
Berson = valueobject("Berson", [("name", str, "foo"), ("age", int, 0)])


class SuperPerson(Person):
    pass


assert Person("foo", "20") == Person("foo", "20")
assert Person("foo", "20") != Berson("foo", "20")
assert SuperPerson("foo", "20") == Person("foo", "20")
assert Person("foo", "20") == SuperPerson("foo", "20")

Person = valueobject("Person", [("name", str, "foo"), ("age", int, 0)])
"""
@total_ordering
class Person(object):
    def __init__(self, name=None, age=None):
        self.name = str(name) if name else 'foo'
        self.age = int(age) if age else 0

    __slots__ = ('name', 'age')

    def __hash__(self):
        return hash('@'.join(map(repr, (self.name, self.age))))

    def __gt__(self, other):
        if self.name > other.name:
            return True
        if self.age > other.age:
            return True
        return False

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.name != other.name:
            return False
        if self.age != other.age:
            return False
        return True

    def __repr__(self):
        name = self.__class__.__name__
        return '{}(name={self.name!r}, age={self.age!r})'.format(name, self=self)
"""
