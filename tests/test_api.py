from python_dag.api import (
    Component, resolve_connections, UnboundMethodError, UnresolvedArgumentError
)


def test_without_arguments():

    def x():
        return 1

    x_component = Component(x)
    assert x_component.process() == 1


def test_with_arguments():

    def add(x, y):
        return x + y

    def x():
        return 1

    x_component = Component(x)
    add_component = Component(add)
    connections = [
        (x_component, add_component, "x"),
        (x_component, add_component, "y"),
    ]

    resolve_connections(connections)
    assert add_component.process() == 2


def test_unresolved_argument():

    def x(x):
        return x

    x_component = Component(x)
    try:
        x_component.process()
    except UnresolvedArgumentError:
        pass


def test_nested_connections():

    def add(x, y):
        return x + y

    def x():
        return 1

    x_component = Component(x)
    add1_component = Component(add)
    add2_component = Component(add)
    connections = [
        (x_component, add1_component, "x"),
        (x_component, add1_component, "y"),
        (add1_component, add2_component, "x"),
        (add1_component, add2_component, "y"),
    ]

    resolve_connections(connections)
    assert add2_component.process() == 4


def test_single_keyword_arguments():

    def add(x, y=1):
        return x + y

    def x():
        return 1

    x_component = Component(x)
    add_component = Component(add)
    connections = [
        (x_component, add_component, "x"),
    ]

    resolve_connections(connections)
    assert add_component.process() == 2


def test_multiple_keyword_arguments():

    def add(x=2, y=1):
        return x + y

    add_component = Component(add)
    assert add_component.process() == 3


def test_override_single_keyword_argument():

    def add(x, y=0):
        return x + y

    def x():
        return 1

    x_component = Component(x)
    add_component = Component(add)
    connections = [
        (x_component, add_component, "x"),
        (x_component, add_component, "y"),
    ]

    resolve_connections(connections)
    assert add_component.process() == 2


def test_override_multiple_keyword_arguments():

    def add(x=0, y=0):
        return x + y

    def x():
        return 1

    x_component = Component(x)
    add_component = Component(add)
    connections = [
        (x_component, add_component, "x"),
        (x_component, add_component, "y"),
    ]

    resolve_connections(connections)
    assert add_component.process() == 2


def test_class_method():

    class add(object):

        y = 1

        def adding(self, x):
            return x + self.y

    def x():
        return 1

    x_component = Component(x)
    add_component = Component(add().adding)
    connections = [
        (x_component, add_component, "x")
    ]

    resolve_connections(connections)
    assert add_component.process() == 2


def test_unbound_class_method():

    class add(object):

        y = 1

        def adding(self, x):
            return x + self.y

    try:
        Component(add.adding)
    except UnboundMethodError:
        pass


def test_override_class_attribute():

    class add(object):

        y = 1

        def adding(self, x):
            return x + self.y

    add_cls = add()
    add_cls.y = 2

    def x():
        return 1

    x_component = Component(x)
    add_component = Component(add_cls.adding)
    connections = [
        (x_component, add_component, "x")
    ]

    resolve_connections(connections)
    assert add_component.process() == 3


def test_unknown_arguments():

    def add(*args):
        return sum(args)

    def x():
        return 1

    x_component = Component(x)
    add_component = Component(add)
    connections = [
        (x_component, add_component, "args"),
        (x_component, add_component, "args"),
    ]

    resolve_connections(connections)
    assert add_component.process() == 2


def test_unknown_keyword_arguments():

    def add(**kwargs):
        return sum(kwargs.values())

    def x():
        return 1

    x_component = Component(x)
    add_component = Component(add)
    connections = [
        (x_component, add_component, "kwargs"),
        (x_component, add_component, "kwargs"),
        (x_component, add_component, "kwargs"),
    ]

    resolve_connections(connections)
    assert add_component.process() == 3
