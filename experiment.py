from collections import defaultdict, deque
import random
from itertools import product

class Experiment(object):

    def __init__(self, params):
        self.params = params
        self.paramCounts = {}
        self.assignments = defaultdict(dict)
        for param in self.params:
            if len(param["conditioned_on"]) == 0:
                param["dist"] = dict.fromkeys(param["choices"], 0)
            else:
                conditioned_choices = [] 
                for conditioner in param["conditioned_on"]:
                    conditioned_choices.append(conditioner["choices"])
                conditioners = list(product(*conditioned_choices))
                param["dist"] = dict.fromkeys(conditioners, dict.fromkeys(param["choices"], 0))
  
    def assign(self, subject_id):
        unassigned = deque()
        if not self.assignments[subject_id]:
            self.assignments[subject_id] = {}
            for param in self.params:
                if len(param["choices"]) != 0:
                    if len(param["conditioned_on"]) == 0:
                        min_value = min(param["dist"].itervalues())
                        min_keys = [k for k in param["dist"] if param["dist"][k] == min_value]
                        assignment = random.choice(min_keys)
                        param["dist"][assignment] += 1
                        self.assignments[subject_id][param["name"]] = assignment
                    else:
                        unassigned.appendleft(param)
            while unassigned:
                param = unassigned.pop()
                conditioned_choices = []
                has_values = True
                for conditioner in param["conditioned_on"]:
                    if self.assignments[subject_id][conditioner["name"]]:
                        conditioned_choices.append(self.assignments[subject_id][conditioner["name"]])
                    else:
                        break
                if has_values:
                    cc = tuple(conditioned_choices)
                    dist = param["dist"][cc]
                    min_value = min(dist.itervalues())
                    min_keys = [k for k in dist if dist[k] == min_value]
                    assignment = random.choice(min_keys)
                    param["dist"][cc][assignment] += 1
                    self.assignments[subject_id][param["name"]] = assignment
        return self.assignments[subject_id]
                
# Example color = (choices=["red", "green"], conditioned_on=["shape"])
# color.choices = ("red":0, "green":1)