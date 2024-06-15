import unittest
from collections import Counter
import random
import networkx as nx
import matplotlib.pyplot as plt
def strings_to_words(strings, wordlist):
    """
    Splits a string into a list of words.

    Args:
    strings (str): The input string.
    wordlist (list): The list to store the words.
    """
    i = 0
    temp = 0
    for letter in strings:
        if letter.isalpha():
            if temp == 1:
                wordlist.append('')
            if len(wordlist) <= i:
                wordlist.append('')
            wordlist[i] += letter.lower()
            temp = 0
        elif temp == 0:
            i += 1
            temp = 1
def shortest_path(graph, word1, word2):
    """
        Finds the shortest path in a directed graph graph from word1 to word2.

        Args:
        graph (networkx.DiGraph): The directed graph.
        word1 (str): The starting word.
        word2 (str): The destination word.

        Returns:
        list: The shortest path as a list of nodes, or an empty list if no path exists.
        """
    if word1==word2:
        return [[word1,word2,0]]
    if word1 not in graph or word2 not in graph:
        return []
    paths = [[word1, 0]]
    shortest_len = 0
    while True:
        for path in paths:
            if path[-2] == word2:
                if shortest_len == 0:
                    shortest_len = path[-1]
                else:
                    shortest_len = min(shortest_len, path[-1])
        if shortest_len:
            paths_emp = [path for path in paths if path[-2] == word2 and path[-1] == shortest_len]
            return paths_emp
        paths_copy = []
        for path in paths:
            if list(graph.successors(path[-2])):
                weight = path.pop(-1)
                for next_node in list(graph.successors(path[-1])):
                    weight_temp = graph.get_edge_data(path[-1], next_node,
                                                      default=None).get('weight', 0)
                    weight_temp += weight
                    paths_copy.append(path + [next_node] + [weight_temp])
        if not paths_copy:
            return []
        paths = paths_copy

def create_pic(wordlist, graph):
    """
    Creates a directed graph from a list of words.

    Args:
    wordlist (list): The list of words.
    graph (networkx.DiGraph): The directed graph.
    """
    dic = Counter(wordlist)
    for v in dic:
        graph.add_node(v)
    edgeslist = []
    for i, v in enumerate(wordlist):
        if i >= 1:
            edge = f'{wordlist[i - 1]} {v}'
            edgeslist.append(edge)
    edge_num = Counter(edgeslist)
    for k, v in edge_num.items():
        edge_div_list = ['']
        strings_to_words(k, edge_div_list)
        graph.add_edge(edge_div_list[0], edge_div_list[1], weight=v)
        
class TestShortestPath(unittest.TestCase):

    def setUp(self):
        # 创建一个空的有向图
        self.graph = nx.DiGraph()

    def test_normal_path(self):
        # 测试两个节点之间直接存在路径的情况
        wordlist = ['apple', 'banana', 'cherry']
        create_pic(wordlist, self.graph)
        path = shortest_path(self.graph, 'apple', 'cherry')
        self.assertEqual(path, [['apple', 'banana', 'cherry', 2]])

    def test_multiple_paths(self):
        # 测试两个节点之间存在多条路径的情况
        wordlist = ['apple', 'banana', 'cherry', 'date', 'banana', 'cherry']
        create_pic(wordlist, self.graph)
        path = shortest_path(self.graph, 'apple', 'cherry')
        self.assertEqual(path, [['apple', 'banana', 'cherry', 3]])

    def test_no_path(self):
        # 测试两个节点之间不存在路径的情况
        wordlist = ['apple', 'banana', 'cherry']
        create_pic(wordlist, self.graph)
        path = shortest_path(self.graph, 'apple', 'date')
        self.assertEqual(path, [])

    def test_same_node(self):
        # 测试起点和终点是同一个节点的情况
        wordlist = ['apple', 'banana', 'apple']
        create_pic(wordlist, self.graph)
        path = shortest_path(self.graph, 'apple', 'apple')
        self.assertEqual(path, [['apple', 'apple', 0]])

    def test_empty_graph(self):
        # 测试图为空的情况
        path = shortest_path(self.graph, 'apple', 'banana')
        self.assertEqual(path, [])

    def test_non_existent_nodes(self):
        # 测试输入的起点或终点不在图中的情况
        wordlist = ['apple', 'banana', 'cherry']
        create_pic(wordlist, self.graph)
        path = shortest_path(self.graph, 'orange', 'banana')
        self.assertEqual(path, [])

    def test_sparse_graph(self):
        # 测试稀疏图的最短路径查询
        wordlist = ['apple', 'banana', 'cherry', 'date', 'apple', 'date']
        create_pic(wordlist, self.graph)
        path = shortest_path(self.graph, 'apple', 'date')
        self.assertEqual(path, [['apple', 'date', 1]])

    def test_dense_graph(self):
        # 测试稠密图的最短路径查询
        wordlist = ['apple', 'banana', 'apple', 'cherry', 'banana', 'cherry', 'apple', 'date']
        create_pic(wordlist, self.graph)
        path = shortest_path(self.graph, 'apple', 'date')
        self.assertEqual(path, [['apple', 'date', 1]])

    def test_large_graph(self):
        # 测试大规模图的最短路径查询
        wordlist = ['apple'] * 100 +['orange','data']*50+ ['banana'] * 100
        create_pic(wordlist, self.graph)
        path = shortest_path(self.graph, 'apple', 'banana')
        self.assertEqual(path, [['apple', 'orange', 'data', 'banana', 52]])


if __name__ == '__main__':
    unittest.main()
