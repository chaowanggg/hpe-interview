#!/usr/bin/env python3
import networkx as nx
import re

from collections import defaultdict
EMPTY_SET = set()
class DAG:
    """
        O(V + E)
    """
    def __init__(self, input_str):
        self.graph = self.build_dag(input_str)
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Input does not form a DAG.")
        self.node_to_ancestors = defaultdict(set)



    def build_dag(self, input_str):
        graph = nx.DiGraph()
        parsed_graph = self.parse_graph(input_str)
        for node, parents in parsed_graph.items():
            for parent in parents:
                graph.add_edge(parent, node)
        return graph

    def parse_graph(self, input_str):
        valid_name_pattern = re.compile("^[A-Za-z0-9]+$")
        parsed_graph = {}
        if not input_str:
            raise ValueError("empty string")
        for line in input_str.strip().split('\n'):
            parts = line.split(':')
            node = parts[0].strip()
            if not valid_name_pattern.match(node):
                raise ValueError("Invalid node name.")
            if node in parsed_graph:
                raise ValueError("Duplicate node definition found.")
        
            parents = parts[1].strip().split(',') if len(parts) > 1 else []
            parsed_graph[node] = [parent.strip() for parent in parents if parent.strip()]
        return parsed_graph

    """
    Time: O(V)
    """
    def find_leaves(self):
        return [node for node, out_degree in self.graph.out_degree() if out_degree == 0]
    
    """
 
    """

    """
       all ancestors O(V + E) higher than that
       3:30
    """


    """
        DFS(node) traverse the node from itself to all its parents and update the ancestors for the node
            if encountered a ancestors alread in cache, return it
        base case: node ancestors already be calcualted 

    """
    def find_ancestors(self):   
        def dfs(node):
            ## Check
            if self.node_to_ancestors[node] != EMPTY_SET:
                return self.node_to_ancestors[node]

            ancestors = set([node])  # A node is an ancestor of itself
            for parent in self.graph.predecessors(node):
                parent_ancestors = dfs(parent)  
                ancestors |= parent_ancestors
            
            ## Store
            self.node_to_ancestors[node] = ancestors
            return ancestors

        for node in self.graph.nodes():
            if self.node_to_ancestors[node] == EMPTY_SET:
                continue 
            dfs(node)

        return self.node_to_ancestors
        
    """
    Time: O(V*(V + E)) => O(V^2)
    """
    def find_bisectors(self):
        N = len(self.graph.nodes)
        bisector_scores = {}
        for node in self.graph.nodes: #O(V)
            A = len(self.find_ancestors(node))
            bisector_scores[node] = min(A, N - A)
        max_score = max(bisector_scores.values())
        result = [node for node, score in bisector_scores.items() if score == max_score]
        return result
##TODO: call find_ancestors to every one
##TODO     Time: calculate all ancestors
# brendon@pachyderm.io

"""
   Time: find a single node's ancestors O(V + E)

    Time: calculate all ancestors

    nx:
        [node: parent]
        [node: parent]
        1. find the parent O(1)
        2. out_degree for each node O(1)

        D
        / \   
        B  C
        \ /

         A

        # 1. memo or cache 
        # 2. concat the ancestors 
        #     ancestors(A) = ancestors(B) + C + A
"""