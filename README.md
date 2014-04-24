Counterbalancing
================

Library for implementing counterbalancing for web-based experiments

How to create an experiment with a color variable and a shape variable
```python
color = {}
shape = {}
shape["choices"] = ["square", "circle"]
shape["conditioned_on"] = []
shape["name"] = "shape"
color["choices"] = ["green", "blue"]
color["conditioned_on"] = [shape]
color["name"] = "color"

e = Experiment ([color, shape])
e.assign(1)
Output: {'color': 'green', 'shape': 'circle'}
e.assign(1)
Out: {'color': 'green', 'shape': 'circle'} # same user id gets same assignment
e.assign(2)
Out: {'color': 'blue', 'shape': 'square'}
```
