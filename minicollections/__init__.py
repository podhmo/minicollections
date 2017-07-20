# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from .langhelpers import as_python_code
from functools import partial
from collections import namedtuple


def taggedtuple(name, attributes):
    """like a collections.namedtuple. but, tagged"""
    C = namedtuple(name, "{} {}".format(name, attributes))
    return partial(C, name)


@as_python_code
def producttype(m, name, doubles):
    """
    syntax sugar, define a class, like this.
    * doubles :: [(attrname, convertor)]
    * convertor :: a -> b
    """
    names = [doub[0] for doub in doubles]

    with m.class_(name):
        with m.method("__init__", ", ".join("{}=None".format(name) for name in names)):
            for name, convertor in doubles:
                if convertor is None:
                    fmt = "self.{name} = {name}"
                    m.stmt(fmt.format(name=name))
                else:
                    fmt = "self.{name} = {convertor}({name})"
                    m.stmt(fmt.format(name=name, convertor=convertor.__name__))

        m.stmt("__slots__ = ({})", ", ".join(repr(name) for name in names))

        with m.method("__repr__"):
            m.stmt("name = self.__class__.__name__")
            args = ", ".join("{name}={{self.{name}!r}}".format(name=name) for name in names)
            m.return_("'<{{}}({}) at {{}}>'.format(name, self=self, id=hex(id(self)))".format(args))
    return name


@as_python_code
def sumtype(m, typename, definitions):
    """
    * definitions :: [definition]
    * definition :: [(name, convertor)]
    * convertor :: a -> b
    """
    with m.class_(typename):
        with m.method("is_same_group", "other"):
            m.return_("isinstance(other, {})".format(typename))

        m.stmt("@classmethod")
        with m.def_("match", "cls", "dispatch_class"):
            with m.def_("_match", "ob, *args, **kwargs"):
                for clsname, _ in definitions:
                    # with m.if_("isinstance(ob, {})".format(clsname)):
                    with m.if_("ob.__class__.__name__ == {!r}".format(clsname)):
                        m.return_("dispatch_class.{}(ob, *args, **kwargs)".format(clsname))
                with m.else_():
                    m.stmt(
                        "raise Exception('dispatch error {!r}() is not supported'.format(ob.__class__.__name__))"
                    )
            for clsname, _ in definitions:
                m.stmt("assert hasattr(dispatch_class, {!r})".format(clsname))
            m.return_("_match")

    for clsname, doubles in definitions:
        names = [doub[0] for doub in doubles]

        with m.class_(clsname, typename):
            if names:
                with m.method("__init__", ", ".join("{}=None".format(name) for name in names)):
                    for name, convertor in doubles:
                        if convertor is None:
                            fmt = "self.{name} = {name}"
                            m.stmt(fmt.format(name=name))
                        else:
                            fmt = "self.{name} = {convertor}({name})"
                            m.stmt(fmt.format(name=name, convertor=convertor.__name__))

            if names:
                m.stmt("__slots__ = ({})", ", ".join(repr(name) for name in names))
            with m.method("__repr__"):
                m.stmt("name = self.__class__.__name__")
                args = ", ".join("{name}={{self.{name}!r}}".format(name=name) for name in names)
                m.return_(
                    "'<{{}} {} at {{id}}>'.format(name, self=self, id=hex(id(self)))".format(args)
                )
    return [typename] + [d[0] for d in definitions]


@as_python_code
def valueobject(m, name, triples):
    """
    syntax sugar, define a class, like this.
    * triples :: [(attrname, convertor, default_value)]
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
            if not triples:
                m.stmt("pass")

        m.stmt("__slots__ = ({})", ", ".join(repr(name) for name in names))

        with m.method("__hash__"):
            m.return_(
                "hash('@'.join(map(repr, ({}))))".
                format(", ".join("self.{}".format(name) for name in names))
            )

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
    return name


@as_python_code
def enum(m, name, values):
    m.from_("enum", "Enum")
    values = [v.strip(" ") for v in values.split(" ")]
    with m.class_(name, "Enum"):
        for i, v in enumerate(values):
            m.stmt("{} = {}".format(v, i))
    return name
