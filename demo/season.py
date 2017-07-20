# -*- coding:utf-8 -*-
from prestring.python import PythonModule
import logging
logger = logging.getLogger(__name__)


def as_python_code(fn):
    def wrapper(name, *args, **kwargs):
        m = PythonModule()
        result = fn(m, name, *args, **kwargs)
        code = str(m)
        logger.debug("-- as_python_code --\n%s", code)
        # activate python code
        env = {}
        exec(code, globals(), env)
        if isinstance(result, (list, tuple)):
            class Ref:
                pass
            Ref.__name__ = name
            for k in result:
                setattr(Ref, k, env[k])
            return Ref
        else:
            return env[name]
    return wrapper


@as_python_code
def enum(m, name, values):
    m.from_("enum", "Enum")
    values = [v.strip(" ") for v in values.split(" ")]
    with m.class_(name, "Enum"):
        for i, v in enumerate(values):
            m.stmt("{} = {}".format(v, i))
    return name


Season = enum("Season", "spring summer autum winter")
print(Season.spring)
print(Season.summer)
print(Season.autum)
print(Season.winter)
