import pandas as pd
import ops as o

class Experiment(object):

    def __init__(self, table=None):
        self.params = dict()
        self.ncparams = dict()
        self.cparams = dict()
        if table == None:
            self.table = pd.DataFrame()
        else:
            self.table = table
  
    def add_param(self, param, op, conditioned_on = None):
        self.params[param] = [op, conditioned_on]
        if conditioned_on == None:
            self.ncparams[param] = op
        else:
            self.cparams[param] = [op, conditioned_on]

    def create_table(self, num_subjects):
        self.table = pd.DataFrame()
        for param in self.ncparams:
            self.table[param] = self.ncparams[param](num_subjects)
        for param in self.cparams:
            conditioners = self.table[self.cparams[param][1]]
            self.table[param] = self.cparams[param][0](conditioners)
        self.table["assigned"] = [0] * num_subjects
        return self.table
                    
    def assign(self, subject_id=-1):
        if subject_id >= 0:
            index = subject_id
        else:
            index = self.table[self.table["assigned"] == 0].index[0]
        self.table["assigned"][index] = 1
        return self.table.iloc[index]



        
        
