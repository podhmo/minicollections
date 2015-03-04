# -*- coding:utf-8 -*-
from evilunit import test_target
import unittest


@test_target("minicollections:valueobject")
class Tests(unittest.TestCase):
    def _makeOne(self, *args, **kwargs):
        Factory = self._getTarget()
        return Factory("Person", [("name", str, None), ("age", int, 0)])

    def test_construct_by_args(self):
        person = self._makeOne()("foo", "20")
        self.assertEqual(person.name, "foo")
        self.assertEqual(person.age, 20)

    def test_construct_by_kwargs(self):
        person = self._makeOne()(name="foo", age="20")
        self.assertEqual(person.name, "foo")
        self.assertEqual(person.age, 20)

    def test_construct_by_defaults(self):
        person = self._makeOne()()
        self.assertEqual(person.name, None)
        self.assertEqual(person.age, 0)

    def test_attributes_limit_via_slots(self):
        person = self._makeOne()()
        with self.assertRaises(AttributeError):
            person.x = 10

    def test_equal_by_value(self):
        Person = self._makeOne()
        person = Person(name="foo", age="20")
        person2 = Person(name="foo", age="20")
        self.assertEqual(person, person2)

    def test_not_equal_by_superclass(self):
        Person = self._makeOne()
        person = Person(name="foo", age="20")

        class Person2(Person):
            pass

        person2 = Person2(name="foo", age="20")
        self.assertNotEqual(person2, person)

    def test_not_equal_by_subclass(self):
        Person = self._makeOne()
        person = Person(name="foo", age="20")

        class Person2(Person):
            pass

        person2 = Person2(name="foo", age="20")
        self.assertNotEqual(person, person2)

    def test_hash(self):
        person = self._makeOne()()
        self.assertEqual(hash(person), hash(person))

    def test_hash2(self):
        person = self._makeOne()(name="foo", age="20")
        person2 = self._makeOne()(name="foo", age="20")
        self.assertEqual(hash(person), hash(person2))

    def test_order(self):
        person = self._makeOne()(name="foo", age="20")
        person2 = self._makeOne()(name="boo", age="20")
        self.assertTrue(person > person2)

    def test_order2(self):
        person = self._makeOne()(name="foo", age="20")
        person2 = self._makeOne()(name="foo", age="30")
        self.assertTrue(person < person2)
