import unittest
from experiment import Experiment

class CounterbalanceTestCase(unittest.TestCase):
    def set_up(self):
        color = {}
        shape = {}
        shape["choices"] = ["square", "circle"]
        shape["conditioned_on"] = []
        shape["name"] = "shape"
        color["choices"] = ["green", "blue"]
        color["conditioned_on"] = [shape]
        color["name"] = "color"
        self.e = Experiment([color, shape])
        
    def test_dict(self):
        a = self.e.assign(1)
        b = self.e.assign(2)
        assert a == b
        
    def test_dist(self):
        for i in range(100):
            self.e.assign(i)
        assert self.e.params[0]["dist"]["blue"] == 50
        
if __name__ == '__main__':
    unittest.main()
