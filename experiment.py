from collections import defaultdict
from numpy import *
import random

class Experiment(object):

    def __init__(self, params):
        self.params = params
        self.paramCounts = {}
        self.assignments = defaultdict(dict)
        for param in self.params:
            param.dist = dict.fromkeys(param.choices)
  
    def assign(self, subject_id):
        if self.assignments[subject_id]:
            return self.assignments[subject_id]
        else:
            for param in self.params:
                if len(param.choices) == 0:
                    continue
                elif len(param.conditioned_on) == 0:
                    min_value = min(param.dist.itervalues())
                    min_keys = [k for k in d if param.dist[k] == min_value]
                    assignment = random.choice(min_keys)
                    param.dist[assignment] += 1
                self.assignments[subject_id] = dict(param=assigment)
                
                


# Example color = (choices=["red", "green"], conditioned_on=["shape"])
# color.choices = ("red":0, "green":1)