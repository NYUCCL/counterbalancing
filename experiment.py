from collections import defaultdict, deque
import random
import copy
from itertools import product
import time
import csv

class Experiment(object):

    def __init__(self, params, length=100000000000):
        """
        Initializes the experiment
        Arguments:
        params -- a set of dictionaries, one for each parameter. 
            Each dict must include: 
                ["choices"] - a list of strings of options for that parameter, e.g. ["square", "circle"]
                ["conditioned_on"] - a list of dicts of other parameters the choice should be conditioned
                    on. e.g. [color, number]
                ["name"] - the name of the parameter
        length -- the length of the experiment
        """
        self.params = params
        self.paramCounts = {}
        self.assignments = defaultdict(dict)
        self.length = length
        for param in self.params:
            d = dict.fromkeys(param["choices"], 0)
            if len(param["conditioned_on"]) == 0:
                param["dist"] = copy.deepcopy(d)
            else:
                conditioned_choices = [] 
                for conditioner in param["conditioned_on"]:
                    conditioned_choices.append(conditioner["choices"])
                conditioners = list(product(*conditioned_choices))
                conditioners.append(param["name"])
                param["dist"] = dict((c,copy.deepcopy(d)) for c in conditioners)
  
    def assign(self, subject_id, check=False):
        """
        Assigns a subject to a condition
        Arguments:
        subject_id -- subject hash
        check -- if true, removes subjects that have been in the experiment for too long
        """
        unassigned = deque()
        if check:
            self.check_time_outs()
        if not self.assignments[subject_id]:
            self.add_subject(subject_id)
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
                    param["dist"][param["name"]][assignment] += 1
                    self.assignments[subject_id][param["name"]] = assignment
        return self.assignments[subject_id]
    
    def add_subject(self, subject_id):
        """
        Adds a new subject to the database
        Arguments:
        subject_id -- subject hash
        """
        self.assignments[subject_id] = {}
        self.assignments[subject_id]["completed"] = False
        self.assignments[subject_id]["time_stamp"] = time.time()
        self.assignments[subject_id]["removed"] = False
        
    
    def remove(self, subject_id):
        """
        Removes a subject from the counts of parameters. However, the subject's assignment to parameters remains in the database
        Arguments:
        subject_id -- subject hash
        """
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
                        param["dist"][param["name"]][assignment] -= 1
    
    def completed(self, subject_id):
        """
        Marks a subject as having completed the experiment. If they had been removed before, adds them back to the counts
        Arguments:
        subject_id -- subject hash
        """
        self.assignments[subject_id]["completed"] = True
        if self.assignments[subject_id]["removed"]:
            for param in self.params:
                assignment = self.assignments[subject_id][param["name"]]
                if len(param["choices"]) != 0:
                    if len(param["conditioned_on"]) == 0:
                        param["dist"][assignment] += 1
                    else:
                        conditioned_choices = []
                        for conditioner in param["conditioned_on"]:
                            conditioned_choices.append(self.assignments[subject_id][conditioner["name"]])
                        cc = tuple(conditioned_choices)
                        param["dist"][cc][assignment] += 1
                        param["dist"][param["name"]][assignment] += 1
        
    def check_time_outs(self):
        """
        Checks if each subject has timed out of the experiment and if so, removes them from the counts
        """
        for subject_id in self.assignments:
            subject = self.assignments[subject_id]
            if not subject["completed"] and not subject["removed"] and time.time() - subject["time_stamp"] > self.length:
                self.remove(subject_id)
                subject["removed"] = True

    def write_csv(self, write_file):
        """
        Writes assignments to file
        Arguments:
        write_file -- file name
        """
        with open(write_file, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            header = ["subject_id"]
            conditions = self.assignments.itervalues().next().keys()
            header.extend(conditions)
            writer.writerow(header)
            for subject_id in self.assignments:
                row = [subject_id]
                row.extend(self.assignments[subject_id].values())
                writer.writerow(row)
            