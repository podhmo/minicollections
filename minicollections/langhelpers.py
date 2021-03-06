from prestring.python import PythonModule
import functools
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


# stolen from pyramid.decorators
class reify(object):
    """ Use as a class method decorator.  It operates almost exactly like the
    Python ``@property`` decorator, but it puts the result of the method it
    decorates into the instance dict after the first call, effectively
    replacing the function it decorates with an instance variable.  It is, in
    Python parlance, a non-data descriptor.  An example:

    .. code-block:: python

       class Foo(object):
           @reify
           def jammy(self):
               print('jammy called')
               return 1

    And usage of Foo:

    >>> f = Foo()
    >>> v = f.jammy
    'jammy called'
    >>> print(v)
    1
    >>> f.jammy
    1
    >>> # jammy func not called the second time; it replaced itself with 1
    """
    def __init__(self, wrapped):
        self.wrapped = wrapped
        functools.update_wrapper(self, wrapped)

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val
