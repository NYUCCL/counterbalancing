from collections import defaultdict, deque
import random
from itertools import product

class Experiment(object):

    def __init__(self, params):
        self.params = params
        self.paramCounts = {}
        self.assignments = defaultdict(dict)
        for param in self.params:
            if len(param.conditioned_on) == 0:
                self.param.dist = dict.fromkeys(param.choices)
            else:
                conditioned_choices = [] 
                for conditioner in self.param.conditioned_on:
                    conditioned_choices.append(conditioner.choices)
                conditioners = list(product(*conditioned_choices))
                self.param.dist = dict.fromkeys(conditioners, dict.fromkeys(param.choices))
  
    def assign(self, subject_id):
        unassigned = deque()
        if not self.assignments[subject_id]:
            self.assignments[subject_id] = {}
            for param in self.params:
                if len(param.choices) != 0:
                    if len(param.conditioned_on) == 0:
                        min_value = min(param.dist.itervalues())
                        min_keys = [k for k in param.dist if param.dist[k] == min_value]
                        assignment = random.choice(min_keys)
                        param.dist[assignment] += 1
                    else:
                        unassigned.appendLeft(param)
                    self.assignments[subject_id][param] = assignment
            while unassigned:
                param = unassigned.pop()
                conditioned_choices = []
                has_values = True
                for conditioner in param.conditioned_on:
                    if self.assignments[subject_id][conditioner]:
                        conditioned_choices.append(self.assignments[subject_id][conditioner])
                    else:
                        break
                if has_values:
                    dist = param.dist[conditioned_choices]
                    min_value = min(dist.itervalues())
                    min_keys = [k for k in dist if dist[k] == min_value]
                    assignment = random.choice(min_keys)
                    param.dist[conditioned_choices][assignment] += 1
                    self.assignments[subject_id][param] = assignment
        return self.assignments[subject_id]
                


# Example color = (choices=["red", "green"], conditioned_on=["shape"])
# color.choices = ("red":0, "green":1)