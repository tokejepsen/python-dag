import functools
import inspect

from component import Component
from error import UnboundMethodError, UnresolvedArgumentError


def resolve_connections(connections):
    for connection in connections:
        source = connection[0]
        target = connection[1]
        arg = connection[2]

        msg = "{0} is not a Component in connection {1}"
        assert isinstance(source, Component), msg.format(source, connection)
        assert isinstance(target, Component), msg.format(target, connection)

        # Resolve arguments
        if arg in target.arguments.keys():
            target.arguments[arg] = functools.partial(source.process)

        # Resolve keyword arguments
        if arg in target.keyword_arguments.keys():
            target.keyword_arguments[arg] = functools.partial(source.process)

        # Resolve *args
        inspection = inspect.getargspec(target.method)
        if inspection.varargs and arg == inspection.varargs:
            num_args = len(target.arguments.keys())
            arg = "{0}{1}".format(arg, num_args + 1)
            target.arguments[arg] = functools.partial(source.process)

        # Resolve **kwargs
        if inspection.keywords and arg == inspection.keywords:
            num_args = len(target.keyword_arguments.keys())
            arg = "{0}{1}".format(arg, num_args + 1)
            target.keyword_arguments[arg] = functools.partial(source.process)


__all__ = [
    "Component",

    "resolve_connections",

    "UnboundMethodError",
    "UnresolvedArgumentError"
]
