# --*-- coding:utf-8 --*--
"""
项目：
作者：Wang
日期：2024年06月11日
"""
from collections import Counter
import random
import networkx as nx
import matplotlib.pyplot as plt



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

def all_short_paths(graph, word1):
    """
    Finds and prints all shortest paths from word1 to all other nodes in the directed graph graph.

    Args:
    graph (networkx.DiGraph): The directed graph.
    word1 (str): The starting word.
    """
    for word2 in graph.nodes():
        if word2 != word1:
            paths = shortest_path(graph, word1, word2)
            if not paths:
                print(f'there is no path from "{word1}" to "{word2}"\n')
            else:
                print(f'the shortest path from {word1} to {word2} is:')
                len_weight = None  # Initialize len_weight
                for path in paths:
                    len_weight = path.pop()
                    print(f' - {" -> ".join(map(str, path))}')
                if len_weight is not None:
                    print(f'总步长为： {str(len_weight)}\n')

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

def show_directed_graph(graph):
    """
    Displays a directed graph and saves the result as an image.

    Args:
    graph (networkx.DiGraph): The directed graph.
    """
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue',
            edge_color='gray', node_size=1400, font_size=10,
            font_weight='bold', arrowstyle='->', arrowsize=20)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.axis('equal')
    plt.savefig("directing_graph.png")

def query_bridge_words(graph, word1, word2):
    """
    Finds and returns bridge words between word1 and word2 in a directed graph graph.

    Args:
    G (networkx.DiGraph): The directed graph.
    word1 (str): The first word.
    word2 (str): The second word.

    Returns:
    str: A message indicating the bridge words or absence thereof.
    """
    word1 = word1.lower()
    word2 = word2.lower()
    if word1 not in graph and word2 not in graph:
        return f'No "{word1}" and "{word2}" in the graph!'
    if word1 not in graph:
        return f'No "{word1}" in the graph!'
    if word2 not in graph:
        return f'No "{word2}" in the graph!'

    bridge_words = [node for node in graph.nodes() if
                    word1 in graph.predecessors(node) and word2 in graph.successors(node)]

    if not bridge_words:
        return f'No bridge words from "{word1}" to "{word2}"!'
    if len(bridge_words) == 1:
        return f'The bridge word from "{word1}" to "{word2}" is: {bridge_words[0]}.'
    bridge_words_list = ", ".join(bridge_words[:-1])
    return (f'The bridge words from "{word1}" to "{word2}" are:'
            f' {bridge_words_list}, and {bridge_words[-1]}.')

def query_bridge_words_s(graph, word1, word2):
    """
    Finds and returns a random bridge word between word1 and word2 in a directed graph graph.

    Args:
    graph (networkx.DiGraph): The directed graph.
    word1 (str): The first word.
    word2 (str): The second word.

    Returns:
    str: A bridge word or 0 if no bridge word exists.
    """
    word1 = word1.lower()
    word2 = word2.lower()
    if not (word1 in graph and word2 in graph):
        return 0

    bridge_words = [node for node in graph.nodes() if
                    word1 in graph.predecessors(node) and word2 in graph.successors(node)]

    if not bridge_words:
        return 0
    if len(bridge_words) == 1:
        return bridge_words[0]
    return bridge_words[random.randint(0, len(bridge_words) - 1)]

def generate_new_text(input_text, graph):
    """
    Generates new text by inserting bridge words between consecutive words in the input text.

    Args:
    input_text (str): The input text.
    graph (networkx.DiGraph): The directed graph.

    Returns:
    str: The generated text.
    """
    words = ['']
    strings_to_words(input_text, words)
    processed_words = [word.strip(".,!?()[]{}:;\"'<>") for word in words]
    new_words = []
    for i in range(len(processed_words) - 1):
        word1 = processed_words[i]
        word2 = processed_words[i + 1]
        bridge_words = query_bridge_words_s(graph, word1, word2)
        if bridge_words:
            new_words.append(word1)
            new_words.append(bridge_words)
        else:
            new_words.append(word1)
    new_words.append(processed_words[-1])
    return ' '.join(new_words)

def random_walk(graph):
    """
    Performs a random walk on the directed graph graph and writes the path to a file.

    Args:
    graph (networkx.DiGraph): The directed graph.
    """
    start = True
    while start:
        current_node = random.choice(list(graph.nodes()))
        passed_node = [current_node]
        passed_edge = []
        while True:
            next_nodes = list(graph.successors(current_node))
            if not next_nodes:
                break
            next_node = random.choice(next_nodes)
            next_edge = (current_node, next_node)
            if next_edge in passed_edge:
                passed_node.append(next_node)
                break
            passed_node.append(next_node)
            passed_edge.append(next_edge)
            current_node = next_node
        write_to_file(passed_node)
        yesno = input('是否继续? 是[Y] 否[任意输入]\n')
        if yesno == 'Y':
            print('继续\n')
        else:
            print('中止\n')
            start = False

def write_to_file(passed_node):
    """
    Writes the nodes of the passed path to a file.
    """
    file_path = "randomWalkoutput.txt"
    with open(file_path, 'a', encoding='utf-8') as file:
        for node in passed_node:
            file.write(node + ' ')
        file.write('\n')

# 示例使用

#根据桥介词生成新文本测试样例
#inputText='Seek to explore new and exciting synergies'
#生成图文本
# strings='To @ explore strange new worlds,To seek out new life and new civilizations?'
# wordlist=['']
#
# strings2word(strings,wordlist)
# G=nx.DiGraph()
# creatPIC(wordlist,G)
#word1, word2 = input("Enter two words: ").split()
#path = shortestPATH(G, word1, word2)
#print(path)
#print("The shortest path from {} to {} is: {}".format(word1, word2, " -> ".join(path)))
#print(G[('to','explore')].get('weight',None))
#generateNewText(inputText, G)
#print(generateNewText(inputText, G))
#showDirectedGraph(G)
#word1, word2 = input("Enter two words: ").split()
#print(query_bridge_words(G,word1,word2))
#randomWalk(G)
