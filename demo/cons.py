# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from minicollections import sumtype

_, Cons, Nil = sumtype("_Cons", [
    ("Cons", [("car", None), ("cdr", None)]),
    ("Nil", [])
])
print(Cons(1, 2))
print(Cons(car=1, cdr=Cons(car=2, cdr=Nil())))


@Cons.match
class match(object):
    @staticmethod
    def Cons(o):
        return "cons"

    @staticmethod
    def Nil(o):
        return "nil"

print(Nil.__name__)
print(match(Nil()))

"""
class _Cons(object):
    def is_same_group(self, other):
        return isinstance(other, _Cons)

    @classmethod
    def match(cls, dispatch_class):
        def _match(ob, *args, **kwargs):
            if ob.__class__.__name__ == 'Cons':
                return dispatch_class.Cons(ob, *args, **kwargs)
            if ob.__class__.__name__ == 'Nil':
                return dispatch_class.Nil(ob, *args, **kwargs)
            else:
                raise Exception('dispatch error {!r}() is not supported'.format(ob.__class__.__name__))

        assert hasattr(dispatch_class, 'Cons')
        assert hasattr(dispatch_class, 'Nil')
        return _match



class Cons(_Cons):
    def __init__(self, car=None, cdr=None):
        self.car = car
        self.cdr = cdr

    __slots__ = ('car', 'cdr')
    def __repr__(self):
        name = self.__class__.__name__
        return '<{} car={self.car!r}, cdr={self.cdr!r} at {id}>'.format(name, self=self, id=hex(id(self)))



class Nil(_Cons):
    def __repr__(self):
        name = self.__class__.__name__
        return '<{}  at {id}>'.format(name, self=self, id=hex(id(self)))
"""
