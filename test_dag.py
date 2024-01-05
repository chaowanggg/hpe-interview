import unittest
from dag import DAG  

class TestDAG(unittest.TestCase):
    def test_empty_graph(self):
        with self.assertRaises(ValueError):
            DAG("") 

    def test_valid_dag_construction(self):
        input_str = "A:\nB: A\nC: B, A"
        dag = DAG(input_str)
        self.assertEqual(set(dag.graph.nodes()), {"A", "B", "C"})
        self.assertEqual(set(dag.graph.edges()), {("A", "B"), ("B", "C"), ("A", "C")})

    def test_invalid_dag_construction(self):
        with self.assertRaises(ValueError):
            DAG("A:\nB: A\nB: C")  # Duplicate node definitions
        with self.assertRaises(ValueError):
            DAG("A1:\nB-2: A1")    # Invalid node names
        with self.assertRaises(ValueError):
            DAG("A: B\nB: A")      # Cycle detection

    def test_find_leaves(self):
        input_str = "A:\nB: A\nC: A"
        dag = DAG(input_str)
        self.assertEqual(set(dag.find_leaves()), {"B", "C"})


    def test_find_ancestors(self):
        test_cases = [
            ("A:", {"A": {"A"}}), # one node
            ("A:\nB: A", {"A": {"A"}, "B": {"A", "B"}}), # two node in one line
            ("A:\nB:\nC: B", {"A": {"A"}, "B": {"B"}, "C": {"B", "C"}}), 
            ("A:\nB: A\nC: A\nD: B, C", {"A": {"A"}, "B": {"A", "B"}, "C": {"A", "C"}, "D": {"A", "B", "C", "D"}}),
            ("A:\nB: A\nC: A\nD: B, C\nE: B, C", {"A": {"A"}, "B": {"A", "B"}, "C": {"A", "C"}, "D": {"A", "B", "C", "D"}, "E": {"A", "B", "C", "E"}})
        ]
        for input_str, expected_ancestors in test_cases:
            dag = DAG(input_str)
            ancestors = dag.find_ancestors()
            self.assertEqual(ancestors, expected_ancestors)


    def test_find_ancestors_complex_graph(self):
        input_str = "A:\nB: A\nC: B\nD:\nE: D\nF: C, E\nG: F\nH: G"
        dag = DAG(input_str)
        ancestors = dag.find_ancestors()
        expected_ancestors = {
            "A": {"A"},
            "B": {"A", "B"},
            "C": {"A", "B", "C"},
            "D": {"D"},
            "E": {"D", "E"},
            "F": {"A", "B", "C", "D", "E", "F"},
            "G": {"A", "B", "C", "D", "E", "F", "G"},
            "H": {"A", "B", "C", "D", "E", "F", "G", "H"}
        }
        self.assertEqual(ancestors, expected_ancestors)


    def test_find_bisectors(self):
        test_cases = [
            ("A:\nB: A\nC: A\nD:B, C", {"B", "C"}),
            ("A:\nB: A\nC: B\nD:\nE: D\nF: C, E\nG: F\nH: G", {"C"})
        ]

        for input_str, expected in test_cases:
            dag = DAG(input_str)
            self.assertEqual(set(dag.find_bisectors()), expected)

if __name__ == '__main__':
    unittest.main()
