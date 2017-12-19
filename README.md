[![Build Status](https://travis-ci.org/tokejepsen/python-dag.svg?branch=travis)](https://travis-ci.org/tokejepsen/python-dag)
[![Build status](https://ci.appveyor.com/api/projects/status/sk4l2b3lqnukbylm?svg=true)](https://ci.appveyor.com/project/tokejepsen/python-dag)

# Goal

Enables users to construct a DAG graph from Python methods.

# Installation

Clone the repository and add to PYTHONPATH:
```
$ git clone https://github.com/tokejepsen/python-dag.git
$ # Windows
$ set PYTHONPATH=%cd%\python-dag
$ # Unix
$ export PYTHONPATH=$(pwd)/python-dag
```

# Usage

In order to process a graph we need to create components and connections.

**Component**

A component wraps a Python method into a reusable instance we can connect to other components. In python-dag everything needs to be a method, and this includes variables:

```python
from python_dag.api import Component

def x():
  return 1

x_component = Component(x)
print x_component.process()
```

Above we are defining a method ```x``` to return a variable. All methods are expected to return some kind of data. We then create our ```Component``` instance with our ```x``` method. Lastly we run the ```process``` method on the ```Component``` instance. The ```process``` is a special method that returns the results of the component.

**Connections**

When you have multiple components, you can create connections between them. A connection describes how data flows from one component to another.

```python
from python_dag.api import Component, resolve_connections

def x():
  return 1

def add(x, y):
  return x + y

x_component = Component(x)
add_component = Component(add)

connections = [
  (x_component, add_component, "x"),
  (x_component, add_component, "y")
]
resolve_connections(connections)

print add_component.process()
```

We continue from the single variable component ```x_component``` and create another component ```add_component```.   
The new component has arguments which needs to have some inputs. We do this by describing a list of connections, where each connection specify a source component, a target component and which argument to map the source components results to; ```(SourceComponent, TargetComponent, Argument)```. This is only a list of the connections, so we need to actually connect the components, which is done with ```resolve_connections```. Lastly we compute the ```add_component``` and its connections resulting in ```2```.

**Keyword Arguments**

You can use keyword arguments as you normally would with Python in python-dag.

```python
from python_dag.api import Component, resolve_connections

def x():
  return 1

def add(x, y=1):
  return x + y

x_component = Component(x)
add_component = Component(add)

connections = [
  (x_component, add_component, "x")
]
resolve_connections(connections)

print add_component.process()
```

If there are no connections to a keyword argument, it will use the default value specified. The result of processing ```add_component``` in the above example will return ```2```, because ```y``` has no connections and defaults to ```1```.


**Class Methods**

You can use class methods in python-dag.

```python
from python_dag.api import Component, resolve_connections

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
print add_component.process()
```

When you are using class method with python-dag you will need to instantiate the class, since python-dag does not support unbound class methods. Trying to use unbound class methods will result in an error.

**Unknown Arguments**

You can use an unknown amount of arguments with ```*args```

```python
from python_dag.api import Component, resolve_connections

def add(*args):
    return sum(args)

def x():
    return 1

x_component = Component(x)
add_component = Component(add)
connections = [
    (x_component, add_component, "args"),
    (x_component, add_component, "args"),
    (x_component, add_component, "args"),
]

resolve_connections(connections)
print add_component.process()
```

Note that you don't need to use the name ```args```, which is just consider standard practise in Python.
