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
The new component has arguments which needs to have some inputs. We do this by describing a list of connections, where each connection specify a source component, a target component and which argument to map the source components results to; ```(SourceComponent, TargetComponent, Argument)```. Lastly
