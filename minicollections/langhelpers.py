from prestring.python import PythonModule
import logging
logger = logging.getLogger(__name__)


def as_python_code(fn):
    def wrapper(name, *args, **kwargs):
        m = PythonModule()
        fn(m, name, *args, **kwargs)
        # activate python code
        env = {}
        exec(str(m), globals(), env)
        return env[name]
    return wrapper
