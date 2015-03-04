# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from .langhelpers import as_python_code, reify
from functools import partial, total_ordering
from collections import namedtuple


def tagged_tuple(name, attributes):
    """like a collections.namedtuple. but, tagged"""
    C = namedtuple(name, "{} {}".format(name, attributes))
    return partial(C, name)


@as_python_code
def value_object(m, name, triples):
    """
    syntax sugar, define a class, like this.
    * triples = [(attrname, convertor, default_value)]
    * convertor :: a -> b
    """

    names = [tri[0] for tri in triples]
    m.from_("functools", "total_ordering")

    m.stmt("@total_ordering")
    with m.class_(name):
        with m.method("__init__", ", ".join("{}=None".format(name) for name in names)):
            for name, convertor, default in triples:
                if convertor is None:
                    fmt = "self.{name} = {name} or {default!r}"
                else:
                    fmt = "self.{name} = {convertor}({name}) if {name} else {default!r}"
                m.stmt(fmt.format(name=name, convertor=convertor.__name__, default=default))

        m.stmt("__slots__ = ({})", ", ".join(repr(name) for name in names))

        with m.method("__hash__"):
            m.return_("hash('@'.join(map(repr, ({}))))".format(", ".join("self.{}".format(name) for name in names)))

        with m.method("__gt__", "other"):
            for name in names:
                with m.if_("self.{name} > other.{name}".format(name=name)):
                    m.return_("True")
            m.return_("False")

        with m.method("__eq__", "other"):
            with m.if_("not isinstance(other, self.__class__)"):
                    m.return_("False")
            for name in names:
                with m.if_("self.{name} != other.{name}".format(name=name)):
                    m.return_("False")
            m.return_("True")

        with m.method("__repr__"):
            m.stmt("name = self.__class__.__name__")
            args = ", ".join("{name}={{self.{name}!r}}".format(name=name) for name in names)
            m.return_("'{{}}({})'.format(name, self=self)".format(args))
    return m
