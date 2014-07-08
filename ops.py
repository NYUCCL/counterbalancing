import hashlib
import time
import copy
from collections import defaultdict

class Ops(object):
    
    def __init__(self):
        self.timestamp = time.clock()
        self.LONG_SCALE = float(0xFFFFFFFFFFFFFFF)
    
    def getHash(self,subject_id):
        sid = str(subject_id + self.timestamp)
        return int(hashlib.sha1(sid).hexdigest()[:15], 16)
        
    def getUniform(self, subject_id, min_val=0.0, max_val=1.0):
        zero_to_one = self.getHash(subject_id)/self.LONG_SCALE
        return min_val + max_val*zero_to_one
    
    def randomFloat(self, num_subjects, max_val=1, min_val=0):
        assignments = []
        for i in range(0, num_subjects):
            assignments.append(self.getUniform(i, min_val, max_val))    
        return assignments
    
    def randomInteger(self, num_subjects, max_val=1, min_val=0):
        assignments = []
        for i in range(0, num_subjects):
            assignments.append(min_val + self.getHash(i) % (max_val - min_val + 1))
        return assignments
        
    def bernoulliTrial(self, num_subjects, p):
        assignments = []
        for i in range(0, num_subjects):
            rand_val = self.getUniform(i)
            assignments.append(1 if rand_val <= p else 0)
        return assignments
        
    def uniformChoice(self, num_subjects, choices):
        assignments = []
        if len(choices) != 0:
            for i in range(0, num_subjects):
                rand_index = self.getHash(i) % len(choices)
                assignments.append(choices[rand_index])  
        return assignments
    
    def weightedChoice(self, num_subjects, choices, weights):
        assignments = []
        if len(choices) != 0:
            cum_weights = dict(zip(choices, weights))
            cum_sum = 0.0
            for choice in cum_weights:
                cum_sum += cum_weights[choice]
                cum_weights[choice] = cum_sum
            for i in range(0, num_subjects):
                stop_value = self.getUniform(i, 0.0, cum_sum)
                for choice in cum_weights:
                    if stop_value <= cum_weights[choice]:
                        assignments.append(choice)
        return assignments 
            
    def sample(self, num_subjects, choices, draws=-1):
        assignments = []
        if draws == -1:
            draws = len(choices)
        for n in range(0, num_subjects):
            for i in xrange(len(choices) - 1, 0, -1):
                j = self.getHash(i) % (i + 1)
                choices[i], choices[j] = choices[j], choices[i]
            assignments.append(choices[:draws])
        return assignments        
        
    def roundRobin(self, num_subjects, choices):
        rounds = num_subjects/len(choices) + 1
        assignments = choices * rounds
        assignments = self.sample(1, assignments, num_subjects)[0]
        return assignments
        
    def conditionedRoundRobin(self, conditioners, choices):
        assignments = []
        counts = dict.fromkeys(choices, 0)
        conditions = defaultdict(dict)
        for i in range(conditioners.shape[0]):
            conds = str(conditioners.values[i])
            print conditions
            if not conditions[conds]:
                conditions[conds] = dict(zip(choices, [0] * len(choices))) 
                c = self.uniformChoice(1, choices)[0]
            else:
                min_value = min(conditions[conds].itervalues())
                min_keys = [k for k in conditions[conds] if conditions[conds][k] == min_value]
                c = self.uniformChoice(1, min_keys)[0]
            conditions[conds][c] += 1
            assignments.append(c)     
        return assignments
            
        
