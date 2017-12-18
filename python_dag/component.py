import inspect

from error import UnboundMethodError, UnresolvedArgumentError


class UnresolvedArgument(object):
    pass


class Component(object):

    def __init__(self, method):
        self.method = method

        # Class methods validation
        if hasattr(method, "im_self"):
            if method.im_self is None:
                raise UnboundMethodError("Class methods needs to be bound.")

        # Get arguments
        args = inspect.getargspec(self.method).args
        kwargs = self.get_keyword_arguments(method).keys()
        arguments = [x for x in args if x not in kwargs]

        # Assign arguments
        self.arguments = {}

        for arg in arguments:
            # Ignore "self" argument of class methods
            if arg == "self":
                continue

            self.arguments[arg] = UnresolvedArgument()

        # Assign keyword arguments
        self.keyword_arguments = {}

        for arg in self.get_keyword_arguments(self.method).keys():
            self.keyword_arguments[arg] = UnresolvedArgument()

    def __str__(self):
        return "<class Component '{0}'>".format(self.method)

    def process(self):

        # Validate all arguments are resolved.
        arguments = []
        for key, value in self.arguments.iteritems():
            if isinstance(value, UnresolvedArgument):
                raise UnresolvedArgumentError(
                    "Argument \"{0}\" could not be resolved on Component "
                    "{1}".format(key, self)
                )
            else:
                arguments.append(value())

        # Get default value for keyword arguments unless its a callable.
        # If the keyword argument is callable, then its been resolved.
        keyword_arguments = self.get_keyword_arguments(self.method)
        for key, value in self.keyword_arguments.iteritems():
            if isinstance(value, UnresolvedArgument):
                self.keyword_arguments[key] = keyword_arguments[key]
            if callable(value):
                self.keyword_arguments[key] = value()

        return self.method(*arguments, **self.keyword_arguments)

    def get_keyword_arguments(self, method):

        arguments = inspect.getargspec(method).args
        defaults = inspect.getargspec(method).defaults
        keyword_arguments = {}
        if defaults:
            for arg in arguments[-len(defaults):]:
                keyword_arguments[arg] = defaults[
                    len(keyword_arguments.keys())
                ]

        return keyword_arguments
