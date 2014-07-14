import unittest
import ops
from experiment import Experiment

class CounterbalanceTestCase(unittest.TestCase):
    def set_up(self):
        e = Experiment()
        e.add_param("color", uniformChoice(choices = ["blue", "green"]))
        e.add_param("shape", conditionedRoundRobin(choices = ["square", "circle"]), ["color"])
        e.create_table(10)
        
    def test_dict(self):
        a = self.e.assign(4)
        b = self.e.assign(4)
        assert a == b
        
    def test_dist(self):
        assert self.e.table.stack().value_counts()["square"] == 5
        
if __name__ == '__main__':
    unittest.main()
