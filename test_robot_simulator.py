import unittest
from unittest.mock import patch
from io import StringIO
from robot_simulator import simulation
import os

directory = './test_data'

files = os.listdir(directory)
tests = []
for filename in files:
    with open(os.path.join(directory, filename), 'r') as file:
        content = file.read().split("\nOutput: ")
        inputs = content[0].split("\n")
        output = content[1]
        tests.append({ 
            "inputs": inputs,
            "output": output,
            "test_name": filename,
        })


class TestRobotSimulation(unittest.TestCase):
    pass

for index, test in enumerate(tests):
    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=test["inputs"])
    def test_scenario(self, mock_input, mock_stdout, test=test):
        simulation()
        self.assertEqual(mock_stdout.getvalue().strip().split("\n")[-1], test["output"])


    setattr(TestRobotSimulation, f'test_scenario_{test["test_name"]}', test_scenario)

if __name__ == '__main__':
    unittest.main()
