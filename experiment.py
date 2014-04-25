from collections import defaultdict, deque
import random
import copy
from itertools import product

class Experiment(object):

    def __init__(self, params):
        self.params = params
        self.paramCounts = {}
        self.assignments = defaultdict(dict)
        for param in self.params:
            d = dict.fromkeys(param["choices"], 0)
            if len(param["conditioned_on"]) == 0:
                param["dist"] = copy.deepcopy(d)
            else:
                conditioned_choices = [] 
                for conditioner in param["conditioned_on"]:
                    conditioned_choices.append(conditioner["choices"])
                conditioners = list(product(*conditioned_choices))
                param["dist"] = dict((c,copy.deepcopy(d)) for c in conditioners)
  
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
                        has_values = False
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
        
    def remove(self, subject_id):
        if self.assignments[subject_id]:
            for param in self.params:
                assignment = self.assignments[subject_id][param["name"]]
                if len(param["choices"]) != 0:
                    if len(param["conditioned_on"]) == 0:
                        param["dist"][assignment] -= 1
                    else:
                        conditioned_choices = []
                        for conditioner in param["conditioned_on"]:
                            conditioned_choices.append(self.assignments[subject_id][conditioner["name"]])
                        cc = tuple(conditioned_choices)
                        param["dist"][cc][assignment] -= 1